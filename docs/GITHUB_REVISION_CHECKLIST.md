# GitHub Revision Checklist

Before resubmitting the HUFLIT revision:

- [ ] Replace the repository root `README.md` with the revised README.
- [ ] Add `configs/reported_run.yaml`.
- [ ] Add `docs/REPRODUCIBILITY.md`.
- [ ] Add `docs/DATASET_REPRODUCTION.md`.
- [ ] Add `docs/ARTIFACTS.md`.
- [ ] Add `docs/ENVIRONMENT.md`.
- [ ] Add `requirements.in`.
- [ ] Add `CITATION.cff`.
- [ ] Add or update `.gitignore`.
- [ ] Confirm `src/databuildt.py` exists and rebuilds the reported conditions.
- [ ] Confirm the training script can accept the exact reported hyperparameters.
- [ ] Confirm `src/eval.py` uses the reported decoding configuration.
- [ ] Confirm aggregate artifacts are present in `metrics/metrics_full/`.
- [ ] Confirm README does not claim files that are absent from the public repository.
- [ ] If exact package versions are recovered, add `requirements.txt`.
- [ ] Do not publish guessed historical package versions.
- [ ] Do not claim empirical NER/TRR without post-truncation target/noise provenance.
