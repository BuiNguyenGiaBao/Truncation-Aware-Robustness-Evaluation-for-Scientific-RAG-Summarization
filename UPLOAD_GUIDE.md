# Upload Guide

Replace / add these files:

```text
CITATION.cff
configs/reported_run.yaml
docs/NOISE_POOL_ALIGNMENT.md
docs/REPRODUCIBILITY.md
docs/SOURCE_DATA_PREPARATION.md
docs/DATASET_RECONSTRUCTION.md
docs/DATASET_REPRODUCTION.md
docs/GITHUB_REVISION_CHECKLIST.md
scripts/verify_reproducibility.py
```

Also apply the small text patches in:

```text
README_PATCH.md
src/databuildt_docstring.patch
```

Then run:

```bash
python scripts/verify_reproducibility.py
```

The check verifies repository consistency with the revised manuscript. It does not prove byte-identical historical processed-data reconstruction.
