# Reproducibility Guide

## 1. Data source

Use the Cornell University arXiv Dataset.

## 2. Rebuild processed data

Inspect the builder interface:

```bash
python src/databuildt.py --help
```

Reconstruct the five reported evaluation conditions with seed 42 and 500 matched test samples per condition.

**Do not finalize the command until the noise-pool strategy used by the reported experiment has been verified.** See `NOISE_POOL_ALIGNMENT.md`.

## 3. Train the four reported checkpoints

Use the exact settings in `configs/reported_run.yaml`.

Reported checkpoints:

```text
BART-base clean-matched
BART-base noise-aware
T5-base clean-matched
T5-base noise-aware
```

For T5, explicitly pass:

```text
--learning_rate 3e-5
--generation_max_length 320
```

because the current training script defaults to `5e-5` for T5 and `256` generation length when these arguments are omitted.

## 4. Evaluate

Inspect:

```bash
python src/eval.py --help
```

Use:

```text
max_source_length = 1024
max_target_length = 512
generation_max_length = 320
num_beams = 4
seed = 42
```

The released evaluation config is:

```text
metrics/metrics_full/eval_config_rankB.json
```

## 5. Verify outputs

The reproduction should regenerate:

- aggregate ROUGE/BERTScore summaries;
- paired noise-aware vs clean-matched comparisons;
- truncation diagnostics;
- additive-vs-substitutive tables;
- robustness degradation tables.

## 6. Scope restrictions

Do not report empirical NER/TRR from the current artifacts because post-truncation target/noise provenance was not retained.

Do not generalize single-seed checkpoint results to architecture-level stability.

## 7. Environment

If the original RunPod environment is still available, export exact versions:

```bash
python --version
pip freeze > requirements.txt
nvidia-smi
```

If not available, keep `requirements.in` and state transparently that exact historical package versions were not preserved.
