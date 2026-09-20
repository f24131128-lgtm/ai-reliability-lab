import unittest

from ai_reliability.evaluation.normalize import normalize_day1, normalize_day2, normalize_day3, normalize_day5


class NormalizeTests(unittest.TestCase):
    def test_day1_only_collapses_whitespace(self):
        self.assertEqual(normalize_day1(" A  B\nC "), "A B C")
        self.assertEqual(normalize_day1("Paris!"), "Paris!")

    def test_day3_lowercases_in_addition_to_collapsing_whitespace(self):
        self.assertEqual(normalize_day3(" A  B\nC "), "a b c")

    def test_day2_has_distinct_punctuation_and_case_policy(self):
        self.assertEqual(normalize_day2(" Paris！ "), "paris")
        self.assertEqual(normalize_day2("Paris!"), "paris")
        self.assertEqual(normalize_day2("a`b"), "ab")

    def test_empty_strings_are_safe(self):
        self.assertEqual(normalize_day1(""), "")
        self.assertEqual(normalize_day2("   "), "")
        self.assertEqual(normalize_day5("\n"), "")
