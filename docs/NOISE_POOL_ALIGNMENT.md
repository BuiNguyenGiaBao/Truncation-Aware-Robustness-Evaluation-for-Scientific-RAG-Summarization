# Noise-Pool Alignment — Action Required Before Resubmission

This is the main unresolved reproducibility issue detected in the current public repository.

## Current manuscript description

The manuscript currently describes a global cross-document distractor pool derived from the training split and reused across noisy train/validation/test construction.

## Current public builder

`src/databuildt.py` currently supports:

```text
--noise_pool_strategy heldout_train_tail
--noise_pool_strategy legacy_train_pool
```

The current default is:

```text
heldout_train_tail
```

The builder also supports a separate test distractor pool through arguments such as:

```text
--test_noise_pool_offset
--test_noise_pool_limit
```

## Why this matters

If the reported Tables 4–8 were generated with the older shared/legacy training pool, then the current default builder does not reproduce the exact reported experiment.

If the reported tables were generated with the held-out strategy, then the manuscript description must be updated.

## Required action

Before resubmission, identify which strategy was used by the run that generated the released metrics.

### If the reported run used the legacy/shared training pool

1. Set the reproduction command to `--noise_pool_strategy legacy_train_pool`.
2. Ensure the test construction uses the same pool behavior as the reported run.
3. Keep the manuscript description aligned with that strategy.
4. Update `configs/reported_run.yaml` so `noise_pool.status` is no longer `MUST_VERIFY_BEFORE_RESUBMISSION`.

### If the reported run used held-out train-tail / separate test pool

1. Keep `heldout_train_tail`.
2. Record exact offsets and pool limits in `configs/reported_run.yaml`.
3. Revise the manuscript description in Section IV-B.
4. Ensure README and response-to-reviewer use the same wording.

Do not submit the revision while manuscript, README, and builder describe different noise-pool strategies.
