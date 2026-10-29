"""
End-to-End Pipeline Integration Test
"""
import unittest
from pathlib import Path

from src.workday_qe.parser import load_whats_new_report, load_e2e_job_catalog
from src.workday_qe.mapper import build_targeted_regression_records
from src.workday_qe.reporter import compute_executive_metrics
from src.workday_qe.config import BASE_DIR

class TestE2EPipeline(unittest.TestCase):

    def test_full_pipeline_execution(self):
        """Validates end-to-end pipeline execution with zero guardrail violations."""
        # 1. Parse inputs
        items, injections = load_whats_new_report()
        self.assertEqual(len(items), 87, "Should load exactly 87 What's New items")
        self.assertEqual(len(injections), 0, "Production release notes should have 0 injection payloads")

        catalog_jobs = load_e2e_job_catalog()
        self.assertEqual(len(catalog_jobs), 42, "Should load exactly 42 master catalog jobs")

        # 2. Map and assert containment
        records = build_targeted_regression_records(items, catalog_jobs)
        self.assertEqual(len(records), 87, "Should produce exactly 87 regression records")

        # 3. Validate metrics
        metrics = compute_executive_metrics(records, catalog_jobs)
        self.assertEqual(metrics['total_release_items'], 87)
        self.assertEqual(metrics['mapped_items_count'], 62)
        self.assertEqual(metrics['gap_items_count'], 25)
        self.assertEqual(metrics['unique_selected_jobs_count'], 17)
        self.assertAlmostEqual(metrics['suite_reduction_pct'], 59.52, places=1)
        self.assertTrue(metrics['is_bounds_valid'])

if __name__ == "__main__":
    unittest.main()
