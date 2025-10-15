"""Flask API exposing Cynthia's core endpoints.

The routes mirror the minimal API surface described in the mechanics
brief. All handlers call placeholder implementations from
``cynthia.core`` so the server can run without external dependencies.
"""

from __future__ import annotations

from flask import Flask, jsonify, request

from . import core

app = Flask(__name__)


@app.post("/v1/resolve-field")
def resolve_field() -> tuple[str, int]:
    data = request.get_json(force=True)
    ts = data.get("ts", "")
    geo = data.get("geo", {})
    user_profile_id = data.get("user_profile_id", "")
    return jsonify(core.resolve_field(ts, geo, user_profile_id)), 200


@app.post("/v1/infer")
def infer() -> tuple[str, int]:
    data = request.get_json(force=True)
    prompts = data.get("prompts", [])
    candidates = core.orchestrate_nodes(prompts)
    return jsonify({"candidates": candidates}), 200


@app.post("/v1/collapse")
def collapse() -> tuple[str, int]:
    data = request.get_json(force=True)
    candidates = data.get("candidates", [])
    field = data.get("field", {})
    intent = data.get("intent", "")
    constraints = data.get("constraints", {})
    decision = core.collapse(candidates, field, intent, constraints)
    return jsonify(decision), 200


@app.post("/v1/act")
def act() -> tuple[str, int]:
    data = request.get_json(force=True)
    text = data.get("text", "")
    field = data.get("field", {})
    mode = data.get("mode", "Soft")
    processed = core.postprocess(text, field, mode)
    actions = core.route_actions(processed, {"mode": mode})
    return jsonify(actions), 200


@app.post("/v1/memory/upsert")
def memory_upsert() -> tuple[str, int]:
    # Placeholder: a real implementation would persist data here.
    return jsonify({"ok": True}), 200


@app.post("/v1/lab/apply-patch")
def lab_apply_patch() -> tuple[str, int]:
    # Placeholder: builder mode would apply a patch and run tests.
    return jsonify({"ok": True, "tests": []}), 200


if __name__ == "__main__":
    app.run(debug=True)
