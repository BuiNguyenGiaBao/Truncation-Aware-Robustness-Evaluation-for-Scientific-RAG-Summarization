# Noise-Pool Alignment

The revised manuscript and the current public builder now use the same rule:

> one shared cross-document distractor pool derived from the training split and reused for noisy training, validation, and test construction.

The public implementation is `src/databuildt.py`.

Current context composition:

```text
Clean:                      3 target chunks
Query-aligned additive:     3 target + 2 distractors
Query-distant additive:     3 target + 2 distractors
Query-aligned substitutive: 1 target + 2 distractors
Query-distant substitutive: 1 target + 2 distractors
```

Current similarity bands:

```text
Query-aligned:
  P70-P95
  fallback P60-P98

Query-distant:
  bottom 10%
  fallback bottom 20%
```

## Historical reproducibility note

The exact historical source snapshot of the original data-building script was not retained in a form that proves byte-identical reconstruction of the previously reported Tables 4-8.

Therefore, the repository makes the narrower claim that the current public builder reproduces the manuscript-described data-construction protocol. It does not claim byte-for-byte regeneration of the historical processed JSONL files.
