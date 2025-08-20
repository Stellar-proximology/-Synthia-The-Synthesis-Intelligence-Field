import argparse
import json
from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info


def handle_oracle(text: str, gate_line: str | None = None) -> None:
    """Decode punctuation and optional Gate.Line information."""
    result = {}

    punct = parse_punctuation(text)
    if punct:
        result["punctuation"] = punct

    target = gate_line or text
    if "." in target:
        parts = target.split(".")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            gate, line = int(parts[0]), int(parts[1])
            result["gate_line"] = get_gate_line_info(gate, line)

    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified interface for builder engine and oracle tools"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    oracle_parser = subparsers.add_parser(
        "oracle", help="Decode punctuation or Gate.Line values"
    )
    oracle_parser.add_argument(
        "text", help="Input text such as 'Psalm 23:1;'"
    )
    oracle_parser.add_argument(
        "--gate-line", help="Explicit Gate.Line value like '22.3'"
    )

    subparsers.add_parser(
        "build", help="Run the builder engine to generate app layout"
    )

    args = parser.parse_args()
    if args.command == "oracle":
        handle_oracle(args.text, args.gate_line)
    elif args.command == "build":
        run_builder()


if __name__ == "__main__":
    main()
