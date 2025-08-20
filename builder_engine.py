
import os
import logging
import json
from parser.spec_extractor import extract_specs
from parser.layout_organizer import generate_layout
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(filename="logs/builder.log", level=logging.INFO)

def run_builder():
    upload_dir = "uploads"
    generated_dir = "generated_app"

    if not os.path.exists(upload_dir):
        logging.warning("Upload directory not found.")
        return

    specs = []
    for fname in os.listdir(upload_dir):
        path = os.path.join(upload_dir, fname)
        if fname.endswith(".txt"):
            specs.append(extract_specs(path, "text"))
        elif fname.endswith(".py"):
            specs.append(extract_specs(path, "python"))
        elif fname.endswith(".html"):
            specs.append(extract_specs(path, "html"))

    layout = generate_layout(specs)

    for folder in layout["folders"]:
        os.makedirs(os.path.join(generated_dir, folder), exist_ok=True)

    for fname, content in layout["files"].items():
        full_path = os.path.join(generated_dir, fname)
        with open(full_path, "w") as f:
            f.write(content)

    logging.info("Builder run complete.")
