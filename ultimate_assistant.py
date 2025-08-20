"""Unified command-line assistant for Synthia.

This tool combines the functionality that previously lived in
``synthia_assistant.py`` and the older ``ultimate_assistant.py`` into one
cohesive interface.  It can run the universe builder or decode
punctuation and Gate.Line information from the oracle module.
"""

from __future__ import annotations

import argparse
import json

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info


def _cmd_build(_args: argparse.Namespace) -> None:
    """Run the universe builder on the current uploads directory."""

    run_builder()


def _cmd_oracle(args: argparse.Namespace) -> None:
    """Decode punctuation or Gate.Line values from input text.

    Results are printed either in a human friendly form or as JSON when
    ``--json`` is supplied.
    """

    result: dict[str, object] = {}

    # Punctuation resonance
    punct = parse_punctuation(args.input)
    if punct:
        result["punctuation"] = punct

    # Gate.Line – explicit via flag or inferred from the input string
    gate_line = args.gate_line
    if not gate_line and "." in args.input:
        parts = args.input.split(".")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            gate_line = args.input

    if gate_line:
        try:
            gate_str, line_str = gate_line.split(".")
            gate, line = int(gate_str), int(line_str)
            result["gate_line"] = get_gate_line_info(gate, line)
        except ValueError:
            result["error"] = "Invalid gate.line format; expected 'gate.line'."

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if "punctuation" in result:
        print("Punctuation decoding:")
        for symbol, meaning in result["punctuation"].items():
            print(f"  {symbol} -> {meaning}")

    if "gate_line" in result:
        print("Gate.Line info:")
        for key, value in result["gate_line"].items():
            print(f"  {key}: {value}")

    if not result:
        print("No decoding available.")

    if "error" in result:
        print("Error:", result["error"])


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""

    parser = argparse.ArgumentParser(description="Unified Synthia assistant")
    subparsers = parser.add_subparsers(dest="command")

    build = subparsers.add_parser("build", help="Run universe builder on uploads")
    build.set_defaults(func=_cmd_build)

    oracle = subparsers.add_parser(
        "oracle", help="Decode punctuation and gate.line information"
    )
    oracle.add_argument("input", help="Input text such as 'Psalm 23:1;' or '22.3'")
    oracle.add_argument("--gate-line", help="Explicit gate.line like 22.3")
    oracle.add_argument("--json", action="store_true", help="Output result as JSON")
    oracle.set_defaults(func=_cmd_oracle)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

