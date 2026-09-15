# Dataset Reconstruction

## Source data

Download the Cornell University arXiv Dataset from:

https://www.kaggle.com/datasets/Cornell-University/arxiv

The source corpus is not redistributed here.

## Data usage

The experimental pipeline uses:

- article text for chunking and retrieval;
- abstracts as reference summaries;
- a task-level summarization query for retrieval/noise construction.

The abstract is not used to build the retrieval query.

## Chunking

The reported configuration uses approximately:

```text
chunk size: 150 words
overlap: 30 words
```

Very short chunks are discarded.

## Retrieval and context construction

Clean contexts contain three target-document chunks.

Additive contexts contain:

```text
3 target chunks + 2 cross-document distractors
```

Substitutive contexts contain:

```text
1 target chunk + 2 cross-document distractors
```

Target and distractor chunks are merged and shuffled after construction to reduce fixed-position bias.

Distractors are selected from a cross-document pool derived from the training split. Chunks from the current target document are excluded from the distractor candidates.

The manuscript uses:

```text
query-aligned = higher query-similarity distractors
query-distant = lower query-similarity distractors
```

Legacy artifact names may still use:

```text
easy -> query-aligned
hard -> query-distant
```

These are file-traceability labels only.

## Expected test files

The reconstructed test directory should contain:

```text
test_clean.jsonl
test_noisy_easy_additive.jsonl
test_noisy_hard_additive.jsonl
test_noisy_easy_substitutive.jsonl
test_noisy_hard_substitutive.jsonl
```

Each reported test condition contains 500 matched samples.

## Recommended reconstruction procedure

1. Run the repository's data-building script with seed 42.
2. Confirm that the five evaluation conditions above are generated.
3. Verify that additive contexts contain 3 target + 2 distractor chunks.
4. Verify that substitutive contexts contain 1 target + 2 distractor chunks.
5. Verify that noisy chunks come from a cross-document training-derived pool.
6. Verify that contexts are shuffled after target/noise merging.
7. Record pre-tokenization source lengths before model-specific truncation.

## Important limitation

The original reported runs did not retain token-level target/noise provenance after model-specific truncation. Therefore NER and target-specific TRR cannot be reconstructed retrospectively from the aggregate artifacts alone.

A future instrumented builder should preserve, for every chunk/token:

```text
sample_id
paper_id
chunk_id
source_role: target | noise
context_position
pre_truncation_token_span
post_truncation_retained_span
```

This would enable direct NER/TRR computation.
