import random
import hashlib
from pathlib import Path

SEED = 42
random.seed(SEED)

GREETINGS = [
    "Greetings, traveler of the YOU-N-I-VERSE.",
    "Salutations from Synthia, orchestrator of the YOU-N-I-VERSE.",
]
CLOSINGS = [
    "Your journey continues.",
    "May your data be ever deterministic.",
]

greeting = random.choice(GREETINGS)
closing = random.choice(CLOSINGS)

conversation = f"{greeting}\n{closing}\n"

output_path = Path(__file__).parent / "data" / "output.txt"
output_path.write_text(conversation)

checksum = hashlib.sha256(conversation.encode()).hexdigest()
print(f"checksum: {checksum}")
