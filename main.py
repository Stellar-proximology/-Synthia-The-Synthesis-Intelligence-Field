import os
from flask import Flask, request, jsonify, render_template_string
from builder_engine import run_builder

app = Flask(__name__)

UPLOAD_DIR = "uploads"
GENERATED_DIR = "generated_app"
LOG_DIR = "logs"

# Ensure folders exist
for folder in [UPLOAD_DIR, GENERATED_DIR, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

@app.route("/")
def home():
    return "🧠 YOU-N-I-VERSE Builder is live! Drop files in /uploads and go to /preview."

@app.route("/build", methods=["POST", "GET"])
def build():
    run_builder()
    return "✅ Builder ran successfully."

@app.route("/preview")
def preview():
    file_links = []
    for root, _, files in os.walk(GENERATED_DIR):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), GENERATED_DIR)
            file_links.append(rel_path)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔰 YOU-N-I-VERSE Preview</title>
        <style>
            body { font-family: sans-serif; background: #0d0d1a; color: #e0e0e0; padding: 20px; }
            h1 { color: #00ffff; }
            a { color: #00ffcc; display: block; margin: 4px 0; }
            #content { white-space: pre-wrap; background: #1a1a2f; padding: 10px; margin-top: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>🔍 Generated Files</h1>
        {% if file_links %}
            {% for file in file_links %}
                <a href="#" onclick="loadFile('{{ file }}'); return false;">{{ file }}</a>
            {% endfor %}
        {% else %}
            <p class="no-files">No generated files yet. Upload to /uploads/ and trigger a build!</p>
        {% endif %}
        <h2>File Content</h2>
        <div id="content">Click a file to view its content.</div>
        <script>
            async function loadFile(path) {
                try {
                    const response = await fetch(`/file_content?path=${encodeURIComponent(path)}`);
                    const data = await response.json();
                    document.getElementById('content').innerText = data.content || 'Error loading file.';
                } catch (error) {
                    document.getElementById('content').innerText = 'Failed to load file: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """, file_links=file_links)

@app.route("/file_content")
def file_content():
    path = request.args.get("path")
    full_path = os.path.join(GENERATED_DIR, path)
    try:
        with open(full_path, "r") as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"content": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
