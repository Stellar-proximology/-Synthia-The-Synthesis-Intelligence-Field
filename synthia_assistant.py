#!/usr/bin/env python3
"""Command-line assistant that combines builder and oracle tools."""

import argparse

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info


def cmd_build(_args: argparse.Namespace) -> None:
    """Run the universe builder to process uploads and generate files."""
    run_builder()
    print("Builder run complete.")


def cmd_decode(args: argparse.Namespace) -> None:
    """Decode punctuation and optional gate.line information."""
    results = parse_punctuation(args.text)
    if results:
        print("Punctuation decoding:")
        for symbol, meaning in results.items():
            print(f"  {symbol} -> {meaning}")
    else:
        print("No punctuation cues detected.")

    if args.gate_line:
        try:
            gate_str, line_str = args.gate_line.split(".")
            gate, line = int(gate_str), int(line_str)
            info = get_gate_line_info(gate, line)
            print("Gate.Line info:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        except ValueError:
            print("Invalid gate.line format; expected 'gate.line'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthia multi-tool assistant")
    subparsers = parser.add_subparsers(dest="command")

    build = subparsers.add_parser("build", help="Run universe builder on uploads")
    build.set_defaults(func=cmd_build)

    decode = subparsers.add_parser("decode", help="Decode punctuation and gate.line")
    decode.add_argument("text", help="Input text to analyse")
    decode.add_argument("--gate-line", help="Gate.line specification like 22.3")
    decode.set_defaults(func=cmd_decode)

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
