# Learn the project in small steps

## Lesson 1: Evidence before evaluation
1. Read `data/policies/travel_policy.md`.
2. Run `python -m src.cli "What is the hotel limit?"`.
3. Find `contexts`, `answer`, `mode` and `latency_ms` in the output.
4. Explain: a document is split into sections; retrieval ranks sections; generation uses the selected evidence.
5. Offline mode only quotes retrieved evidence. Ollama mode generates an answer using a real model.

Exercise: change the question to "What is the meal allowance?". Explain why retrieving a related paragraph does not always mean an answer is available.

## Lesson 2: Your first test
Read `tests/test_rag.py`, particularly `test_wrong_amount_fails`.
- Arrange: obtain a response.
- Act: deliberately replace the correct amount.
- Assert: the check must reject it.
Run `python -m pytest tests/test_rag.py -v`.

Exercise: add one synthetic policy section and a matching JSON test case yourself.

## Lesson 3: Understand evaluator limitations
A phrase checker can pass a contradictory answer containing the right words. Citation-ID validation does not prove the cited passage supports the claim. Offline evidence extraction does not demonstrate LLM safety.
Manually label live answers for correctness, faithfulness and completeness. Record your reason and compare with an independent judge before trusting its threshold.

## Lesson 4: Controlled regressions
Run the evaluation with `--output reports/baseline`. Change a policy limit temporarily and rerun with `--output reports/changed`. Inspect both JSON reports, identify the failures, then restore the policy. Dataset expectations must be reviewed when policies intentionally change.

## Next milestones
- API endpoints and contract tests.
- Semantic retrieval and paraphrase evaluation.
- DeepEval judge integration, human calibration and repeat-run comparison.
- Agent tools with confirmation, argument validation and failure recovery.

Do not claim these next milestones as implemented on your resume.
