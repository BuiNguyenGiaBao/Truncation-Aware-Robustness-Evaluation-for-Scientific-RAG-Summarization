# Reproducibility Guide

## Goal

Reproduce the reported checkpoint-level proof-of-concept using the exact configuration in:

```text
configs/reported_run.yaml
```

## Step 1 — Prepare source data

Download the Cornell University arXiv Dataset and place it in the location expected by the repository data builder.

Do not redistribute the raw Kaggle dataset unless its license permits it.

## Step 2 — Build processed contexts

Use the existing repository data-construction script.

Before running, inspect its current interface:

```bash
python src/databuildt.py --help
```

Use seed 42 and reconstruct the five matched evaluation conditions described in `DATASET_REPRODUCTION.md`.

## Step 3 — Train four checkpoints

Train:

```text
BART-base clean-matched
BART-base noise-aware
T5-base clean-matched
T5-base noise-aware
```

Common settings:

```text
epochs                 = 1
optimizer              = AdamW (adamw_torch)
learning_rate          = 3e-5
weight_decay           = 0.01
warmup_ratio           = 0.03
max_source_length      = 1024
max_target_length      = 512
generation_max_length  = 320
effective_batch_size   = 16
seed                   = 42
```

BART-base:

```text
per_device_train_batch_size = 8
per_device_eval_batch_size  = 8
gradient_accumulation_steps = 2
```

T5-base:

```text
per_device_train_batch_size = 4
per_device_eval_batch_size  = 4
gradient_accumulation_steps = 4
```

Important: explicitly set T5 learning rate to `3e-5`; do not rely on any architecture-specific default.

## Step 4 — Generation / decoding

Use:

```text
generation_max_length = 320
num_beams             = 4
early_stopping        = True
no_repeat_ngram_size  = 3
```

Before running evaluation, inspect the current script interface:

```bash
python src/eval.py --help
```

## Step 5 — Evaluate

Run evaluation on the same 500 matched samples per condition.

Report:

```text
ROUGE-1
ROUGE-2
ROUGE-L
BERTScore F1
paired bootstrap 95% CI
Holm-corrected paired tests
paired effect size
model-specific truncation rate
```

## Step 6 — Evidence classification

Use the study-specific thresholds:

```text
Primary   <= 5% truncation
Qualified > 5% and <= 50%
Excluded  > 50%
```

These are operational study rules, not universal cutoffs.

## Step 7 — Statistical interpretation

Interpret results only at checkpoint level.

Do not treat paired bootstrap uncertainty across test instances as multi-seed training uncertainty.

## NER/TRR limitation

The reported runs lack post-truncation target/noise token provenance.

Therefore:

```text
NER: not reported empirically
target-specific TRR: not reported empirically
```

Do not substitute overall input-retention ratio for TRR.

## Reproduction checklist

- [ ] Cornell arXiv source dataset downloaded
- [ ] seed fixed to 42
- [ ] 5 evaluation conditions reconstructed
- [ ] 500 matched test samples per condition
- [ ] BART LR = 3e-5
- [ ] T5 LR = 3e-5
- [ ] effective batch size = 16
- [ ] source / target max = 1024 / 512
- [ ] generation max = 320
- [ ] beams = 4
- [ ] early stopping enabled
- [ ] no-repeat 3-gram enabled
- [ ] paired statistics recomputed
- [ ] truncation summary recomputed
- [ ] claims limited to checkpoint-level evidence
