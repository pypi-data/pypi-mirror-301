import json
import os
import pickle
from collections import defaultdict
from copy import deepcopy
from glob import glob
from logging import getLogger
from threading import Lock

from prometheus_client import Metric, multiprocess
from prometheus_client.mmap_dict import MmapedDict
from prometheus_client.samples import Sample
from prometheus_client.utils import floatToGoString

LOGGER = getLogger("pothead.metrics")


class CustomMultiProcessCollector:
    """Collector for files for multi-process mode."""

    def __init__(self, registry, path=None):
        if path is None:
            path = os.environ.get("PROMETHEUS_MULTIPROC_DIR")
        if not path or not os.path.isdir(path):
            raise ValueError(
                "env PROMETHEUS_MULTIPROC_DIR is not set or not a directory"
            )
        self._path = path
        self._key_cache = {}
        self._history_lock = Lock()
        self._historical_metrics = {}
        self._dead_processes_lock = Lock()
        self._dead_process_pids = []
        if registry:
            registry.register(self)

    def _parse_key(self, key):
        val = self._key_cache.get(key)
        if not val:
            metric_name, name, labels, help_text = json.loads(key)
            labels_key = tuple(sorted(labels.items()))
            val = self._key_cache[key] = (
                metric_name,
                name,
                labels,
                labels_key,
                help_text,
            )
        return val

    def mark_process_dead(self, pid):
        with self._dead_processes_lock:
            self._dead_process_pids.append(pid)

    def _update_historical_metrics(self):
        files = []
        with self._history_lock:
            with self._dead_processes_lock:
                for pid in self._dead_process_pids:
                    # First we remove any live metrics for the dead process.
                    multiprocess.mark_process_dead(pid, self._path)
                    # Then we collect the remaining metrics for the dead process
                    # to update the in-memory historical metrics.
                    files.extend(glob(os.path.join(self._path, f"*_{pid}.db")))
                self._dead_process_pids = []

            if len(files) == 0:
                return

            # Update historical metrics with the dead process metrics.
            # Note that it is important to not accumulate the histograms as
            # that would lead to compound accumulation (accumulate=False).
            self._historical_metrics = self._accumulate_metrics(
                self._read_metrics(files, self._historical_metrics), accumulate=False
            )
            for file in files:
                LOGGER.debug("Removing %s", file)
                os.remove(file)

    def _historical_metrics_size_bytes(self):
        with self._history_lock:
            return len(pickle.dumps(self._historical_metrics))

    def merge(self, files, accumulate=True):
        """Merge metrics from given mmap files.

        By default, histograms are accumulated, as per prometheus wire format.
        But if writing the merged data back to mmap files, use
        accumulate=False to avoid compound accumulation.
        """
        return self._accumulate_metrics(
            self._read_metrics(files, self._historical_metrics), accumulate
        ).values()

    def _read_metrics(self, files, starting_metrics=None):
        metrics = {} if starting_metrics is None else deepcopy(starting_metrics)

        for f in files:
            parts = os.path.basename(f).split("_")
            typ = parts[0]
            if typ == "gauge" and parts[1] in ["all", "mostrecent"]:
                # NOTE: 'all' and 'mostrecent' gauges are currently not supported.
                # 'all' gauges are not supported because they do not work well with
                #       historical aggregation when running with short lived processes.
                #       This is because the 'all' gauges will keep track of the samples
                #       even from long dead processes and the memory usage will keep
                #       increasing.
                # 'mostrecent' gauges are not supported because the historical aggregation
                #       will not work correctly. They are currently forgotten once the process
                #       dies. We don't really need them at the moment so we are not supporting
                #       them out of simplicity.
                LOGGER.warning(f"Gauge multiprocess mode '{parts[1]}' is not supported")
                continue
            try:
                file_values = MmapedDict.read_all_values_from_file(f)
            except FileNotFoundError:
                if typ == "gauge" and parts[1].startswith("live"):
                    # Files for 'live*' gauges can be deleted between the glob of collect
                    # and now (via a mark_process_dead call) so don't fail if
                    # the file is missing
                    continue
                raise
            for key, value, timestamp, _ in file_values:
                metric_name, name, labels, labels_key, help_text = self._parse_key(key)

                metric = metrics.get(metric_name)
                if metric is None:
                    metric = Metric(metric_name, help_text, typ)
                    metrics[metric_name] = metric

                if typ == "gauge":
                    pid = parts[2][:-3]
                    metric._multiprocess_mode = parts[1]
                    metric.add_sample(
                        name, labels_key + (("pid", pid),), value, timestamp
                    )
                else:
                    # The duplicates and labels are fixed in the next for.
                    metric.add_sample(name, labels_key, value)
        return metrics

    @staticmethod
    def _accumulate_metrics(metrics, accumulate):
        for metric in metrics.values():
            samples: defaultdict[tuple[str, tuple[tuple[str, str]]], float] = (
                defaultdict(float)
            )
            buckets: defaultdict[tuple[tuple[str, str]], defaultdict[float, float]] = (
                defaultdict(lambda: defaultdict(float))
            )
            sample_timestamps: defaultdict[
                tuple[str, tuple[tuple[str, str]]], float
            ] = defaultdict(float)
            samples_setdefault = samples.setdefault

            for s in metric.samples:
                name, labels, value, timestamp, _exemplar = s
                if isinstance(labels, dict):
                    labels = tuple(sorted(labels.items()))
                if metric.type == "gauge":
                    without_pid_key = (
                        name,
                        tuple(label for label in labels if label[0] != "pid"),
                    )
                    if metric._multiprocess_mode in ("min", "livemin"):
                        current = samples_setdefault(without_pid_key, value)
                        if value < current:
                            samples[without_pid_key] = value
                    elif metric._multiprocess_mode in ("max", "livemax"):
                        current = samples_setdefault(without_pid_key, value)
                        if value > current:
                            samples[without_pid_key] = value
                    elif metric._multiprocess_mode in ("sum", "livesum"):
                        samples[without_pid_key] += value
                    elif metric._multiprocess_mode in ("mostrecent", "livemostrecent"):
                        current_timestamp = sample_timestamps[without_pid_key]
                        timestamp = float(timestamp or 0)
                        if current_timestamp < timestamp:
                            samples[without_pid_key] = value
                            sample_timestamps[without_pid_key] = timestamp
                    else:  # all/liveall
                        samples[(name, labels)] = value

                elif metric.type == "histogram":
                    # A for loop with early exit is faster than a genexpr
                    # or a listcomp that ends up building unnecessary things
                    for label in labels:
                        if label[0] == "le":
                            bucket_value = float(label[1])
                            # _bucket
                            without_le = tuple(
                                label for label in labels if label[0] != "le"
                            )
                            buckets[without_le][bucket_value] += value
                            break
                    else:  # did not find the `le` key
                        # _sum/_count
                        samples[(name, labels)] += value
                else:
                    # Counter and Summary.
                    samples[(name, labels)] += value

            # Accumulate bucket values.
            if metric.type == "histogram":
                for labels, values in buckets.items():
                    acc = 0.0
                    for bucket, value in sorted(values.items()):
                        sample_key = (
                            metric.name + "_bucket",
                            labels + (("le", floatToGoString(bucket)),),
                        )
                        if accumulate:
                            acc += value
                            samples[sample_key] = acc
                        else:
                            samples[sample_key] = value
                    if accumulate:
                        samples[(metric.name + "_count", labels)] = acc

            # Convert to correct sample format.
            metric.samples = [
                Sample(name_, dict(labels), value)
                for (name_, labels), value in samples.items()
            ]
        return metrics

    def collect(self):
        self._update_historical_metrics()
        with self._history_lock:
            files = glob(os.path.join(self._path, "*.db"))
            return self.merge(files, accumulate=True)
