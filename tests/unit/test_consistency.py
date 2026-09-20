import unittest
from pathlib import Path

from ai_reliability.evaluation.records import day02_record
from ai_reliability.io import read_csv
from ai_reliability.metrics.consistency import evaluate_consistency, jaccard


class ConsistencyTests(unittest.TestCase):
    def test_legacy_day2_demo_values(self):
        records = [day02_record(row, "test") for row in read_csv(Path("data/demo/day02_runs.csv"))]
        results = evaluate_consistency(records)
        self.assertAlmostEqual(results["unique_ratio"].value, 0.8)
        self.assertAlmostEqual(results["mode_agreement"].value, 0.4)
        self.assertAlmostEqual(results["pairwise_jaccard"].value, 0.73, places=2)

    def test_empty_outputs_are_excluded(self):
        records = [day02_record({"run_id": "1", "output": ""}, "test"), day02_record({"run_id": "2", "output": "A"}, "test")]
        result = evaluate_consistency(records)["unique_ratio"]
        self.assertEqual(result.denominator, 1)
        self.assertEqual(result.value, 1.0)

    def test_jaccard_empty_edge_cases(self):
        self.assertEqual(jaccard("", ""), 1.0)
        self.assertEqual(jaccard("", "answer"), 0.0)
        self.assertEqual(jaccard("same", "same"), 1.0)
