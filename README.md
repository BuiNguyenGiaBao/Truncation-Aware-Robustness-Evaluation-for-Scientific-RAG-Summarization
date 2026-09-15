# Truncation-Aware Robustness Evaluation for Scientific RAG Summarization



**Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5**

Authors: **Bui Nguyen Gia Bao, Le Nhat Tung**

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
=======
This repository contains the code and released evaluation artifacts for the study:

**Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5**

Authors: **Bui Nguyen Gia Bao and Le Nhat Tung**

The project studies a measurement-validity problem in retrieval-augmented generation (RAG) summarization: when noisy retrieved context increases input length, model-specific tokenization may truncate part of the intended evidence. A model can therefore appear robust even when it was not exposed to all injected noise.

The goal of this repository is **not** to claim a new state-of-the-art summarization architecture. Instead, it provides a reproducible proof-of-concept pipeline for separating:

1. intended context composition,
2. model-specific truncation,
3. evidence status,
4. paired performance differences, and
5. clean/noisy trade-offs.

---

## 1. Repository Status

The current public repository contains source code and aggregate evaluation artifacts used by the study.

```text
.
├── README.md
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

Large processed datasets and model checkpoints are not tracked in Git because of their size. The dataset-construction and training scripts are provided so that the experimental data and checkpoints can be reconstructed from the source dataset.

---

## 2. Research Question

The study asks:

> **When a RAG summarization model appears robust to retrieval noise, was the model actually exposed to the intended noisy evidence after model-specific tokenization and truncation?**

This distinction matters especially for additive-noise experiments, because adding distractor chunks increases source length and can trigger truncation.

---

## 3. Dataset

The experiments use the **Cornell University arXiv Dataset** released on Kaggle:

https://www.kaggle.com/datasets/Cornell-University/arxiv

The local pipeline uses:

- article text for chunking and retrieval;
- abstracts as reference summaries;
- task-level summarization queries for distractor selection.

The abstract is **not** used to construct the retrieval query.

The section-aware chunker falls back to a word-window strategy when section detection is insufficient. The reported configuration uses approximately:

```text
chunk size     ≈ 150 words
chunk overlap  = 30 words
```

Very short chunks are discarded.

---

## 4. Experimental Conditions

The paper uses five matched evaluation conditions.

| Paper terminology | Legacy file label | Context composition | Role |
|---|---|---:|---|
| Clean | `test_clean.jsonl` | 3 target chunks | Baseline |
| Query-aligned additive | `test_noisy_easy_additive.jsonl` | 3 target + 2 distractors | Additive stress test |
| Query-distant additive | `test_noisy_hard_additive.jsonl` | 3 target + 2 distractors | Additive stress test |
| Query-aligned substitutive | `test_noisy_easy_substitutive.jsonl` | 1 target + 2 distractors | Length-controlled stress test |
| Query-distant substitutive | `test_noisy_hard_substitutive.jsonl` | 1 target + 2 distractors | Length-controlled stress test |

The legacy labels `easy` and `hard` are retained only for file traceability:

```text
easy  -> query-aligned
hard  -> query-distant
```

They should **not** be interpreted as human-validated difficulty categories.

After noisy contexts are constructed, target and distractor chunks are merged and shuffled to reduce fixed-position bias.

---

## 5. Models

The proof-of-concept experiments use:

```text
facebook/bart-base
google-t5/t5-base
```

For each architecture, two checkpoints are compared:

```text
clean-matched  -> trained on clean retrieval contexts
noise-aware    -> trained on clean and noisy retrieval contexts
```

The experiments are intended as a **proof-of-concept demonstration of the evaluation framework**, not as a benchmark-level comparison of BART and T5.

---

## 6. Exact Training Configuration

The reported runs use the following configuration.

| Parameter | BART-base | T5-base |
|---|---:|---:|
| Training epochs | 1 | 1 |
| Optimizer | AdamW (`adamw_torch`) | AdamW (`adamw_torch`) |
| Learning rate | `3e-5` | `3e-5` |
| Weight decay | `0.01` | `0.01` |
| Warmup ratio | `0.03` | `0.03` |
| Max source length | `1024` | `1024` |
| Max target length | `512` | `512` |
| Generation max length | `320` | `320` |
| Per-device train batch size | `8` | `4` |
| Per-device eval batch size | `8` | `4` |
| Gradient accumulation steps | `2` | `4` |
| Effective batch size | `16` | `16` |
| Random seed | `42` | `42` |

**Important:** the training script has architecture-dependent defaults. To reproduce the paper, explicitly pass `--learning_rate 3e-5` for **both** BART-base and T5-base.

---

## 7. Decoding Configuration

The evaluation code uses model-specific tokenization with truncation at 1024 source tokens.

The reported generation configuration is:

```text
generation_max_length = 320
num_beams              = 4
early_stopping         = True
no_repeat_ngram_size   = 3
```

The released evaluation configuration is stored in:

```text
metrics/metrics_full/eval_config_rankB.json
```

That file also records the evaluated model directories, test files, BERTScore configuration, source/target limits, and random seed.

---

## 8. Reconstructing the Processed Dataset

Place the arXiv dataset in the path expected by the builder, for example:

```text
./dataset/arxiv
```

Then inspect the available arguments:

```bash
python src/databuildt.py --help
```

A paper-matched reconstruction uses the study settings below:

```bash
python src/databuildt.py \
  --arxiv_dir ./dataset/arxiv \
  --output_dir ./prepared_data_rankB_fixed_v2 \
  --train_limit 20000 \
  --valid_limit 1000 \
  --test_limit 500 \
  --min_target_words 30 \
  --max_target_words 512 \
  --final_k 3 \
  --noise_k 2 \
  --min_chunks 1 \
  --noise_pool_limit 10000 \
  --noise_pool_strategy heldout_train_tail \
  --test_noise_pool_offset 30000 \
  --test_noise_pool_limit 10000 \
  --substitutive_clean_k 1 \
  --num_workers 2 \
  --encode_batch_size 16 \
  --paper_batch 100 \
  --clean_control_mode unique \
  --seed 42 \
  --laptop_safe
