# Dataset Reconstruction

## Starting point

Use a local HuggingFace Dataset/DatasetDict with:

```text
train / validation / test
article / abstract
```

See `SOURCE_DATA_PREPARATION.md`.

## Reported context composition

```text
Clean:                      3 target chunks
Query-aligned additive:     3 target + 2 distractors
Query-distant additive:     3 target + 2 distractors
Query-aligned substitutive: 1 target + 2 distractors
Query-distant substitutive: 1 target + 2 distractors
```

## Chunking

```text
maximum chunk size: approximately 150 words
overlap: 30 words
very short chunks discarded
```

## Noise pool

The manuscript-aligned builder uses one cross-document distractor pool derived from the training split and reuses that source for noisy train/validation/test construction.

## Similarity bands

```text
Query-aligned:
  P70-P95
  fallback P60-P98

Query-distant:
  bottom 10%
  fallback bottom 20%
```

## Test files

```text
test_clean.jsonl
test_noisy_easy_additive.jsonl
test_noisy_hard_additive.jsonl
test_noisy_easy_substitutive.jsonl
test_noisy_hard_substitutive.jsonl
```

The reported evaluation uses 500 matched samples per condition.

## Required checks

Verify that:
- all five conditions exist;
- matched paper IDs are retained across conditions;
- additive = 3 target + 2 distractors;
- substitutive = 1 target + 2 distractors;
- target/noise chunks are shuffled after merging;
- distractors are cross-document;
- seed = 42;
- `dataset_build_manifest.json` records the build settings.

## Provenance limitation

The retained historical artifacts do not preserve post-truncation token-level target/noise provenance, so empirical NER and target-specific TRR cannot be reconstructed retrospectively.
