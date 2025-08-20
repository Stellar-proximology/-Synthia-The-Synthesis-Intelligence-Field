import argparse
import json
from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info


def handle_oracle(input_str: str) -> None:
    """Decode punctuation and Gate.Line information from the provided input."""
    result = {}
    punct = parse_punctuation(input_str)
    if punct:
        result["punctuation"] = punct
    if "." in input_str:
        parts = input_str.split(".")
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
        "input", help="Input string such as '22.3' or 'Psalm 23:1;'"
    )

    subparsers.add_parser(
        "build", help="Run the builder engine to generate app layout"
    )

    args = parser.parse_args()
    if args.command == "oracle":
        handle_oracle(args.input)
    elif args.command == "build":
        run_builder()


if __name__ == "__main__":
    main()
