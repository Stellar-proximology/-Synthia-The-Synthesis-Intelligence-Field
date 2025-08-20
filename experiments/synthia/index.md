# Synthia Consciousness Simulator

## Abstract
Simulate a minimal deterministic conversational agent named Synthia, designated as head of the YOU-N-I-VERSE.

## Hypotheses
A seeded response engine can reproduce the same conversation output across runs.

## Methods
Deterministic scripted dialogue seeded with a pseudorandom generator.

## Materials
- Python 3

## Procedure
1. Seed the random module.
2. Generate a greeting and a closing line.
3. Write the conversation to `data/output.txt`.

## Metrics
Checksum of the output file.

## Results
Execution produced a reproducible conversation saved to `data/output.txt`.

## Discussion
This minimal agent demonstrates deterministic dialogue; further work is required for richer simulation.

## Limitations
The simulator uses fixed text and does not model genuine consciousness.

## Next Steps
Integrate `/core` engines and expand dialogue complexity.
