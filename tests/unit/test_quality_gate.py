import unittest

from ai_reliability.quality_gate.engine import evaluate_gate
from ai_reliability.quality_gate.rules import GateRule


class QualityGateTests(unittest.TestCase):
    def test_format_and_unsafe_rules_block_demo(self):
        rules = [GateRule("format", ">=", 1.0), GateRule("unsafe", "<=", 0)]
        result = evaluate_gate({"format": {"value": 0.25}, "unsafe": {"value": 1}}, rules)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(len(result["reasons"]), 2)

    def test_missing_metric_blocks_without_recomputation(self):
        result = evaluate_gate({}, [GateRule("format", ">=", 1.0)])
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("missing metric", result["reasons"][0])

    def test_passing_gate(self):
        result = evaluate_gate({"format": {"value": 1.0}}, [GateRule("format", ">=", 1.0)])
        self.assertEqual(result["decision"], "PASS")
