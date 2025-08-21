"""Simple offline TinyLlama chat assistant.

This script loads a locally stored TinyLlama model and starts an
interactive REPL.  Set the ``TINY_LLAMA_PATH`` environment variable to the
directory containing the model files downloaded from Hugging Face.
No network access or API keys are required.
"""

import os
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    """Run an interactive chat with the TinyLlama model locally."""

    model_path = os.environ.get("TINY_LLAMA_PATH")
    if not model_path:
        print(
            "TINY_LLAMA_PATH is not set.\n"
            "Download the TinyLlama weights from\n"
            "https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0\n"
            "and set TINY_LLAMA_PATH to the directory containing the model files."
        )
        sys.exit(1)

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=dtype, local_files_only=True
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    print("TinyLlama is ready. Press Ctrl+C to exit.")
    try:
        while True:
            prompt = input("You: ")
            if not prompt:
                continue
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            outputs = model.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"TinyLlama: {response}")
    except KeyboardInterrupt:
        print("\nExiting TinyLlama chat.")


if __name__ == "__main__":
    main()
