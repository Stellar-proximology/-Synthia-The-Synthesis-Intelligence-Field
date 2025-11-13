from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from fastapi.responses import StreamingResponse

from assistant_core import ChatInitializationError, build as core_build, chat as core_chat, decode

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
    return core_build(req.uploads, req.output)


@app.post("/oracle")
def oracle(req: OracleRequest):
    """Decode punctuation and optionally a specific Gate.Line."""
    return decode(req.text, req.gate_line)


@app.post("/chat")
def chat(req: ChatRequest, stream: bool = False):
    """Generate TinyLlama responses that mirror the CLI contract."""

    try:
        response_text = core_chat(req.prompt, req.max_tokens)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ChatInitializationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if stream:
        def token_stream():
            for token in response_text.split():
                yield token + " "

        return StreamingResponse(token_stream(), media_type="text/plain")

    return {"response": response_text}
