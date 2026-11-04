import json
import pytest
from src.rag import ROOT, ask, retrieve, load_chunks
from src.run_evaluation import check, run

CASES = json.loads((ROOT / "data/evaluation/rag_cases.json").read_text())

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_retrieval_expected_evidence(case):
    result = ask(case["question"])
    assert check(case, result)["passed"]

def test_empty_question_rejected():
    with pytest.raises(ValueError):
        ask("   ")

def test_empty_corpus_abstains():
    assert "does not specify" in ask("hotel", chunks=[])["answer"]

def test_bad_configuration_rejected():
    with pytest.raises(ValueError):
        retrieve("hotel", load_chunks(), 0)
    with pytest.raises(ValueError):
        ask("hotel", mode="pretend")

def test_live_adapter_uses_actual_generator_result():
    def fake(question, evidence):
        assert question == "hotel"
        assert evidence[0]["id"] == "travel_policy:hotel-accommodation"
        return "An intentionally distinctive model answer"
    result = ask("hotel", mode="ollama", generator=fake)
    assert result["answer"] == "An intentionally distinctive model answer"

def test_provider_failure_is_not_a_fake_success():
    def broken(*args):
        raise TimeoutError("provider unavailable")
    with pytest.raises(TimeoutError):
        ask("hotel", mode="ollama", generator=broken)

def test_invalid_citation_fails():
    result = ask(CASES[0]["question"])
    result["answer"] += " [invented:source]"
    assert not check(CASES[0], result)["checks"]["citation_ids_valid"]

def test_wrong_amount_fails():
    result = ask(CASES[0]["question"])
    result["answer"] = result["answer"].replace("3,000", "9,000")
    assert not check(CASES[0], result)["passed"]

def test_report_contains_actual_runs(tmp_path):
    report = run(output=tmp_path, repeats=2)
    assert report["total"] == 24
    assert report["passed"] == 24
    assert json.loads((tmp_path / "evaluation.json").read_text())["mode"] == "offline"