```

The expected processed files are:

```text
prepared_data_rankB_fixed_v2/
├── train_noiseaware.jsonl
├── train_clean_matched.jsonl
├── valid_noiseaware.jsonl
├── valid_clean_matched.jsonl
├── test_clean.jsonl
├── test_noisy_easy_additive.jsonl
├── test_noisy_hard_additive.jsonl
├── test_noisy_easy_substitutive.jsonl
└── test_noisy_hard_substitutive.jsonl
```

Each reported test condition contains **500 matched samples**.

---

## 9. Training

### 9.1 BART-base noise-aware

```bash
python src/train/train_bart_t5_runpod.py \
  --data_dir ./prepared_data_rankB_fixed_v2 \
  --train_file train_noiseaware.jsonl \
  --validation_file valid_noiseaware.jsonl \
  --model_name facebook/bart-base \
  --output_dir ./outputs/bart_t5_auto_1epoch/01_bart_base_noiseaware \
  --num_train_epochs 1 \
  --learning_rate 3e-5 \
  --weight_decay 0.01 \
  --warmup_ratio 0.03 \
  --max_source_length 1024 \
  --max_target_length 512 \
  --generation_max_length 320 \
  --generation_num_beams 4 \
  --per_device_train_batch_size 8 \
  --per_device_eval_batch_size 8 \
  --gradient_accumulation_steps 2 \
  --optim adamw_torch \
  --seed 42
```

### 9.2 BART-base clean-matched

```bash
python src/train/train_bart_t5_runpod.py \
  --data_dir ./prepared_data_rankB_fixed_v2 \
  --train_file train_clean_matched.jsonl \
  --validation_file valid_clean_matched.jsonl \
  --model_name facebook/bart-base \
  --output_dir ./outputs/bart_t5_auto_1epoch/02_bart_base_clean_matched \
  --num_train_epochs 1 \
  --learning_rate 3e-5 \
  --weight_decay 0.01 \
  --warmup_ratio 0.03 \
  --max_source_length 1024 \
  --max_target_length 512 \
  --generation_max_length 320 \
  --generation_num_beams 4 \
  --per_device_train_batch_size 8 \
  --per_device_eval_batch_size 8 \
  --gradient_accumulation_steps 2 \
  --optim adamw_torch \
  --seed 42
