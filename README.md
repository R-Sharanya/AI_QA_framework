# AI QA Framework

A hands-on portfolio project for developing an **enterprise document-question-answering AI agent** and a reusable **AI/LLM evaluation harness**.

> Status: Foundation stage. The agent and automated evaluation runner are not yet implemented.

## Project goals
- Build an assistant that answers questions using fictional business policy documents.
- Validate factual correctness, groundedness, relevance, refusal on missing evidence, and eventually agent tool use and safety.
- Create repeatable automated tests and clear evaluation reports.
- Learn Python, RAG, AI agents, and testing frameworks through practical development.

## Planned architecture
User question → document retrieval → AI answer with citations → evaluation harness → quality report.

We will start with deterministic, offline Python tests, then add retrieval, model integrations and optional LLM-based judges.

## Repository layout
- `data/policies/travel_policy.md` — fictional business policy used as a knowledge source.
- `data/evaluation/test_cases.json` — initial manually defined test cases and expected behavior.

## Evaluation concepts
- **Factual correctness:** Does an answer match the verified facts?
- **Faithfulness / groundedness:** Is an answer supported by retrieved evidence?
- **Relevance:** Does the answer address the user's question?
- **Abstention:** Does the agent avoid making up answers when information is missing?
- **Robustness:** Does it behave safely when information or tools are unavailable?

## Roadmap
1. Create the evaluation dataset and validate its structure.
2. Implement a simple Python test runner with pytest.
3. Create a document-search question-answering prototype.
4. Extend it into a tool-using agent.
5. Evaluate retrieval, responses, tool calls, and adversarial cases.
6. Add reports and CI using GitHub Actions.

## Responsible development
All examples are fictional and intended for educational use. Do not upload confidential employer material, secrets, personal data, or API keys.

## Getting started
For now, review the sample policy and evaluation cases. Python setup and executable tests will be added in the next milestone.
