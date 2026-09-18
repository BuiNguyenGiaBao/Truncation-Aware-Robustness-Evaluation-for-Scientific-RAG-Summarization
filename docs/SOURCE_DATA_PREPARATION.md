# Source Data Preparation

## Input expected by `src/databuildt.py`

The current builder does not ingest a raw metadata dump or a directory of PDFs directly.

It expects a local HuggingFace `Dataset` / `DatasetDict` saved with `datasets.save_to_disk(...)` and containing:

```text
train
validation
test
```

Each sample must expose:

```text
article   -> full article text used for chunking and retrieval
abstract  -> reference summary
```

Minimal example:

```json
{
  "article": "Full scientific article text ...",
  "abstract": "Reference abstract ..."
}
```

Validation:

```python
from datasets import load_from_disk

ds = load_from_disk("./dataset/arxiv")
assert "article" in ds["train"].column_names
assert "abstract" in ds["train"].column_names
```

## Reproducibility boundary

The repository provides the RAG data-construction stage starting from article/abstract text, but it does not provide a raw-source-to-full-text ingestion pipeline.

The accurate claim is:

> Given a local article/abstract DatasetDict derived from the Cornell arXiv source corpus, the released builder deterministically reconstructs the manuscript-aligned clean, additive, and substitutive RAG contexts using the reported seed and configuration.

## Builder command

```bash
python src/databuildt.py   --arxiv_dir ./dataset/arxiv   --output_dir ./prepared_data_huflit   --train_limit 20000   --valid_limit 1000   --test_limit 500   --noise_pool_offset 20000   --noise_pool_limit 10000   --final_k 3   --noise_k 2   --substitutive_clean_k 1   --seed 42
```
