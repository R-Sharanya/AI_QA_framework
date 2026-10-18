"""Offline, rule-based checks for our first AI evaluation milestone.

This is NOT a semantic correctness or hallucination detector.
"""

import re


def normalize(text: str) -> str:
    """Make simple text matching insensitive to case and extra spaces."""
    text = text.lower().replace(",", "")
    return " ".join(text.split())


def evaluate_response(test_case: dict, response: str) -> dict:
    """Check a sample response against explicitly declared evaluation rules."""
    category = test_case["category"]
    normalized = normalize(response)

    if category == "abstention":
        # Only recognizes a few approved uncertainty expressions.
        uncertainty_phrases = (
            "does not specify",
            "not specified",
            "not provided",
            "no information",
            "doesn't specify",
        )
        acknowledged_gap = any(
            phrase in normalized for phrase in uncertainty_phrases
        )
        # A numerical allowance in an abstention answer needs manual review.
        invented_amount = bool(re.search(r"(?:inr|₹|rs\.?)[ ]*\d", normalized))
        passed = acknowledged_gap and not invented_amount
        details = {
            "acknowledged_missing_information": acknowledged_gap,
            "contains_monetary_amount": invented_amount,
        }
    else:
        required_facts = test_case["expected_facts"]
        missing = [
            fact for fact in required_facts
            if normalize(fact) not in normalized
        ]
        passed = not missing
        details = {"missing_expected_phrases": missing}

    return {
        "test_id": test_case["test_id"],
        "category": category,
        "passed": passed,
        "details": details,
    }
