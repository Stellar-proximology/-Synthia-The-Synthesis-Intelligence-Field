import argparse
import json

import builder_engine
from oracle import parse_punctuation, get_gate_line_info


def handle_decode(text: str) -> None:
    """Decode punctuation or Gate.Line information."""
    punct_results = parse_punctuation(text)
    if punct_results:
        for symbol, meaning in punct_results.items():
            print(f"{symbol} -> {meaning}")
    if '.' in text:
        try:
            gate, line = map(int, text.split('.'))
            info = get_gate_line_info(gate, line)
            print(json.dumps(info, indent=2))
        except ValueError:
            print("Invalid Gate.Line format")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ultimate AI assistant")
    subparsers = parser.add_subparsers(dest="command")

    decode_parser = subparsers.add_parser("decode", help="Decode punctuation or Gate.Line")
    decode_parser.add_argument("text", help="Input text or Gate.Line like 22.3")

    subparsers.add_parser("build", help="Run builder engine")

    args = parser.parse_args()
    if args.command == "decode":
        handle_decode(args.text)
    elif args.command == "build":
        builder_engine.run_builder()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
