
import re
from typing import Iterable, Union

EncodingSelector = Union[str, Iterable[str]]


def _read_file_with_encodings(file_path, encodings: EncodingSelector) -> str:
    if isinstance(encodings, str):
        encodings_to_try = [encodings]
    else:
        encodings_to_try = list(encodings)

    if not encodings_to_try:
        raise ValueError("At least one encoding must be provided")

    last_error = None
    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError as exc:
            last_error = exc

    raise last_error or UnicodeDecodeError(
        "", b"", 0, 0, "Unable to decode file with provided encodings"
    )


def extract_specs(file_path, file_type, encodings: EncodingSelector = "utf-8"):
    content = _read_file_with_encodings(file_path, encodings)

    if file_type == "text":
        return extract_from_text(content)
    elif file_type == "python":
        return {"type": "code", "language": "python", "content": content}
    elif file_type == "html":
        return {"type": "template", "language": "html", "content": content}
    else:
        return {"type": "unknown", "content": content}

def extract_from_text(text):
    lines = text.splitlines()
    module = None
    pairs = []
    intents = []
    for line in lines:
        if "Module:" in line:
            module = line.split("Module:")[1].strip()
        elif "-" in line and "at" in line:
            match = re.match(r"(.+?) at ([0-9.]+)", line.strip())
            if match:
                label = match.group(1).strip()
                value = float(match.group(2).strip())
                pairs.append((label, value))
        elif "assigns" in line and "credits" in line:
            match = re.match(r"(\w+) assigns (\w+) with ([0-9]+) credits", line.strip())
            if match:
                user, bot, credits = match.groups()
                intents.append({"user": user, "bot": bot, "credits": int(credits)})

    return {
        "type": "text",
        "module": module,
        "pairs": pairs,
        "intents": intents,
        "raw": text
    }