```

### 9.3 T5-base noise-aware

```bash
python src/train/train_bart_t5_runpod.py \
  --data_dir ./prepared_data_rankB_fixed_v2 \
  --train_file train_noiseaware.jsonl \
  --validation_file valid_noiseaware.jsonl \
  --model_name google-t5/t5-base \
  --output_dir ./outputs/bart_t5_auto_1epoch/03_t5_base_noiseaware \
  --num_train_epochs 1 \
  --learning_rate 3e-5 \
  --weight_decay 0.01 \
  --warmup_ratio 0.03 \
  --max_source_length 1024 \
  --max_target_length 512 \
  --generation_max_length 320 \
  --generation_num_beams 4 \
  --per_device_train_batch_size 4 \
  --per_device_eval_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --optim adamw_torch \
  --seed 42
```

### 9.4 T5-base clean-matched

```bash
python src/train/train_bart_t5_runpod.py \
  --data_dir ./prepared_data_rankB_fixed_v2 \
  --train_file train_clean_matched.jsonl \
  --validation_file valid_clean_matched.jsonl \
  --model_name google-t5/t5-base \
  --output_dir ./outputs/bart_t5_auto_1epoch/04_t5_base_clean_matched \
  --num_train_epochs 1 \
  --learning_rate 3e-5 \
  --weight_decay 0.01 \
  --warmup_ratio 0.03 \
  --max_source_length 1024 \
  --max_target_length 512 \
  --generation_max_length 320 \
  --generation_num_beams 4 \
  --per_device_train_batch_size 4 \
  --per_device_eval_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --optim adamw_torch \
  --seed 42
```

All four runs use the same one-epoch budget and the same effective batch size of 16.

---

## 10. Evaluation

The main evaluation script is:

```text
src/eval.py
```

A fresh generation-and-evaluation run can be launched with:

```bash
python src/eval.py \
  --data_dir ./prepared_data_rankB_fixed_v2 \
  --out_root ./outputs/bart_t5_auto_1epoch \
  --output_dir ./reproduced_metrics \
  --max_source_length 1024 \
  --max_target_length 512 \
  --generation_max_length 320 \
  --num_beams 4 \
  --batch_size 8 \
  --bertscore_model roberta-large \
  --bertscore_batch_size 8 \
  --bertscore_max_length 512 \
  --length_tokenizer facebook/bart-base \
  --seed 42
