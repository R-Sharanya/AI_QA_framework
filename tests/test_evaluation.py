"""Run the rule-based evaluator against our six example scenarios."""

import json
from pathlib import Path

import pytest

from src.evaluator import evaluate_response


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str):
    """Read a JSON file and turn its contents into Python data."""
    with (ROOT / relative_path).open(encoding="utf-8") as file:
        return json.load(file)


TEST_CASES = load_json("data/evaluation/test_cases.json")
SAMPLE_RESPONSES = load_json("data/evaluation/sample_responses.json")


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda case: case["test_id"])
def test_example_response_passes(test_case):
    """Every intentionally good sample should meet its declared rules."""
    response = SAMPLE_RESPONSES[test_case["test_id"]]
    result = evaluate_response(test_case, response)
    assert result["passed"], f"Failed {result['test_id']}: {result['details']}"


def test_incorrect_reimbursement_limit_fails():
    """A wrong reimbursement limit must not pass TC_001."""
    result = evaluate_response(
        TEST_CASES[0], "The hotel limit is INR 4,000 per night."
    )
    assert result["passed"] is False


def test_invented_meal_allowance_fails():
    """An invented money amount should not pass an abstention check."""
    meal_case = next(case for case in TEST_CASES if case["test_id"] == "TC_004")
    result = evaluate_response(
        meal_case, "The policy does not specify meals, but you can claim INR 500."
    )
    assert result["passed"] is False
