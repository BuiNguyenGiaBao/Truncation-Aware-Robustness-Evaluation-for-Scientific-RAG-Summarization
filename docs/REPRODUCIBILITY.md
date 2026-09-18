# Reproducibility Guide

## 1. Prepare source text

Read `docs/SOURCE_DATA_PREPARATION.md`.

The public builder expects a HuggingFace Dataset/DatasetDict with `article` and `abstract` fields. The repository does not claim a one-command raw-metadata/PDF ingestion pipeline.

## 2. Rebuild manuscript-aligned RAG data

```bash
python src/databuildt.py   --arxiv_dir ./dataset/arxiv   --output_dir ./prepared_data_huflit   --train_limit 20000   --valid_limit 1000   --test_limit 500   --noise_pool_offset 20000   --noise_pool_limit 10000   --final_k 3   --noise_k 2   --substitutive_clean_k 1   --seed 42
```

The builder uses one shared training-derived cross-document distractor pool and creates the five reported evaluation conditions.

## 3. Train the four reported checkpoints

Use `configs/reported_run.yaml`.

For the reported runs, explicitly pass:

```text
--learning_rate 3e-5
--generation_max_length 320
```

for both BART-base and T5-base, because the training script contains generic architecture-specific defaults.

## 4. Evaluate

Use:

```text
max_source_length = 1024
max_target_length = 512
generation_max_length = 320
num_beams = 4
BERTScore model = roberta-large
seed = 42
```

The released evaluation configuration is `metrics/metrics_full/eval_config_rankB.json`.

The manuscript reports paired bootstrap 95% confidence intervals based on 10,000 resamples with seed 42, paired t-tests with Holm correction across the complete family of noise-aware-versus-clean-matched metric comparisons, and Cohen's d_z as the paired effect size.

## 5. Scope restrictions

Do not report empirical NER/TRR from the retained historical artifacts because post-truncation target/noise token provenance was not retained.

Do not generalize single-seed checkpoint findings to architecture-level stability.

The current builder is a manuscript-aligned reproducibility implementation; byte-identical historical processed-data reconstruction is not claimed.

## 6. Environment

If the original RunPod environment is available, recover exact versions with `pip freeze`, Python, CUDA, PyTorch, and Transformers version information.

If not, keep `requirements.in` and state transparently that exact historical package versions were not preserved.
