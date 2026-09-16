# Truncation-Aware Robustness Evaluation for Scientific RAG Summarization

**Truncation-Aware Robustness Evaluation for Scientific RAG Summarization:  
A Proof-of-Concept Study with BART and T5**

Authors: **Bui Nguyen Gia Bao, Le Nhat Tung**

## Overview

This repository contains the code and evaluation artifacts supporting the HUFLIT manuscript.

The study presents a **checkpoint-level proof-of-concept** for truncation-aware robustness evaluation in scientific RAG summarization. It does not claim multi-seed architecture-level generalization or complete empirical validation of all proposed diagnostics.

The repository supports reproducibility of:

- source-data preparation;
- section-aware chunking;
- dense retrieval and MMR selection;
- controlled retrieval-noise construction;
- clean, additive, and substitutive evaluation conditions;
- BART-base and T5-base training;
- generation and evaluation;
- truncation diagnostics;
- paired statistical analysis.

---

## Source Dataset

The experiments use the **Cornell University arXiv Dataset**:

https://www.kaggle.com/datasets/Cornell-University/arxiv

Article text is used for chunking and retrieval, while abstracts are used as reference summaries.

The abstract is not used to construct the retrieval query.

---

## Data Construction

The current reproducibility pipeline uses a **shared cross-document distractor pool derived from the training split**.

The same distractor pool is reused for noisy training, validation, and test construction.

Target chunks are retrieved using dense embeddings and MMR.

The default retrieval encoder is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Chunking uses approximately:

```text
maximum chunk size = 150 words
overlap            = 30 words
```

Noise selection:

```text
Query-aligned:
  P70-P95 similarity band
  fallback: P60-P98

Query-distant:
  bottom 10%
  fallback: bottom 20%
```

After target and noise chunks are combined, their order is shuffled.

To rebuild the processed dataset:

```bash
python src/databuildt.py \
  --arxiv_dir ./dataset/arxiv \
  --output_dir ./prepared_data_huflit \
  --train_limit 20000 \
  --valid_limit 1000 \
  --test_limit 500 \
  --noise_pool_offset 20000 \
  --noise_pool_limit 10000 \
  --final_k 3 \
  --noise_k 2 \
  --substitutive_clean_k 1 \
  --seed 42
```

---

## Evaluation Conditions

| Condition | File | Context |
|---|---|---|
| Clean | `test_clean.jsonl` | 3 target chunks |
| Query-aligned additive | `test_noisy_easy_additive.jsonl` | 3 target + 2 distractors |
| Query-distant additive | `test_noisy_hard_additive.jsonl` | 3 target + 2 distractors |
| Query-aligned substitutive | `test_noisy_easy_substitutive.jsonl` | 1 target + 2 distractors |
| Query-distant substitutive | `test_noisy_hard_substitutive.jsonl` | 1 target + 2 distractors |

The legacy labels `easy` and `hard` are retained only for file traceability:

```text
easy -> query-aligned
hard -> query-distant
```

They should not be interpreted as human-validated difficulty labels.

---

## Models

The reported experiments use:

```text
facebook/bart-base
google-t5/t5-base
```

For each architecture, two checkpoints are compared:

```text
clean-matched
noise-aware
```

---

## Reported Training Configuration

| Parameter | BART-base | T5-base |
|---|---:|---:|
| Epochs | 1 | 1 |
| Optimizer | AdamW (`adamw_torch`) | AdamW (`adamw_torch`) |
| Learning rate | `3e-5` | `3e-5` |
| Weight decay | `0.01` | `0.01` |
| Warmup ratio | `0.03` | `0.03` |
| Max source length | `1024` | `1024` |
| Max target length | `512` | `512` |
| Generation max length | `320` | `320` |
| Beam size | `4` | `4` |
| Early stopping | `True` | `True` |
| No-repeat n-gram size | `3` | `3` |
| Train batch/device | `8` | `4` |
| Eval batch/device | `8` | `4` |
| Gradient accumulation | `2` | `4` |
| Effective batch size | `16` | `16` |
| Seed | `42` | `42` |

The machine-readable configuration is provided in:

```text
configs/reported_run.yaml
```

