from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from assistant_core import build as core_build, decode

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
    return core_build(req.uploads, req.output)


@app.post("/oracle")
def oracle(req: OracleRequest):
    """Decode punctuation and optionally a specific Gate.Line."""
    return decode(req.text, req.gate_line)
