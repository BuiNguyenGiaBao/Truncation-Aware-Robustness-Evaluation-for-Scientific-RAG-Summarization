# Dataset Reconstruction

## Source

Cornell University arXiv Dataset.

## Reported context composition

```text
Clean:                     3 target chunks
Query-aligned additive:    3 target + 2 noise
Query-distant additive:    3 target + 2 noise
Query-aligned substitutive: 1 target + 2 noise
Query-distant substitutive: 1 target + 2 noise
```

## Chunking

Reported fallback chunking:

```text
maximum chunk size: approximately 150 words
overlap: 30 words
very short chunks discarded
```

## Test files

```text
test_clean.jsonl
test_noisy_easy_additive.jsonl
test_noisy_hard_additive.jsonl
test_noisy_easy_substitutive.jsonl
test_noisy_hard_substitutive.jsonl
```

Each reported test condition contains 500 matched samples.

## Required validation checks

After rebuilding data, verify:

- exactly five reported test conditions exist;
- additive contexts contain 3 target + 2 distractors;
- substitutive contexts contain 1 target + 2 distractors;
- target/noise chunks are shuffled after merging;
- distractors are cross-document;
- seed is 42;
- the selected noise-pool strategy matches the manuscript.

## Important provenance limitation

The current aggregate artifacts do not preserve post-truncation target/noise token provenance. This prevents retrospective empirical NER/TRR calculation.
