"""Unified command-line assistant for Synthia.

This tool combines the functionality previously in `synthia_assistant.py` and
`ultimate_assistant.py` into one cohesive interface. It can run the universe builder
or decode punctuation and Gate.Line information from the oracle module.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, Any, Optional

from assistant_core import (
    ChatInitializationError,
    build as core_build,
    chat as core_chat,
    decode as core_decode,
)


def _cmd_build(args: argparse.Namespace) -> None:
    """Run the universe builder through the shared assistant_core facade."""

    try:
        summary = core_build(args.uploads, args.output)
    except Exception as exc:
        print(f"Error running universe builder: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(summary or {}, indent=2))
        return

    if not summary:
        print("Universe builder completed with no summary payload.")
        return

    lines = [
        "Universe builder completed successfully:",
        f"  uploads: {summary.get('uploads', args.uploads)}",
        f"  output: {summary.get('output', args.output)}",
    ]
    files = summary.get("files_written")
    if files:
        lines.append(f"  files_written: {', '.join(files)}")
    folders = summary.get("folders_created")
    if folders:
        lines.append(f"  folders_created: {', '.join(folders)}")

    print("\n".join(lines))


def _cmd_oracle(args: argparse.Namespace) -> None:
    """Decode punctuation or Gate.Line values via assistant_core.decode."""

    result: Dict[str, Any] = {}

    # Handle empty input
    if not args.input or not args.input.strip():
        result["error"] = "Input text cannot be empty."
    else:
        input_text = args.input.strip()

        gate_line = args.gate_line
        if not gate_line and "." in input_text:
            # Try to extract gate.line from input automatically
            parts = input_text.split(".")
            if len(parts) >= 2:
                potential_gate = parts[-2].split()[-1] if parts[-2] else ""
                potential_line = parts[-1].split()[0] if parts[-1] else ""
                if potential_gate.isdigit() and potential_line.isdigit():
                    gate_line = f"{potential_gate}.{potential_line}"

        try:
            result = core_decode(input_text, gate_line)
        except Exception as exc:
            result["error"] = f"Error decoding input: {exc}"

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    output_sections = []

    if "punctuation" in result:
        lines = ["Punctuation decoding:"]
        for symbol, meaning in result["punctuation"].items():
            lines.append(f"  {symbol} -> {meaning}")
        output_sections.append("\n".join(lines))

    if "gate_line" in result:
        lines = ["Gate.Line info:"]
        gate_info = result["gate_line"]
        if isinstance(gate_info, dict):
            for key, value in gate_info.items():
                lines.append(f"  {key}: {value}")
        else:
            lines.append(f"  {gate_info}")
        output_sections.append("\n".join(lines))

    if "error" in result and not output_sections:
        output_sections.append(f"Error: {result['error']}")

    if output_sections:
        print("\n\n".join(output_sections))
    else:
        print("No decoding available for the provided input.")


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""
    parser = argparse.ArgumentParser(
        description="Unified Synthia assistant for consciousness system operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s build                    # Run universe builder
  %(prog)s oracle "Psalm 23:1;"     # Decode punctuation
  %(prog)s oracle "22.3"            # Decode gate.line
  %(prog)s oracle "22.3" --json     # JSON output
  %(prog)s oracle "text" --gate-line "22.3"  # Explicit gate.line
  %(prog)s chat "Hello"             # TinyLlama chat (stdin supported)
        """
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )

    # Build command
    build = subparsers.add_parser(
        "build",
        help="Run the universe builder on the uploads directory"
    )
    build.add_argument(
        "--uploads",
        default="uploads",
        help="Directory containing uploaded specs (default: uploads)",
    )
    build.add_argument(
        "--output",
        default="generated_app",
        help="Directory where the generated app is written (default: generated_app)",
    )
    build.add_argument(
        "--json",
        action="store_true",
        help="Print the builder summary as JSON",
    )
    build.set_defaults(func=_cmd_build)

    # Oracle command
    oracle = subparsers.add_parser(
        "oracle", 
        help="Decode punctuation and Gate.Line information from input text"
    )
    oracle.add_argument(
        "input", 
        help="Input text such as 'Psalm 23:1;' or '22.3'"
    )
    oracle.add_argument(
        "--gate-line", 
        help="Explicit Gate.Line value like '22.3' (overrides auto-detection)"
    )
    oracle.add_argument(
        "--json", 
        action="store_true", 
        help="Output result as JSON instead of human-readable format"
    )
    oracle.set_defaults(func=_cmd_oracle)

    # Chat command
    chat_parser = subparsers.add_parser(
        "chat",
        help="Chat with the TinyLlama model via assistant_core",
    )
    chat_parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt text. If omitted, stdin is read instead.",
    )
    chat_parser.add_argument(
        "--max-tokens",
        type=int,
        default=128,
        help="Maximum number of tokens to generate (default: 128)",
    )
    chat_parser.set_defaults(func=_cmd_chat)

    return parser


def _cmd_chat(args: argparse.Namespace) -> None:
    """Invoke the shared TinyLlama chat orchestrator."""

    prompt = (args.prompt or "").strip()
    if not prompt:
        prompt = sys.stdin.read().strip()

    if not prompt:
        print("Error: provide a prompt argument or pipe input via stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        response = core_chat(prompt, args.max_tokens)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ChatInitializationError as exc:
        print(f"Initialization error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected TinyLlama error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(response)


def main() -> None:
    """Main entry point for the Synthia assistant."""
    try:
        parser = build_parser()
        args = parser.parse_args()
        
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
