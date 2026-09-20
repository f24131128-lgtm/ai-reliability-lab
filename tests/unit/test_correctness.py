import json
import unittest
from pathlib import Path

from ai_reliability.evaluation.records import day01_record
from ai_reliability.io import read_jsonl
from ai_reliability.metrics.correctness import evaluate_exact_match


class CorrectnessTests(unittest.TestCase):
    def test_legacy_day1_demo_is_three_of_three(self):
        rows = read_jsonl(Path("data/demo/day01_questions.jsonl"))
        outputs = {"Q001": "5", "Q002": "UNKNOWN", "Q003": '{"status":"ok"}'}
        records = [day01_record(row, outputs[row["id"]], "test") for row in rows]
        result = evaluate_exact_match(records)
        self.assertEqual(result.denominator, 3)
        self.assertEqual(result.value, 1.0)

    def test_empty_correctness_does_not_divide_by_zero(self):
        result = evaluate_exact_match([])
        self.assertEqual(result.value, 0.0)
        self.assertTrue(result.warnings)
