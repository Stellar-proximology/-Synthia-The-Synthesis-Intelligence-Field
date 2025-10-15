import argparse
import json
import uvicorn
from assistant_core import build as core_build, decode

def handle_oracle(text: str, gate_line: str | None = None) -> None:
    """Decode punctuation and optional Gate.Line information."""
    result = decode(text, gate_line)
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

    server_parser = subparsers.add_parser(
        "server", help="Run the FastAPI server"
    )
    server_parser.add_argument("--host", default="127.0.0.1")
    server_parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()
    if args.command == "oracle":
        handle_oracle(args.text, args.gate_line)
    elif args.command == "build":
        core_build(args.uploads, args.output)
    elif args.command == "server":
        uvicorn.run("assistant_api:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
