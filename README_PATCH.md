# README patch

Apply these edits to the current `README.md`.

## Replace the current `Source Dataset` section with

```markdown
## Source Dataset and Input Contract

The study uses the Cornell University arXiv source corpus.

The public `src/databuildt.py` builder starts from a local HuggingFace
`Dataset` / `DatasetDict` containing `article` and `abstract` fields.
It does not ingest a raw metadata dump or PDF directory directly.

See:

- `docs/SOURCE_DATA_PREPARATION.md`
- `docs/DATASET_RECONSTRUCTION.md`

Given this article/abstract DatasetDict, the released builder deterministically
reconstructs the manuscript-aligned clean, additive, and substitutive RAG
contexts using the reported seed and configuration.
```

## Add this sentence under `Reproducibility Limitations`

```markdown
The public builder reproduces the manuscript-described data-construction
protocol, but the retained artifacts do not establish byte-identical
reconstruction of the historical processed JSONL files from the raw source
corpus alone.
```

## Add this file to the documentation list

```text
docs/SOURCE_DATA_PREPARATION.md
```
