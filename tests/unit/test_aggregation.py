import unittest
from pathlib import Path

from ai_reliability.evaluation.records import day03_record
from ai_reliability.io import read_csv
from ai_reliability.metrics.aggregation import evaluate_reliability_matrix, quadrant
from ai_reliability.schemas import EvaluationRecord


class AggregationTests(unittest.TestCase):
    def test_legacy_day3_matrix_and_macro_average(self):
        records = [day03_record(row) for row in read_csv(Path("data/demo/day03_results.csv"))]
        result = evaluate_reliability_matrix(records)
        self.assertEqual(result.value["mean_accuracy"], 0.6)
        self.assertEqual(result.value["mean_consistency"], 0.85)
        self.assertEqual([row["quadrant"] for row in result.per_case], ["又準又穩", "又準又穩", "穩但不準", "又不準又不穩"])

    def test_threshold_is_inclusive(self):
        self.assertEqual(quadrant(0.8, 0.8, 0.8), "又準又穩")

    def test_group_uses_first_expected_value_for_all_rows(self):
        records = [
            EvaluationRecord(case_id="QX", question_id="QX", response="Answer", expected_answer="Answer"),
            EvaluationRecord(case_id="QX", question_id="QX", response="Answer", expected_answer="Different"),
        ]
        result = evaluate_reliability_matrix(records)
        self.assertEqual(result.per_case[0]["accuracy"], 1.0)
        self.assertEqual(result.value["mean_accuracy"], 1.0)
