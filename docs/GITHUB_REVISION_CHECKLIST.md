# GitHub Revision Checklist

Before HUFLIT resubmission:

- [ ] README and `CITATION.cff` use only Bui Nguyen Gia Bao and Le Nhat Tung.
- [ ] `configs/reported_run.yaml` states `shared_training_pool` and contains no obsolete blocker.
- [ ] `src/databuildt.py` is the manuscript-aligned shared-pool builder.
- [ ] `docs/NOISE_POOL_ALIGNMENT.md` contains no obsolete held-out-pool instructions.
- [ ] `docs/SOURCE_DATA_PREPARATION.md` states the required `article` / `abstract` DatasetDict input contract.
- [ ] `docs/REPRODUCIBILITY.md` uses the current builder command and explicit reported settings.
- [ ] training is reproduced with `--learning_rate 3e-5` and `--generation_max_length 320`.
- [ ] `src/eval.py` and `metrics/metrics_full/eval_config_rankB.json` agree on the five conditions and decoding settings.
- [ ] aggregate artifacts remain present in `metrics/metrics_full/`.
- [ ] empirical NER/TRR are not claimed from historical artifacts.
- [ ] exact historical package versions are not guessed.
- [ ] response-to-reviewers uses the same reproducibility wording as the repository.
- [ ] run `python scripts/verify_reproducibility.py`.
