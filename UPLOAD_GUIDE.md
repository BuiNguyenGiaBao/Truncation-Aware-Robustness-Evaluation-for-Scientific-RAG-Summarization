# Upload Guide

Copy these files/folders into the root of the existing GitHub repository:

```text
README.md
configs/
docs/
scripts/
requirements.in
CITATION.cff
.gitignore
```

Keep the existing:

```text
src/
metrics/
```

Then run:

```bash
python scripts/verify_reproducibility.py
```

The verifier will intentionally fail until the noise-pool strategy used by the reported experiment is confirmed and `configs/reported_run.yaml` is updated.
