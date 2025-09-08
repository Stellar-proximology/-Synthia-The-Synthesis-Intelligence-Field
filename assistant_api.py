from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info

try:  # Lazy import so non-chat routes work without transformers installed
    from transformers import AutoModelForCausalLM, AutoTokenizer
except Exception:  # pragma: no cover - optional dependency
    AutoModelForCausalLM = AutoTokenizer = None

_model = _tokenizer = None

app = FastAPI(title="Synthia Assistant")


class BuildRequest(BaseModel):
    """Parameters for invoking the builder engine."""
    uploads: str = "uploads"
    output: str = "generated_app"


class OracleRequest(BaseModel):
    """Payload for decoding punctuation and gate/line information."""
    text: str
    gate_line: Optional[str] = None


class ChatRequest(BaseModel):
    """Input for generating a TinyLlama response."""
    prompt: str
    max_tokens: int = 128


@app.post("/build")
def build(req: BuildRequest):
    """Run the builder engine on the provided directories."""
    return run_builder(req.uploads, req.output)


@app.post("/oracle")
def oracle(req: OracleRequest):
    """Decode punctuation and optionally a specific Gate.Line."""
    result = {}
    punct = parse_punctuation(req.text)
    if punct:
        result["punctuation"] = punct

    target = req.gate_line or req.text
    if "." in target:
        parts = target.split(".")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            result["gate_line"] = get_gate_line_info(int(parts[0]), int(parts[1]))

    return result


def _get_model():
    """Load TinyLlama model/tokenizer on first use."""
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        if AutoModelForCausalLM is None or AutoTokenizer is None:
            raise ImportError("transformers is required for the chat endpoint")
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForCausalLM.from_pretrained(model_name)
    return _model, _tokenizer


@app.post("/chat")
def chat(req: ChatRequest):
    """Generate a response from the local TinyLlama model."""
    model, tokenizer = _get_model()
    inputs = tokenizer(req.prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=req.max_tokens)
    return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}
