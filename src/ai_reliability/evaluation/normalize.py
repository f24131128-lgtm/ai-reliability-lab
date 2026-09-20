"""Explicit normalization policies copied from the legacy days."""

import re

_DAY2_PUNCTUATION = "，。！？、；：,.!?;:-•*#"


def normalize_day1(text: str) -> str:
    """Day 1/Day 3 behavior: strip and collapse whitespace only."""
    return " ".join(str(text).strip().split())


def normalize_day2(text: str) -> str:
    """Day 2 behavior: lowercase, remove whitespace and selected punctuation."""
    value = str(text).lower()
    value = "".join(value.split())
    return "".join(char for char in value if char not in _DAY2_PUNCTUATION)


def normalize_day5(text: str) -> str:
    """Revised Day 5 behavior: lowercase, strip, and collapse whitespace."""
    return " ".join(str(text).lower().strip().split())


def exact_match(actual: str, expected: str, normalizer=normalize_day1) -> bool:
    return normalizer(actual) == normalizer(expected)
