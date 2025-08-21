import argparse
import json
from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info

try:  # Lazy import so non-chat commands work without transformers installed
    from transformers import AutoModelForCausalLM, AutoTokenizer
except Exception:  # pragma: no cover - optional dependency
    AutoModelForCausalLM = AutoTokenizer = None


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


def handle_chat(prompt: str, max_tokens: int = 128) -> None:
    """Generate a TinyLlama response for the provided prompt."""
    if AutoModelForCausalLM is None or AutoTokenizer is None:
        raise ImportError("transformers is required for the chat command")

    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


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

    build_parser = subparsers.add_parser(
        "build", help="Run the builder engine to generate app layout"
    )
    build_parser.add_argument(
        "--uploads", default="uploads", help="Directory with spec files"
    )
    build_parser.add_argument(
        "--output", default="generated_app", help="Directory for generated app"
    )

    chat_parser = subparsers.add_parser(
        "chat", help="Chat with a local TinyLlama model"
    )
    chat_parser.add_argument("prompt", help="Prompt text for the model")
    chat_parser.add_argument(
        "--max-tokens", type=int, default=128, help="Maximum new tokens to generate"
    )

    args = parser.parse_args()
    if args.command == "oracle":
        handle_oracle(args.text, args.gate_line)
    elif args.command == "build":
        run_builder(args.uploads, args.output)
    elif args.command == "chat":
        handle_chat(args.prompt, args.max_tokens)


if __name__ == "__main__":
    main()
