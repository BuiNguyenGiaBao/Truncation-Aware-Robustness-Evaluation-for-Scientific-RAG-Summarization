# Truncation-Aware Robustness Evaluation for Scientific RAG Summarization

This repository supports the manuscript:

**Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5**

Authors: **Bui Nguyen Gia Bao, Tran Le Van, Le Nhat Tung**

## Scope

This study is a **checkpoint-level proof-of-concept** for truncation-aware robustness evaluation in scientific RAG summarization. It is not a multi-seed architecture benchmark and does not claim complete empirical validation of every diagnostic in the proposed framework.

The released materials are intended to make the following components reproducible:

- source-data preparation;
- section-aware chunking;
- retrieval and controlled noisy-context construction;
- clean, additive, and substitutive evaluation conditions;
- BART-base and T5-base training;
- generation and decoding;
- truncation diagnostics;
- paired statistical evaluation;
- aggregate result tables used in the manuscript.

## Source dataset

The experiments use the Cornell University arXiv Dataset:

https://www.kaggle.com/datasets/Cornell-University/arxiv

The local pipeline uses article text for chunking and retrieval and abstracts as reference summaries. The abstract is not used to build the retrieval query.

## Evaluation conditions

| Manuscript condition | Legacy file label | Context composition | Evidence role |
|---|---|---:|---|
| Clean | `test_clean.jsonl` | 3 target chunks | Baseline |
| Query-aligned additive | `test_noisy_easy_additive.jsonl` | 3 target + 2 distractors | Additive stress test |
| Query-distant additive | `test_noisy_hard_additive.jsonl` | 3 target + 2 distractors | Additive stress test |
| Query-aligned substitutive | `test_noisy_easy_substitutive.jsonl` | 1 target + 2 distractors | Length-controlled stress test |
| Query-distant substitutive | `test_noisy_hard_substitutive.jsonl` | 1 target + 2 distractors | Length-controlled stress test |

`easy` and `hard` are retained only for file traceability. In the manuscript they are interpreted as `query-aligned` and `query-distant`; they are not human-validated difficulty labels.

## Exact reported configuration

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
| Beam size | `4` | `4` |
| Early stopping | `True` | `True` |
| No-repeat n-gram size | `3` | `3` |
| Train batch / device | `8` | `4` |
| Eval batch / device | `8` | `4` |
| Gradient accumulation | `2` | `4` |
| Effective batch size | `16` | `16` |
| Seed | `42` | `42` |
| Training replication | 1 checkpoint pair | 1 checkpoint pair |

The machine-readable configuration is in:

```text
configs/reported_run.yaml
```

## Reproduction workflow

1. Download the Cornell arXiv source dataset.
2. Rebuild processed clean/noisy contexts with the repository data-construction script.
3. Train four checkpoints:
   - BART-base clean-matched
   - BART-base noise-aware
   - T5-base clean-matched
   - T5-base noise-aware
4. Run generation and evaluation on the five matched test conditions.
5. Recompute truncation diagnostics and paired statistics.
6. Compare reproduced aggregate tables with the released result artifacts.

Detailed instructions are in:

- `docs/DATASET_REPRODUCTION.md`
- `docs/REPRODUCIBILITY.md`
- `docs/ARTIFACTS.md`
- `docs/ENVIRONMENT.md`

## Truncation-aware evidence status

The manuscript uses study-specific operational thresholds:

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

The full framework defines:

\[
NER = \frac{N_{\text{noise, retained}}}{N_{\text{noise, injected}}}
\]

\[
TRR = \frac{N_{\text{target, retained}}}{N_{\text{target, pre-truncation}}}
\]

The original reported runs did **not** retain post-truncation target/noise token provenance. Therefore this release:

- does not report empirical NER values;
- does not report target-specific empirical TRR values;
- does not relabel overall input-retention ratio as TRR;
- uses model-specific truncation rate only as a conservative evidence-screening diagnostic;
- treats BART additive results as **Qualified**;
- treats T5 additive results as **Excluded from primary claims**.

This limitation is why the manuscript is framed as a **proof-of-concept demonstration** rather than a full empirical validation of every diagnostic in the framework.

## Statistical scope

Only one independently trained checkpoint pair is reported per architecture. Paired bootstrap confidence intervals and paired tests quantify uncertainty across matched test instances, not optimization variability across independently trained seeds. Multi-seed replication is therefore required before architecture-level generalization.

## Main interpretation

The strongest numerical BART gains occur in the query-distant additive condition, but this condition is Qualified because 20.0% of inputs are truncated.

For the primary low-truncation query-distant substitutive condition:

```text
BERTScore F1 delta = +0.0021
paired effect size d_z = 0.204
```

The ROUGE differences are not statistically reliable after multiplicity correction. The manuscript therefore interprets this result as a small, condition-specific checkpoint-level effect rather than a large or universal gain in summary quality.

## Environment note

Exact package versions from the original run should be added only if they can be recovered from the original RunPod environment or logs. Do **not** invent package versions.

See `docs/ENVIRONMENT.md`.

## Citation

```bibtex
@unpublished{bao2026truncationaware,
  author = {Bui Nguyen Gia Bao and Tran Le Van and Le Nhat Tung},
  title  = {Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5},
  year   = {2026},
  note   = {Manuscript under revision}
}
```
