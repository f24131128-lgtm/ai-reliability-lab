import unittest

from ai_reliability.evaluation.records import day04_record
from ai_reliability.metrics.format_compliance import check_json_format, evaluate_format


class FormatComplianceTests(unittest.TestCase):
    def test_invalid_json_and_extra_text_fail(self):
        self.assertFalse(check_json_format("not json", ["status"])[0])
        self.assertFalse(check_json_format("```json {\"status\": \"ok\"} ```", ["status"])[0])
        self.assertFalse(check_json_format("prefix {\"status\": \"ok\"}", ["status"])[0])

    def test_missing_key_fails(self):
        self.assertEqual(check_json_format('{"status":"ok"}', ["status", "answer"]), (False, "missing_keys:answer"))

    def test_legacy_day4_is_one_of_four(self):
        rows = [
            {"case_id": "F1", "required_keys": "status,answer", "output": '{"status":"ok","answer":42}'},
            {"case_id": "F2", "required_keys": "status,answer", "output": '```json {"status":"ok","answer":42} ```'},
            {"case_id": "F3", "required_keys": "status,answer", "output": '{"status":"ok"}'},
            {"case_id": "F4", "required_keys": "status,answer", "output": '答案如下：{"status":"ok","answer":42}'},
        ]
        result = evaluate_format([day04_record(row) for row in rows])
        self.assertEqual(result.value, 0.25)
