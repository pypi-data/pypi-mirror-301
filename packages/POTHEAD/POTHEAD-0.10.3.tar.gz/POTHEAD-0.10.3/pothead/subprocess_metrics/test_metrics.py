import glob
import os
import re
import shutil
import unittest
from tempfile import TemporaryDirectory

from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector, mark_process_dead

from . import CustomMultiProcessCollector


def _generate_sorted_metrics_report(registry: CollectorRegistry) -> str:
    return "\n".join(
        sorted(generate_latest(registry).decode("utf-8").strip().split("\n"))
    )


def _generate_default_metrics_report(files: list) -> str:
    with TemporaryDirectory() as temp_dir:
        for db_file in files:
            shutil.copy(db_file, temp_dir)
        registry = CollectorRegistry()
        MultiProcessCollector(registry, temp_dir)

        return _generate_sorted_metrics_report(registry)


class MetricsTest(unittest.TestCase):
    TESTDATA_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/testdata"

    all_metric_files = glob.glob(f"{TESTDATA_DIR}/*.db")
    all_pids = sorted(
        set(re.search(r"_(\d+)\.db", file).group(1) for file in all_metric_files)
    )
    EXPECTED_FINAL_METRICS_INCL_LIVE = _generate_default_metrics_report(
        all_metric_files
    )
    EXPECTED_FINAL_METRICS_EXCL_LIVE = _generate_default_metrics_report(
        [file for file in all_metric_files if "live" not in file]
    )

    def setUp(self):
        self.maxDiff = None
        self.prometheus_dir = TemporaryDirectory()

    def tearDown(self):
        self.prometheus_dir.cleanup()

    def _copy_source_to_prom(self, pattern="*.db"):
        db_files = glob.glob(os.path.join(MetricsTest.TESTDATA_DIR, pattern))
        for db_file in db_files:
            shutil.copy(db_file, self.prometheus_dir.name)

    def _copy_source_to_prom_with_pid_override(self, pattern, target_pid):
        db_files = glob.glob(os.path.join(MetricsTest.TESTDATA_DIR, pattern))
        for db_file in db_files:
            target_path = re.sub(
                r"_\d+\.db$", f"_{target_pid}.db", os.path.basename(db_file)
            )
            shutil.copy(db_file, f"{self.prometheus_dir.name}/{target_path}")

    def assert_metrics_dir_empty(self):
        self.assertEqual(0, len(glob.glob(os.path.join(self.prometheus_dir.name, "*"))))

    def test_collect(self):
        registry = CollectorRegistry()
        CustomMultiProcessCollector(registry, self.prometheus_dir.name)

        self._copy_source_to_prom("*.db")

        self.assertEqual(
            _generate_sorted_metrics_report(registry),
            self.EXPECTED_FINAL_METRICS_INCL_LIVE,
        )

    def test_default_process_death_handling(self):
        # Just serves as a sanity check to verify that the EXPECTED_FINAL_METRICS_EXCL_LIVE
        # is correct in terms of what the default prometheus client would do.
        registry = CollectorRegistry()
        MultiProcessCollector(registry, self.prometheus_dir.name)

        for pid in self.all_pids:
            self._copy_source_to_prom(f"*_{pid}.db")
            mark_process_dead(pid, self.prometheus_dir.name)

            generate_latest(registry)

        self.assertEqual(
            _generate_sorted_metrics_report(registry),
            self.EXPECTED_FINAL_METRICS_EXCL_LIVE,
        )

    def test_collect_staggered(self):
        registry = CollectorRegistry()
        coll = CustomMultiProcessCollector(registry, self.prometheus_dir.name)

        def expected_report(live_pids: list[int], dead_pids: list[int]) -> str:
            files = []
            for pid in live_pids:
                files.extend(glob.glob(f"{MetricsTest.TESTDATA_DIR}/*_{pid}.db"))
            for pid in dead_pids:
                files.extend(
                    file
                    for file in glob.glob(f"{MetricsTest.TESTDATA_DIR}/*_{pid}.db")
                    if "live" not in file
                )
            return _generate_default_metrics_report(files)

        for pid in self.all_pids[:-1]:
            # process generated metrics and died before the first collection
            self._copy_source_to_prom(f"*_{pid}.db")
            coll.mark_process_dead(pid)

            # metric files are deleted after collection
            generate_latest(registry)
            self.assert_metrics_dir_empty()

        # last process is still alive and its metrics are also included
        self._copy_source_to_prom(f"*_{self.all_pids[-1]}.db")
        self.assertEqual(
            _generate_sorted_metrics_report(registry),
            expected_report([self.all_pids[-1]], self.all_pids[:-1]),
        )

        # last process dies and its metrics are still included
        coll.mark_process_dead(self.all_pids[-1])

        self.assertEqual(
            _generate_sorted_metrics_report(registry),
            self.EXPECTED_FINAL_METRICS_EXCL_LIVE,
        )  # NOTE: Here be the dragons regarding the 'gauge_mostrecent' metric

        # metrics are still unchanged and correct
        self.assertEqual(
            _generate_sorted_metrics_report(registry),
            self.EXPECTED_FINAL_METRICS_EXCL_LIVE,
        )

    def test_in_memory_historical_metrics_growth(self):
        registry = CollectorRegistry()
        coll = CustomMultiProcessCollector(registry, self.prometheus_dir.name)

        # Get a first baseline of stored metrics size
        for pid in self.all_pids:
            self._copy_source_to_prom(f"*_{pid}.db")
            coll.mark_process_dead(pid)
            generate_latest(registry)
            self.assert_metrics_dir_empty()
        size_of_stored_metrics = coll._historical_metrics_size_bytes()

        for i in range(1, 100):
            for pid in self.all_pids:
                fake_pid = pid * i
                # NOTE: Here be the dragons regarding the 'gauge_all' metric
                self._copy_source_to_prom_with_pid_override(f"*_{pid}.db", fake_pid)
                coll.mark_process_dead(fake_pid)
                generate_latest(registry)
                self.assert_metrics_dir_empty()

                self.assertEqual(
                    size_of_stored_metrics, coll._historical_metrics_size_bytes()
                )