**Important:** explicitly use `--learning_rate 3e-5` and
`--generation_max_length 320` for both BART-base and T5-base when reproducing the reported runs.

---

## Evaluation

The reported evaluation uses:

```text
max_source_length     = 1024
max_target_length     = 512
generation_max_length = 320
num_beams             = 4
early_stopping        = True
no_repeat_ngram_size  = 3
BERTScore model       = roberta-large
seed                  = 42
```

The released evaluation configuration is stored in:

```text
metrics/metrics_full/eval_config_rankB.json
```

The evaluator computes:

- ROUGE-1;
- ROUGE-2;
- ROUGE-L;
- BERTScore;
- retrieval diagnostics;
- truncation diagnostics;
- paired statistical tests;
- bootstrap confidence intervals;
- effect sizes;
- robustness degradation;
- additive-versus-substitutive comparisons.

---

## Truncation-Aware Evidence Status

The manuscript uses study-specific operational labels:

```text
Primary:   truncation rate <= 5%
Qualified: truncation rate > 5% and <= 50%
Excluded:  truncation rate > 50%
```

Observed truncation rates:

| Model | Condition | Truncation | Status |
|---|---|---:|---|
| BART | Clean | 1.4% | Primary |
| BART | Query-aligned additive | 23.4% | Qualified |
| BART | Query-distant additive | 20.0% | Qualified |
| BART | Query-aligned substitutive | 1.6% | Primary |
| BART | Query-distant substitutive | 1.0% | Primary |
| T5 | Clean | 5.8% | Qualified |
| T5 | Query-aligned additive | 78.8% | Excluded |
| T5 | Query-distant additive | 75.4% | Excluded |
| T5 | Query-aligned substitutive | 6.8% | Qualified |
| T5 | Query-distant substitutive | 3.0% | Primary |

---

## NER and TRR

The complete framework defines Noise Exposure Rate (NER) and Target Retention Rate (TRR) as post-truncation exposure diagnostics.

The original reported runs did **not** retain token-level target/noise provenance after model-specific truncation.

Therefore:

- empirical NER is not reported;
- target-specific empirical TRR is not reported;
- overall input-retention ratio is not relabeled as TRR;
- truncation rate is used only as a conservative evidence-screening diagnostic.

This limitation is one reason the study is presented as a **proof-of-concept** rather than a complete validation of every diagnostic in the framework.

---

## Statistical Scope

The study reports one independently trained checkpoint pair per architecture.

Paired bootstrap confidence intervals and paired statistical tests quantify uncertainty across matched test instances.

They do **not** measure training variability across independently trained random seeds.

Multi-seed replication is therefore required before architecture-level generalization.

---

## Released Artifacts

Evaluation outputs are available under:

```text
metrics/metrics_full/
```

Important files include:

```text
eval_config_rankB.json
predictions/
rankB_additive_vs_substitutive.csv
rankB_compact_paper_table.csv
rankB_metrics_record_level.csv
rankB_metrics_summary.csv
rankB_paired_noiseaware_vs_clean.csv
rankB_retrieval_summary.csv
rankB_robustness_degradation.csv
rankB_truncation_summary.csv
```

---

## Reproduction Workflow

```text
1. Download the Cornell arXiv dataset.
2. Run src/databuildt.py.
3. Train BART-base clean-matched.
4. Train BART-base noise-aware.
5. Train T5-base clean-matched.
6. Train T5-base noise-aware.
7. Run src/eval.py on the five matched test conditions.
8. Compare reproduced metrics with metrics/metrics_full/.
```

Additional documentation is available in:

```text
docs/REPRODUCIBILITY.md
docs/DATASET_RECONSTRUCTION.md
docs/ARTIFACTS.md
docs/ENVIRONMENT.md
```

---

## Reproducibility Limitations

The reported study has two explicit limitations:

1. only one independently trained checkpoint pair is evaluated per architecture;
2. post-truncation target/noise token provenance was not retained in the original runs.

These limitations are explicitly reflected in the claims made in the manuscript.

---

## Citation

```bibtex
@unpublished{bao2026truncationaware,
  author = {Bui Nguyen Gia Bao and Le Nhat Tung},
  title  = {Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5},
  year   = {2026},
  note   = {Manuscript under revision}
}
```
