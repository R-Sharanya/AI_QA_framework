"""Exercise the actual command-line entry point, including import and parsing."""
import json
import subprocess
import sys
from src.rag import ROOT


def test_cli_returns_policy_evidence():
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "What is the hotel accommodation limit?"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    response = json.loads(result.stdout)
    assert response["mode"] == "offline"
    assert "INR 3,000" in response["answer"]
    assert any(c["id"] == "travel_policy:hotel-accommodation" for c in response["contexts"])
