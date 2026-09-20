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

    def test_punctuation_only_output_is_not_raw_empty(self):
        records = [
            day02_record({"run_id": "1", "output": "!!!"}, "test"),
            day02_record({"run_id": "2", "output": "!!!"}, "test"),
        ]
        results = evaluate_consistency(records)
        self.assertEqual(results["unique_ratio"].denominator, 2)
        self.assertEqual(results["unique_ratio"].value, 0.5)
        self.assertEqual(results["mode_agreement"].denominator, 2)
        self.assertEqual(results["mode_agreement"].value, 1.0)

    def test_pairwise_jaccard_uses_raw_outputs_before_normalization(self):
        records = [
            day02_record({"run_id": "1", "output": "foo-bar"}, "test"),
            day02_record({"run_id": "2", "output": "foo baz"}, "test"),
        ]
        result = evaluate_consistency(records)["pairwise_jaccard"]
        self.assertEqual(result.denominator, 1)
        self.assertAlmostEqual(result.value, 1 / 3)

    def test_jaccard_empty_edge_cases(self):
        self.assertEqual(jaccard("", ""), 1.0)
        self.assertEqual(jaccard("", "answer"), 0.0)
        self.assertEqual(jaccard("same", "same"), 1.0)
