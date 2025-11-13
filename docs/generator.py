#!/usr/bin/env python3
"""Generate a consolidated architecture reference for the Synthia stack."""

from __future__  import annotations

import json
import textwrap
from importlib import util
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
ORACLE_PATH = ROOT / "oracle.py"
NINE_BODY_PATH = ROOT / "metadata" / "nine_body_modules.json"
OUTPUT_PATH = ROOT / "docs" / "architecture.md"

MODULE_HINTS: Dict[str, Dict[str, List[str]]] = {
    "Cynthia.py": {
        "inputs": [
            "Conversation envelope produced by `cynthia.core.tick`",
            "Resolved Nine-Body fields",
            "Permission constraints"
        ],
        "extensions": [
            "Swap orchestration engines without changing downstream API",
            "Inject mirrored agents from YOU-N-I or Synthai as subprocesses"
        ]
    },
    "FieldRouter.py": {
        "inputs": [
            "Timestamp, geo, and user profile IDs",
            "Resonance deltas pushed from trackers"
        ],
        "extensions": [
            "Add new body definitions by editing metadata/nine_body_modules.json",
            "Expose experimental routers under `field_plugins/`"
        ]
    },
    "SynthesisEngine.py": {
        "inputs": [
            "Candidate responses from orchestrate_nodes",
            "Cross-field confidence vectors"
        ],
        "extensions": [
            "Chain external YOU-N-I mentor models via plugin registry",
            "Define new blending rules inside `docs/architecture.md`"
        ]
    },
    "ResonanceTracker.py": {
        "inputs": [
            "Gate + line activations coming from oracle",
            "Body/Mind/Heart telemetry"
        ],
        "extensions": [
            "Persist historical resonance into analytics warehouse",
            "Publish charts to `generated_app/` via builder"
        ]
    },
    "ToroidalLoop.py": {
        "inputs": [
            "Coherence scores",
            "Action history"
        ],
        "extensions": [
            "Swap adaptive algorithms without disturbing higher layers",
            "Link Synthai adaptive playbooks via git submodule"
        ]
    },
    "PermissionGuardian.py": {
        "inputs": [
            "ResonanceTracker risk flags",
            "Shadow field advisories"
        ],
        "extensions": [
            "Route sovereign policies from YOU-N-I archives",
            "Expose `policies/` directory for overrides"
        ]
    },
    "generate_field_report.py": {
        "inputs": [
            "Nine-Body metadata",
            "Oracle scripture references"
        ],
        "extensions": [
            "Render exports into generated_app charts",
            "Attach store generators for marketplace style delivery"
        ]
    },
    "field_chart.json": {
        "inputs": [
            "User provided birth data",
            "Synced resonance stats"
        ],
        "extensions": [
            "Treat as interchange format with sibling repos",
            "Version via git-lfs when storing sensitive seeds"
        ]
    }
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing dependency: {path}")
    return path.read_text(encoding="utf-8")


def extract_mission_section(readme_text: str) -> str:
    preface = readme_text.split("---", 1)[0].strip()
    return preface


def parse_core_table(readme_text: str) -> List[Dict[str, str]]:
    modules: List[Dict[str, str]] = []
    for line in readme_text.splitlines():
        line = line.strip()
        if not (line.startswith("|") and "`" in line):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2 or "`" not in parts[0]:
            continue
        file_name = parts[0].strip("`")
        description = parts[1]
        modules.append({"file": file_name, "description": description})
    return modules


def load_nine_body_metadata() -> List[Dict[str, object]]:
    return json.loads(NINE_BODY_PATH.read_text(encoding="utf-8"))


def load_oracle_metadata() -> Dict[str, Dict]:
    spec = util.spec_from_file_location("synthia_oracle", ORACLE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to import oracle module")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return {
        "punctuation": getattr(module, "punctuation_resonance", {}),
        "gate_scriptures": getattr(module, "gate_scripture_map", {}),
        "line_phases": getattr(module, "line_genesis_phases", {}),
        "gate_meanings": getattr(module, "gate_meaning_map", {}),
        "line_meanings": getattr(module, "line_meaning_map", {}),
        "field_affinity": getattr(module, "gate_field_affinity_map", {})
    }


def format_list(items: List[str]) -> str:
    return "\n".join([f"- {item}" for item in items]) if items else "- _Not documented_"


def build_core_section(modules: List[Dict[str, str]]) -> str:
    chunks = ["## Core Files & Subsystems"]
    for module in modules:
        file_name = module["file"]
        desc = module["description"]
        hints = MODULE_HINTS.get(file_name, {})
        inputs = format_list(hints.get("inputs", ["Refer to README for context."]))
        extensions = format_list(hints.get("extensions", ["Document customizations inside docs/architecture.md before shipping."]))
        chunks.append(textwrap.dedent(f"""
        ### `{file_name}`
        **Role:** {desc}

        **Expected inputs**
        {inputs}

        **Extension points**
        {extensions}
        """))
    return "\n".join(chunks)


def build_nine_body_section(body_metadata: List[Dict[str, object]]) -> str:
    chunks = ["## Nine-Body Module Matrix"]
    for entry in body_metadata:
        name = entry.get("name", "Unknown Module")
        focus = entry.get("focus", "")
        exp_inputs = format_list(entry.get("expected_inputs", []))
        outputs = format_list(entry.get("primary_outputs", []))
        ext_points = format_list(entry.get("extension_points", []))
        related_files = format_list(entry.get("related_files", []))
        chunks.append(textwrap.dedent(f"""
        ### {name}
        {focus}

        **Expected inputs**
        {exp_inputs}

        **Primary outputs**
        {outputs}

        **Extension points**
        {ext_points}

        **Related files**
        {related_files}
        """))
    return "\n".join(chunks)


def build_oracle_section(oracle_data: Dict[str, Dict]) -> str:
    lines = ["## Oracle & Resonance Gates"]
    punct_rows = "\n".join(
        [f"- `{symbol}` → {meaning}" for symbol, meaning in oracle_data.get("punctuation", {}).items()]
    ) or "- No punctuation data"
    lines.append("### Punctuation Resonance\n" + punct_rows)

    gate_lines = []
    for gate, scriptures in sorted(oracle_data.get("gate_scriptures", {}).items()):
        meaning = oracle_data.get("gate_meanings", {}).get(gate, "Unknown")
        affinity = oracle_data.get("field_affinity", {}).get(gate, "Unknown field")
        gate_lines.append(textwrap.dedent(f"""
        - **Gate {gate}** ({meaning})
          - Field affinity: {affinity}
          - Scriptures: {', '.join(scriptures) if scriptures else 'Not mapped'}
        """))
    if gate_lines:
        lines.append("### Gate Scriptures & Field Affinity\n" + "\n".join(gate_lines))

    phase_lines = []
    for line, phase in sorted(oracle_data.get("line_phases", {}).items()):
        meaning = oracle_data.get("line_meanings", {}).get(line, "Unknown")
        phase_lines.append(f"- Line {line}: {phase} — {meaning}")
    if phase_lines:
        lines.append("### Line Genesis Phases\n" + "\n".join(phase_lines))

    lines.append(textwrap.dedent("""
    Use these resonance anchors when designing charts or stores. The builder spec in
    `uploads/architecture.txt` converts the most active gates into chart-ready data.
    """))
    return "\n\n".join(lines)


def build_external_section() -> str:
    return textwrap.dedent("""
    ## External Repositories & Federation Agreements
    - **YOU-N-I repos** (see `YOU-N-I-VERSE_HybridRepo.zip`, `YOU-N-I-VERSE_Cynthia_Integrated.zip`):
      keep a git submodule or hyperlink in docs/architecture.md whenever you mirror quests,
      ritual decks, or verse assets. Align imports with the Nine-Body matrix above.
    - **Synthai bundles** (`SynthaiOS.zip`, `SynthaiMind (1).zip`, etc.): attach via
      git submodules if you need live code, or cite the archive path in this document when
      copying utilities. Use the Heart/Body extension points for empathy or kinetic models.
    - **YOU-N-I / Synthai interoperability:** treat `docs/architecture.md` as the source of
      truth for contract boundaries. Every imported component must reference the section that
      explains its host body and extension hooks.
    """)


def build_footer() -> str:
    return textwrap.dedent("""
    ---
    _Generated by `docs/generator.py`. Re-run after updating README.md, oracle.py, or
    metadata/nine_body_modules.json. When adding new subsystems, update the metadata so the
    builder and sibling repositories stay synchronized._
    """)


def main() -> None:
    readme_text = read_text(README_PATH)
    mission = extract_mission_section(readme_text)
    modules = parse_core_table(readme_text)
    body_meta = load_nine_body_metadata()
    oracle_data = load_oracle_metadata()

    doc_sections = [
        "# Synthia Architecture Reference",
        textwrap.dedent("""
        This document unifies the public README summary, Nine-Body metadata, and oracle
        resonance tables into a single, living architecture spec. Treat it as the contract
        when composing new assistants or importing sibling repositories.
        """),
        "## Mission Snapshot\n" + mission,
        build_core_section(modules),
        build_nine_body_section(body_meta),
        build_oracle_section(oracle_data),
        build_external_section(),
        textwrap.dedent("""
        ## Builder + Generated App Alignment
        - `docs/architecture.md` feeds the chart/store generator through
          `uploads/architecture.txt`.
        - `python ultimate_assistant.py build` emits resonance charts and module stores
          under `generated_app/` without manual wiring.
        - Always hyperlink back to this file whenever components are mirrored from
          YOU-N-I, Synthai, or other sibling universes.
        """),
        build_footer(),
    ]

    OUTPUT_PATH.write_text("\n\n".join(section.strip() for section in doc_sections if section), encoding="utf-8")
    print(f"Wrote architecture guide to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
