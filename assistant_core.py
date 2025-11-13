"""Core logic shared by CLI and API for the Synthia assistant."""
from __future__ import annotations

import os
from typing import Tuple, TYPE_CHECKING

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info

if TYPE_CHECKING:  # pragma: no cover - type checking helper
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

_CHAT_MODEL: "AutoModelForCausalLM | None" = None
_CHAT_TOKENIZER: "AutoTokenizer | None" = None
_CHAT_DEVICE: "torch.device | None" = None


class ChatInitializationError(RuntimeError):
    """Raised when the TinyLlama chat model cannot be prepared."""


def _load_chat_stack() -> Tuple["AutoTokenizer", "AutoModelForCausalLM", "torch.device"]:
    """Load and cache the TinyLlama tokenizer/model stack."""

    global _CHAT_MODEL, _CHAT_TOKENIZER, _CHAT_DEVICE
    if _CHAT_MODEL is not None and _CHAT_TOKENIZER is not None and _CHAT_DEVICE is not None:
        return _CHAT_TOKENIZER, _CHAT_MODEL, _CHAT_DEVICE

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:  # pragma: no cover - environment specific
        raise ChatInitializationError(
            "TinyLlama chat requires the 'torch' and 'transformers' packages."
        ) from exc

    model_path = os.environ.get("TINY_LLAMA_PATH")
    if not model_path:
        raise ChatInitializationError(
            "TINY_LLAMA_PATH is not set. Download the TinyLlama weights and set the"
            " environment variable to their directory."
        )

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


def chat(prompt: str, max_tokens: int = 128) -> str:
    """Generate a TinyLlama response for the provided prompt."""

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
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
