# builder_engine.py
import os
import logging
import json
from pathlib import Path

# ── resilient imports: root or parser/ ─────────────────────────
try:
    from spec_extractor import extract_specs
    from layout_organizer import generate_layout
except ModuleNotFoundError:  # fallback to package-style layout
    from parser.spec_extractor import extract_specs
    from parser.layout_organizer import generate_layout

try:
    from jinja2 import Environment, FileSystemLoader
    _HAS_JINJA = True
except Exception:
    _HAS_JINJA = False

# ── logging ────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs", "builder.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SUPPORTED_EXTS = {
    ".txt": "text",
    ".py": "python",
    ".html": "html",
    ".md": "markdown",
    ".json": "json",
}

def _collect_specs(upload_dir: Path):
    """Walk uploads/ and extract specs for supported files."""
    specs = []
    if not upload_dir.exists():
        logging.warning("Upload directory %s not found. Creating it now.", upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        return specs

    for entry in upload_dir.iterdir():
        if not entry.is_file():
            continue
        ftype = SUPPORTED_EXTS.get(entry.suffix.lower())
        if not ftype:
            logging.info("Skipping unsupported file: %s", entry.name)
            continue
        try:
            specs.append(extract_specs(str(entry), ftype))
        except Exception as e:
            logging.exception("Failed to extract specs from %s: %s", entry.name, e)
    return specs

def _render_output(layout: dict, out_dir: Path):
    """Write files to generated_app/ and optionally render index.html via Jinja2."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create folders listed by the generator
    for folder in layout.get("folders", []):
        (out_dir / folder).mkdir(parents=True, exist_ok=True)

    # Write generated files
    for fname, content in (layout.get("files") or {}).items():
        fpath = out_dir / fname
        fpath.parent.mkdir(parents=True, exist_ok=True)
        try:
            with fpath.open("w", encoding="utf-8") as f:
                f.write(content if content is not None else "")
        except Exception as e:
            logging.exception("Failed writing %s: %s", fpath, e)

    # Optional: Jinja template → index.html
    if _HAS_JINJA and Path("templates/index.html.j2").exists():
        try:
            env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("index.html.j2")
            html = template.render(layout=layout)
            with (out_dir / "index.html").open("w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            logging.exception("Jinja render failed: %s", e)
    else:
        # Minimal fallback index.html so there’s always an entry point
        fallback = out_dir / "index.html"
        if not fallback.exists():
            try:
                with fallback.open("w", encoding="utf-8") as f:
                    f.write("""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Generated App</title>
<body style="font-family: system-ui, sans-serif; padding: 24px;">
<h1>Generated App</h1>
<p>This is a fallback index. Add <code>templates/index.html.j2</code> for custom rendering.</p>
<pre id="summary" style="white-space: pre-wrap; background:#f6f6f6; padding:12px; border-radius:8px;"></pre>
<script>
fetch('layout.json').then(r=>r.json()).then(j=>{summary.textContent = JSON.stringify(j, null, 2)})
.catch(()=>{summary.textContent = 'layout.json not found';});
</script>
</body></html>""")
            except Exception as e:
                logging.exception("Failed writing fallback index.html: %s", e)

    # Write JSON snapshot for debugging/preview
    try:
        with (out_dir / "layout.json").open("w", encoding="utf-8") as f:
            json.dump(layout, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.exception("Failed writing layout.json: %s", e)

def run_builder(upload_dir: str = "uploads", generated_dir: str = "generated_app"):
    """Main build runner. Returns a dict summary for CLI wrappers."""
    upload_path = Path(upload_dir)
    out_path = Path(generated_dir)

    try:
        specs = _collect_specs(upload_path)
        if not specs:
            msg = f"No specs found in {upload_path.resolve()}. Place .txt/.py/.html/.md/.json files there."
            logging.warning(msg)
            print(f"⚠️  {msg}")
            # still produce a minimal layout so the pipeline doesn’t die
            layout = {"folders": [], "files": {"README.txt": "No specs found.\nAdd files to uploads/ and re-run."}}
        else:
            layout = generate_layout(specs)

        _render_output(layout, out_path)

        summary = {
            "uploads": str(upload_path.resolve()),
            "output": str(out_path.resolve()),
            "files_written": list((layout.get("files") or {}).keys()),
            "folders_created": list(layout.get("folders") or []),
        }
        logging.info("Builder run complete: %s", summary)
        print(f"✅ Build complete → {summary['output']}")
        return summary

    except Exception as e:
        logging.exception("Builder failed: %s", e)
        print(f"❌ Builder failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    run_builder()