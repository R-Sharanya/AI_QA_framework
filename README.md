# AI QA Framework — Knowledge Assistant & RAG Testing

Independent learning and portfolio project by Sharanya. All policies are synthetic.

## What works now
- Section-based document ingestion and BM25 retrieval with source IDs.
- Offline evidence-extraction assistant (no model, no API key).
- Optional real LLM generation through a local Ollama server.
- 12 RAG diagnostic cases, negative evaluator tests, JSON/Markdown reports and offline CI.
- Original rule-based evaluation lessons preserved in `src/evaluator.py` and `tests/test_evaluation.py`.

## Quick start (Python 3.10+)
```bash
git clone https://github.com/R-Sharanya/AI_QA_framework.git
cd AI_QA_framework
git checkout feature/rag-evaluation-assistant
python -m venv .venv
```
Activate on Windows PowerShell: `.venv\Scripts\Activate.ps1`.
Activate on macOS/Linux: `source .venv/bin/activate`.
```bash
python -m pip install -r requirements.txt
python -m pytest
python -m src.cli "What is the hotel accommodation limit?"
python -m src.run_evaluation
```
Reports are written to `reports/evaluation.json` and `reports/evaluation.md`. Exit code 1 means diagnostic checks failed; provider failures are reported as failures.

## Live model mode
Install Ollama separately and download a model suitable for your computer. Start its local server, then set `OLLAMA_MODEL` to the exact installed model name.
PowerShell: `$env:OLLAMA_MODEL="YOUR_INSTALLED_MODEL"`.
macOS/Linux: `export OLLAMA_MODEL="YOUR_INSTALLED_MODEL"`.
```bash
python -m src.cli "What is the hotel accommodation limit?" --mode ollama
python -m src.run_evaluation --mode ollama --repeats 3 --output reports/live
```
This uses `http://localhost:11434/api/chat` by default. Local inference requires adequate hardware and a model download; no paid API is required. `OLLAMA_URL` can override the address. No remote provider is configured by default.

## Architecture
Question → ranked document sections → offline excerpts OR local LLM → response with contexts → evaluation report.
`src/rag.py`: retrieval and generation. `src/run_evaluation.py`: dataset execution and reporting. `data/evaluation/rag_cases.json`: expected sources and phrase checks. `docs/LEARNING_GUIDE.md`: exercises.

## What the report does and does not prove
Retrieval recall checks whether expected source IDs were returned. Phrase checks find literal expected facts. Citation checks validate IDs and expected source presence. These are transparent diagnostics, NOT semantic correctness, groundedness scores or hallucination rates. A fluent paraphrase may fail; a contradictory response may pass. Adversarial cases in offline mode do not demonstrate model resistance to prompt injection.

Live inference must be run separately. The local implementation tests inject a fake generator to verify adapter behavior; they do not certify any live model. No live-model quality results are claimed.

## Roadmap
1. **Implemented:** runnable baseline retrieval, offline assistant, Ollama adapter, deterministic evaluation and CI configuration.
2. **Next:** API testing, semantic evaluation using DeepEval and human calibration, stronger datasets, baseline comparison.
3. **Extension:** simulated IT ticket tools, confirmation and tool-call evaluations.

## Learning and resume use
Start with [Lesson 1](docs/LEARNING_GUIDE.md). You should be able to explain a failed test and add a new case before listing this as hands-on experience. Describe it as an independent project, separate from employment.

## References
- [Ollama API](https://docs.ollama.com/api)
- [DeepEval faithfulness — planned semantic evaluation](https://deepeval.com/docs/metrics-faithfulness)

Never commit secrets, `.env` files or confidential employer documents.
