# Truncation-Aware Robustness Evaluation for Scientific RAG Summarization

**Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5**

Authors: **Bui Nguyen Gia Bao, Tran Le Van, Le Nhat Tung**

This repository contains the code and released evaluation artifacts supporting the HUFLIT manuscript revision. The study is a **checkpoint-level proof-of-concept** and does not claim multi-seed architecture-level generalization or complete empirical validation of all proposed diagnostics.

## Repository contents

```text
.
├── README.md
├── configs/
│   └── reported_run.yaml
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── DATASET_RECONSTRUCTION.md
│   ├── ARTIFACTS.md
│   ├── ENVIRONMENT.md
│   └── NOISE_POOL_ALIGNMENT.md
├── scripts/
│   └── verify_reproducibility.py
├── requirements.in
├── CITATION.cff
├── src/
│   ├── databuildt.py
│   ├── eval.py
│   ├── retrieval_tokenizer.py
│   ├── rulebase_chunkforpdf.py
│   ├── summarized.py
│   └── train/
│       └── train_bart_t5_runpod.py
└── metrics/
    └── metrics_full/
        ├── eval_config_rankB.json
        ├── predictions/
        ├── rankB_additive_vs_substitutive.csv
        ├── rankB_all_metrics_tables.xlsx
        ├── rankB_compact_paper_table.csv
        ├── rankB_metrics_record_level.csv
        ├── rankB_metrics_summary.csv
        ├── rankB_paired_noiseaware_vs_clean.csv
        ├── rankB_retrieval_summary.csv
        ├── rankB_robustness_degradation.csv
        └── rankB_truncation_summary.csv
```

## Source dataset

The source corpus is the Cornell University arXiv Dataset:

https://www.kaggle.com/datasets/Cornell-University/arxiv

Article text is used for chunking/retrieval, while abstracts are used as reference summaries.

## Evaluation conditions

| Condition | Legacy filename | Composition |
|---|---|---|
| Clean | `test_clean.jsonl` | 3 target chunks |
| Query-aligned additive | `test_noisy_easy_additive.jsonl` | 3 target + 2 distractors |
| Query-distant additive | `test_noisy_hard_additive.jsonl` | 3 target + 2 distractors |
| Query-aligned substitutive | `test_noisy_easy_substitutive.jsonl` | 1 target + 2 distractors |
| Query-distant substitutive | `test_noisy_hard_substitutive.jsonl` | 1 target + 2 distractors |

Legacy `easy`/`hard` names are retained only for artifact traceability.

## Exact reported training configuration

| Parameter | BART-base | T5-base |
|---|---:|---:|
| Model | `facebook/bart-base` | `google-t5/t5-base` |
| Epochs | 1 | 1 |
| Optimizer | AdamW (`adamw_torch`) | AdamW (`adamw_torch`) |
| Learning rate | `3e-5` | `3e-5` |
| Weight decay | `0.01` | `0.01` |
| Warmup ratio | `0.03` | `0.03` |
| Max source length | `1024` | `1024` |
| Max target length | `512` | `512` |
| Generation max length | `320` | `320` |
| Beams | `4` | `4` |
| Early stopping | `True` | `True` |
| No-repeat n-gram | `3` | `3` |
| Train batch/device | `8` | `4` |
| Eval batch/device | `8` | `4` |
| Gradient accumulation | `2` | `4` |
| Effective batch size | `16` | `16` |
| Seed | `42` | `42` |
| Training replication | 1 checkpoint pair | 1 checkpoint pair |

**Important:** the training script has architecture-specific defaults. For the reported experiment, explicitly pass `--learning_rate 3e-5` and `--generation_max_length 320` for both architectures.

## Evaluation configuration

The released `metrics/metrics_full/eval_config_rankB.json` records:

- the five test files;
- max source/target lengths `1024/512`;
- generation max length `320`;
- beam size `4`;
- BERTScore model `roberta-large`;
- seed `42`;
- the four evaluated checkpoint paths.

## Truncation-aware evidence status

Study-specific operational labels:

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

## NER / TRR scope

The full framework defines NER and TRR as post-truncation exposure diagnostics. The original reported runs did not retain post-truncation target/noise token provenance, so empirical NER and target-specific TRR are **not** reported or imputed.

Truncation rate is used only as a conservative evidence-screening diagnostic; it is not a numerical substitute for NER or TRR.

## Reproduction

See:

- `docs/REPRODUCIBILITY.md`
- `docs/DATASET_RECONSTRUCTION.md`
- `docs/ARTIFACTS.md`
- `docs/ENVIRONMENT.md`
- `docs/NOISE_POOL_ALIGNMENT.md`

Before resubmission, run:

```bash
python scripts/verify_reproducibility.py
```

## Critical noise-pool note

The current public `src/databuildt.py` supports both a held-out train-tail noise-pool strategy and a legacy train-pool strategy. The manuscript and repository must describe the **same strategy actually used to generate the reported tables**.

See `docs/NOISE_POOL_ALIGNMENT.md` before resubmission. Do not claim that the public builder exactly reproduces the manuscript until this item has been verified.

## Statistical scope

Only one independently trained checkpoint pair is reported per architecture. Paired tests and bootstrap intervals quantify uncertainty across matched test instances, not training variability across independently trained random seeds.

## Citation

```bibtex
@unpublished{bao2026truncationaware,
  author = {Bui Nguyen Gia Bao and Tran Le Van and Le Nhat Tung},
  title  = {Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5},
  year   = {2026},
  note   = {Manuscript under revision}
}
```
