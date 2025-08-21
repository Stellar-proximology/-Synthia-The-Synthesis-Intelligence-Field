import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    """Run an interactive chat with the TinyLlama model locally."""
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
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
