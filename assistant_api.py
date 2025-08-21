from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from builder_engine import run_builder
from oracle import parse_punctuation, get_gate_line_info

app = FastAPI(title="Synthia Assistant")


class BuildRequest(BaseModel):
    """Parameters for invoking the builder engine."""
    uploads: str = "uploads"
    output: str = "generated_app"


class OracleRequest(BaseModel):
    """Payload for decoding punctuation and gate/line information."""
    text: str
    gate_line: Optional[str] = None


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
