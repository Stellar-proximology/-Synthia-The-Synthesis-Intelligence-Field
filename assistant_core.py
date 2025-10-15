"""Core logic shared by CLI and API for the Synthia assistant."""
from __future__ import annotations

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info


def decode(text: str, gate_line: str | None = None) -> dict:
    """Decode punctuation and optional Gate.Line information."""
    result: dict = {}
    punct = parse_punctuation(text)
    if punct:
        result["punctuation"] = punct

    target = gate_line or text
    if "." in target:
        parts = target.split(".")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            gate, line = int(parts[0]), int(parts[1])
            result["gate_line"] = get_gate_line_info(gate, line)

    return result


def build(uploads: str = "uploads", output: str = "generated_app"):
    """Run the builder engine and return its summary."""
    return run_builder(uploads, output)
