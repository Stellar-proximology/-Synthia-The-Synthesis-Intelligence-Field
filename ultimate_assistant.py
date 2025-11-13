"""Unified command-line assistant for Synthia.

This tool combines the functionality previously in `synthia_assistant.py` and
`ultimate_assistant.py` into one cohesive interface. It can run the universe builder
or decode punctuation and Gate.Line information from the oracle module.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, Any, Optional, Tuple, TYPE_CHECKING

from assistant_core import ChatInitializationError

if TYPE_CHECKING:  # pragma: no cover - import-time helper
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

try:
    from builder_engine import run_builder
except ImportError:
    print("Warning: builder_engine module not found. 'build' command will not work.", file=sys.stderr)
    run_builder = None

try:
    from oracle import parse_punctuation, get_gate_line_info
except ImportError:
    print("Warning: oracle module not found. 'oracle' command will not work.", file=sys.stderr)
    parse_punctuation = None
    get_gate_line_info = None


def _cmd_build(_args: argparse.Namespace) -> None:
    """Run the universe builder on the current uploads directory."""
    if run_builder is None:
        print("Error: builder_engine module not available.", file=sys.stderr)
        sys.exit(1)
    
    try:
        run_builder()
        print("Universe builder completed successfully.")
    except Exception as e:
        print(f"Error running universe builder: {e}", file=sys.stderr)
        sys.exit(1)


def _cmd_oracle(args: argparse.Namespace) -> None:
    """Decode punctuation or Gate.Line values from input text.

    Results are printed in a human-friendly format or as JSON if --json is provided.
    """
    if parse_punctuation is None or get_gate_line_info is None:
        print("Error: oracle module not available.", file=sys.stderr)
        sys.exit(1)

    result: Dict[str, Any] = {}

    # Handle empty input
    if not args.input or not args.input.strip():
        result["error"] = "Input text cannot be empty."
    else:
        input_text = args.input.strip()
        
        # Punctuation resonance
        try:
            punct = parse_punctuation(input_text)
            if punct:
                result["punctuation"] = punct
        except Exception as e:
            result["punctuation_error"] = f"Error parsing punctuation: {e}"

        # Gate.Line – explicit via flag or inferred from the input string
        gate_line = args.gate_line
        if not gate_line and "." in input_text:
            # Try to extract gate.line from input
            parts = input_text.split(".")
            if len(parts) >= 2:
                # Handle cases like "Gate 22.3" or just "22.3"
                potential_gate = parts[-2].split()[-1] if parts[-2] else ""
                potential_line = parts[-1].split()[0] if parts[-1] else ""
                
                if potential_gate.isdigit() and potential_line.isdigit():
                    gate_line = f"{potential_gate}.{potential_line}"

        if gate_line:
            try:
                parts = gate_line.split(".")
                if len(parts) != 2:
                    result["gate_line_error"] = "Invalid gate.line format; expected 'gate.line' (e.g., '22.3')."
                else:
                    gate_str, line_str = parts[0].strip(), parts[1].strip()
                    if not (gate_str.isdigit() and line_str.isdigit()):
                        result["gate_line_error"] = "Invalid gate.line format; expected numeric values."
                    else:
                        gate, line = int(gate_str), int(line_str)
                        # Validate ranges (assuming Human Design gates 1-64, lines 1-6)
                        if not (1 <= gate <= 64):
                            result["gate_line_error"] = f"Gate {gate} out of range (1-64)."
                        elif not (1 <= line <= 6):
                            result["gate_line_error"] = f"Line {line} out of range (1-6)."
                        else:
                            gate_info = get_gate_line_info(gate, line)
                            if gate_info:
                                result["gate_line"] = gate_info
                            else:
                                result["gate_line_error"] = f"No information found for Gate {gate}.{line}."
            except ValueError as e:
                result["gate_line_error"] = f"Error parsing gate.line: {e}"
            except Exception as e:
                result["gate_line_error"] = f"Error retrieving gate.line info: {e}"

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

    # Print any errors
    errors = []
    for key in ["error", "punctuation_error", "gate_line_error"]:
        if key in result:
            errors.append(f"Error: {result[key]}")
    
    if errors:
        output_sections.extend(errors)

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
        help="Chat with the TinyLlama model using cached weights",
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


_CHAT_MODEL: "AutoModelForCausalLM | None" = None
_CHAT_TOKENIZER: "AutoTokenizer | None" = None
_CHAT_DEVICE: "torch.device | None" = None
_CHAT_LOAD_ERROR: Optional[ChatInitializationError] = None


def _load_chat_stack() -> Tuple["AutoTokenizer", "AutoModelForCausalLM", "torch.device"]:
    """Load and cache the TinyLlama tokenizer/model stack."""

    global _CHAT_MODEL, _CHAT_TOKENIZER, _CHAT_DEVICE, _CHAT_LOAD_ERROR

    if _CHAT_MODEL is not None and _CHAT_TOKENIZER is not None and _CHAT_DEVICE is not None:
        return _CHAT_TOKENIZER, _CHAT_MODEL, _CHAT_DEVICE

    if _CHAT_LOAD_ERROR is not None:
        raise _CHAT_LOAD_ERROR

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:  # pragma: no cover - environment specific
        _CHAT_LOAD_ERROR = ChatInitializationError(
            "TinyLlama chat requires the 'torch' and 'transformers' packages."
        )
        raise _CHAT_LOAD_ERROR from exc

    model_path = os.environ.get("TINY_LLAMA_PATH")
    if not model_path:
        _CHAT_LOAD_ERROR = ChatInitializationError(
            "TINY_LLAMA_PATH is not set. Download the TinyLlama weights and set the "
            "environment variable to their directory."
        )
        raise _CHAT_LOAD_ERROR

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=dtype, local_files_only=True
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    _CHAT_MODEL = model
    _CHAT_TOKENIZER = tokenizer
    _CHAT_DEVICE = device
    return tokenizer, model, device


def handle_chat(prompt: str, max_tokens: int = 128) -> str:
    """Generate a TinyLlama response using cached tokenizer/model objects."""

    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("Prompt cannot be empty.")

    tokenizer, model, device = _load_chat_stack()
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max(1, max_tokens),
        do_sample=True,
        temperature=0.7,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def _cmd_chat(args: argparse.Namespace) -> None:
    """Invoke the shared TinyLlama chat orchestrator."""

    prompt = (args.prompt or "").strip()
    if not prompt:
        prompt = sys.stdin.read().strip()

    if not prompt:
        print("Error: provide a prompt argument or pipe input via stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        response = handle_chat(prompt, args.max_tokens)
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
