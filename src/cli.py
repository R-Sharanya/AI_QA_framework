"""Command-line entry point for the policy assistant."""
import argparse
import json
from src.rag import ask

def main():
    p = argparse.ArgumentParser(description="Policy assistant: offline evidence or local LLM")
    p.add_argument("question")
    p.add_argument("--mode", choices=["offline", "ollama"], default="offline")
    p.add_argument("--top-k", type=int, default=2)
    args = p.parse_args()
    try:
        print(json.dumps(ask(args.question, args.mode, args.top_k), indent=2))
    except Exception as error:
        p.exit(2, f"Assistant failed: {error}\n")
if __name__ == "__main__":
    main()
