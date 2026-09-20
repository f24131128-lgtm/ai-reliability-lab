import unittest
from pathlib import Path

from ai_reliability.evaluation.records import day06_record
from ai_reliability.io import read_csv
from ai_reliability.metrics.risk_coverage import evaluate_risk_coverage


class RiskCoverageTests(unittest.TestCase):
    def test_legacy_day6_has_ten_observed_threshold_points(self):
        records = [day06_record(row) for row in read_csv(Path("data/demo/day06_risk_coverage.csv"))]
        result = evaluate_risk_coverage(records)
        self.assertEqual(result.denominator, 10)
        self.assertEqual(len(result.value), 10)
        self.assertEqual(result.value[-1]["coverage"], 1.0)
        self.assertEqual(result.value[-1]["risk"], 0.4)
        self.assertIn("not calibrated", result.metadata["confidence_note"])

    def test_threshold_selection_changes_coverage_and_risk(self):
        rows = [
            {"case_id": "high", "confidence": "0.9", "correct": "1"},
            {"case_id": "low", "confidence": "0.1", "correct": "0"},
        ]
        points = evaluate_risk_coverage([day06_record(row) for row in rows]).value
        self.assertEqual(points[0]["coverage"], 0.5)
        self.assertEqual(points[0]["risk"], 0.0)
        self.assertEqual(points[-1]["risk"], 0.5)

    def test_invalid_correct_flag_is_rejected(self):
        with self.assertRaises(ValueError):
            day06_record({"case_id": "bad", "confidence": "0.5", "correct": "unknown"})
