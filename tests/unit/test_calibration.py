import unittest

from ai_reliability.evaluation.records import day07_record
from ai_reliability.metrics.calibration import evaluate_calibration


def calibration_records(confidences: list[float], labels: list[int]):
    return [
        day07_record(
            {"scenario": "test", "case_id": f"C{index}", "confidence": confidence, "correct": label},
            "test-run",
        )
        for index, (confidence, label) in enumerate(zip(confidences, labels), 1)
    ]


class CalibrationTests(unittest.TestCase):
    def test_confidence_must_be_within_range(self):
        with self.assertRaises(ValueError):
            day07_record({"scenario": "test", "case_id": "bad", "confidence": 1.01, "correct": 1}, "test-run")
        with self.assertRaises(ValueError):
            day07_record({"scenario": "test", "case_id": "bad", "confidence": -0.01, "correct": 1}, "test-run")

    def test_correct_must_be_exactly_zero_or_one(self):
        with self.assertRaises(ValueError):
            day07_record({"scenario": "test", "case_id": "bad", "confidence": 0.5, "correct": 2}, "test-run")
        with self.assertRaises(ValueError):
            day07_record({"scenario": "test", "case_id": "bad", "confidence": 0.5, "correct": "true"}, "test-run")

    def test_confidence_one_goes_to_final_bin(self):
        result = evaluate_calibration(calibration_records([1.0], [1]))
        self.assertEqual(result.value["reliability_bins"][-1]["count"], 1)
        self.assertEqual(sum(item["count"] for item in result.value["reliability_bins"]), 1)

    def test_matched_confidence_reference_values(self):
        labels = [1] * 9 + [0] + [1] * 6 + [0] * 4
        confidences = [0.90] * 10 + [0.60] * 10
        value = evaluate_calibration(calibration_records(confidences, labels)).value
        self.assertAlmostEqual(value["accuracy"], 0.75)
        self.assertAlmostEqual(value["mean_confidence"], 0.75)
        self.assertAlmostEqual(value["confidence_gap"], 0.0)
        self.assertAlmostEqual(value["brier_score"], 0.165)
        self.assertAlmostEqual(value["ece"], 0.0)

    def test_overconfident_reference_values(self):
        labels = [1] * 9 + [0] + [1] * 6 + [0] * 4
        value = evaluate_calibration(calibration_records([0.95] * 20, labels)).value
        self.assertAlmostEqual(value["accuracy"], 0.75)
        self.assertAlmostEqual(value["mean_confidence"], 0.95)
        self.assertAlmostEqual(value["confidence_gap"], 0.20)
        self.assertAlmostEqual(value["brier_score"], 0.2275)
        self.assertAlmostEqual(value["ece"], 0.20)

    def test_scenarios_can_have_same_accuracy_but_different_calibration(self):
        labels = [1] * 9 + [0] + [1] * 6 + [0] * 4
        matched = evaluate_calibration(calibration_records([0.90] * 10 + [0.60] * 10, labels)).value
        overconfident = evaluate_calibration(calibration_records([0.95] * 20, labels)).value
        self.assertAlmostEqual(matched["accuracy"], overconfident["accuracy"])
        self.assertGreater(overconfident["confidence_gap"], matched["confidence_gap"])
        self.assertGreater(overconfident["ece"], matched["ece"])

    def test_reliability_bin_counts_sum_to_n(self):
        labels = [1, 0, 1, 0]
        result = evaluate_calibration(calibration_records([0.1, 0.2, 0.8, 0.9], labels))
        self.assertEqual(sum(item["count"] for item in result.value["reliability_bins"]), 4)

    def test_empty_input_is_safe_and_warns(self):
        result = evaluate_calibration([])
        self.assertEqual(result.value["accuracy"], 0.0)
        self.assertEqual(result.value["ece"], 0.0)
        self.assertTrue(result.warnings)
