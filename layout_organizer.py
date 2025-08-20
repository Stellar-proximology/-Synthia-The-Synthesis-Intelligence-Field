
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader("universe_builder/templates"))

def generate_layout(specs):
    layout = {
        "folders": [],
        "files": {}
    }

    for spec in specs:
        if spec["type"] == "text":
            module = spec.get("module", "UnknownModule")
            if spec.get("pairs"):
                layout["folders"].append("charts")
                chart_template = env.get_template("chart.html.j2")
                chart_html = chart_template.render(title=module + " Chart", pairs=spec["pairs"])
                layout["files"][f"charts/{module}_chart.html"] = chart_html

                chart_spec = f"{module} chart data:\n" + "\n".join([f"{p[0]}: {p[1]}" for p in spec["pairs"]])
                layout["files"][f"charts/{module}_spec.txt"] = chart_spec

            elif spec.get("intents"):
                layout["folders"].append("store")
                store_template = env.get_template("store.html.j2")
                logic_template = env.get_template("store_logic.py.j2")

                store_html = store_template.render(store_name=module, assignments=spec["intents"])
                logic_py = logic_template.render(store_name=module, assignments=spec["intents"])

                layout["files"][f"store/{module}_store.html"] = store_html
                layout["files"][f"store/{module}_logic.py"] = logic_py

                store_spec = f"{module} bot assignments:\n" + "\n".join(
                    [f"{a['user']} → {a['bot']}: {a['credits']} credits" for a in spec["intents"]]
                )
                layout["files"][f"store/{module}_spec.txt"] = store_spec

        elif spec["type"] == "template":
            layout["folders"].append("custom_html")
            layout["files"][f"custom_html/manual_upload.html"] = spec["content"]

        elif spec["type"] == "code":
            layout["folders"].append("scripts")
            layout["files"][f"scripts/manual_upload.py"] = spec["content"]

    return layout