```

If predictions have already been generated and only the metrics need to be recomputed, add:

```bash
--skip_generation
```

The released paper-level evaluation artifacts are available under:

```text
metrics/metrics_full/
```

---

## 11. Evaluation Metrics

The released evaluation pipeline reports:

### Summary quality

```text
ROUGE-1
ROUGE-2
ROUGE-L
ROUGE-Lsum
BERTScore precision / recall / F1
```

### Statistical analysis

```text
paired t-test
Wilcoxon signed-rank test
Cohen's dz
Cliff's delta
rank-biserial correlation
paired bootstrap 95% confidence interval
Holm correction
```

### Diagnostic / support proxies

```text
source token lengths
model-specific truncation rate
target-source context composition
source-supported entity rate
unsupported entity rate
number preservation
source token support rate
sentence-support proxy
```

The source-support measures are **sanity-check proxies**, not full factuality metrics.

---

## 12. Truncation-Aware Evidence Classification

The study uses the following operational rules:

| Truncation rate | Evidence status |
|---:|---|
| `<= 5%` | Primary |
| `> 5% and <= 50%` | Qualified |
| `> 50%` | Excluded from primary claims |

These thresholds are **study-specific operational rules**, not universal literature-derived cutoffs.

The observed truncation rates are:

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

## 13. NER and TRR: Scope of the Current Release

The full proposed framework defines two post-truncation exposure diagnostics.

### Noise Exposure Rate (NER)

$$
NER = \frac{N_{\text{noise, retained}}}{N_{\text{noise, injected}}}
$$

### Target Retention Rate (TRR)

$$
TRR = \frac{N_{\text{target, retained}}}{N_{\text{target, pre-truncation}}}
$$

However, the original reported runs did **not** retain token-level target/noise provenance after model-specific tokenization and truncation.

Therefore:

```text
- numerical NER is not claimed for the current runs;
- numerical target-specific TRR is not claimed for the current runs;
- aggregate input retention is not relabeled as TRR;
- observed model-specific truncation rate is used as a conservative exposure diagnostic;
- additive BART evidence is qualified;
- additive T5 evidence is excluded from primary robustness claims.
```

This is why the study is framed as a **proof-of-concept empirical demonstration**, rather than a complete empirical validation of every diagnostic in the full protocol.

A future fully instrumented run should retain per-token target/noise provenance after tokenization so that NER and TRR can be computed directly.

---

## 14. Main Findings

The strongest numerical BART improvement occurs under **query-distant additive noise**, but that condition has a 20.0% truncation rate and is therefore treated as **qualified evidence**.

For the primary low-truncation **query-distant substitutive** condition, the noise-aware BART checkpoint improves BERTScore F1 by approximately:

```text
+0.0021
```

while the ROUGE differences are not statistically reliable after multiplicity correction.

Accordingly, the paper interprets the primary result as a **small, condition-specific semantic-similarity effect**, not as a large or universal improvement in summary quality.

T5 additive results are not used as primary robustness evidence because 75.4–78.8% of those inputs are truncated.

---

## 15. Reproducibility Notes

To reproduce the reported study as closely as possible:

```text
1. Use seed 42.
2. Use the exact 3e-5 learning rate for both architectures.
3. Keep max source/target lengths at 1024/512.
4. Use generation max length 320 and 4-beam decoding.
5. Preserve the five matched evaluation conditions.
6. Do not reinterpret legacy easy/hard labels as human difficulty.
7. Treat T5 additive results as excluded from primary claims.
8. Do not report NER/TRR unless token-level target/noise provenance is available.
```

The released file:

```text
metrics/metrics_full/eval_config_rankB.json
```

is the primary machine-readable record of the evaluation configuration used for the reported metrics.

---

## 16. Limitations

The current study has several deliberate scope limitations.

- One trained checkpoint pair per architecture is reported; the study does not estimate multi-seed training variability.
- Paired bootstrap confidence intervals characterize uncertainty across matched test instances, not across independently trained seeds.
- Token-level post-truncation provenance was not preserved in the original runs, so NER/TRR cannot be reconstructed retrospectively from the aggregate artifacts.
- Retrieval source membership is a construction diagnostic, not a human annotation of summary relevance.
- ROUGE and BERTScore do not provide full factuality verification.
- The study evaluates BART-base and T5-base as proof-of-concept model families rather than as a comprehensive architecture benchmark.

---

## 17. Released Result Files

| File | Purpose |
|---|---|
| `rankB_compact_paper_table.csv` | Compact performance table |
| `rankB_metrics_summary.csv` | Aggregate metric summary |
| `rankB_metrics_record_level.csv` | Record-level evaluation data |
| `rankB_paired_noiseaware_vs_clean.csv` | Paired checkpoint comparison |
| `rankB_robustness_degradation.csv` | Clean/noisy robustness trade-offs |
| `rankB_additive_vs_substitutive.csv` | Additive vs. substitutive comparison |
| `rankB_retrieval_summary.csv` | Retrieval/context diagnostics |
| `rankB_truncation_summary.csv` | Model-specific truncation diagnostics |
| `rankB_all_metrics_tables.xlsx` | Consolidated workbook |
| `eval_config_rankB.json` | Machine-readable evaluation configuration |

---

## 18. Citation

If you use this repository, please cite the manuscript as:

```bibtex
@unpublished{bao2026truncationaware,
  author = {Bui Nguyen Gia Bao , Le Nhat Tung},
>>>>>>> cb9e52a2af685806cc5b246cf07e850fc0b00acd
  title  = {Truncation-Aware Robustness Evaluation for Scientific RAG Summarization: A Proof-of-Concept Study with BART and T5},
  year   = {2026},
  note   = {Manuscript under revision}
}
```
<<<<<<< HEAD
=======

Please update the citation if a final journal citation becomes available.

---

## 19. License

No explicit license file is currently included in this repository. Unless a license is added, reuse and redistribution are subject to the repository authors' copyright.

---

## 20. Contact

For reproduction questions or issues with the released scripts/artifacts, please open a GitHub issue or contact the repository maintainers.


