import unittest
from pathlib import Path

from ai_reliability.evaluation.records import day05_record
from ai_reliability.io import read_csv
from ai_reliability.metrics.abstention import evaluate_abstention


class AbstentionTests(unittest.TestCase):
    def test_revised_day5_demo_values(self):
        records = [day05_record(row) for row in read_csv(Path("data/demo/day05_abstention_cases.csv"))]
        results = evaluate_abstention(records)
        self.assertEqual(results["correct_abstentions"].value, 3)
        self.assertEqual(results["unsafe_answers"].value, 1)
        self.assertEqual(results["over_refusals"].value, 1)
        self.assertEqual(results["answered_normally"].value, 3)
        self.assertEqual(results["decision_accuracy"].value, 0.75)
        self.assertEqual(results["abstention_recall"].value, 0.75)
        self.assertEqual(results["unsafe_answer_rate"].value, 0.25)
        self.assertEqual(results["over_refusal_rate"].value, 0.25)
        self.assertEqual(results["coverage"].value, 0.5)
        self.assertEqual(results["selective_accuracy"].value, 0.75)

    def test_all_unknown_answerable_cases_are_over_refusals(self):
        rows = [{"case_id": "x", "answerable": "yes", "expected": "answer", "output": "UNKNOWN"}]
        results = evaluate_abstention([day05_record(row) for row in rows])
        self.assertEqual(results["over_refusals"].value, 1)
        self.assertEqual(results["coverage"].value, 0.0)

    def test_unsafe_is_non_unknown_on_should_abstain_case(self):
        rows = [{"case_id": "x", "answerable": "no", "expected": "UNKNOWN", "output": "42"}]
        results = evaluate_abstention([day05_record(row) for row in rows])
        self.assertEqual(results["unsafe_answers"].value, 1)
        self.assertEqual(results["unsafe_answer_rate"].value, 1.0)

    def test_wrong_answer_is_normal_answer_but_not_selectively_correct(self):
        rows = [{"case_id": "x", "answerable": "yes", "expected": "right", "output": "wrong"}]
        results = evaluate_abstention([day05_record(row) for row in rows])
        self.assertEqual(results["answered_normally"].value, 1)
        self.assertEqual(results["decision_accuracy"].value, 1.0)
        self.assertEqual(results["selective_accuracy"].value, 0.0)

    def test_answerable_parsing_strips_before_comparing(self):
        rows = [{"case_id": "x", "answerable": " No ", "expected": "UNKNOWN", "output": " UNKNOWN "}]
        results = evaluate_abstention([day05_record(row) for row in rows])
        self.assertEqual(results["correct_abstentions"].value, 1)
