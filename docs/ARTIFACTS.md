# Released Experimental Artifacts

The repository should expose the aggregate artifacts used to check the manuscript tables whenever those files are available.

Recommended/expected artifact directory:

```text
metrics/metrics_full/
```

The current study refers to the following artifact types:

| Artifact | Purpose |
|---|---|
| `eval_config_rankB.json` | Machine-readable evaluation configuration |
| `rankB_metrics_summary.csv` | Aggregate quality metrics |
| `rankB_metrics_record_level.csv` | Per-sample evaluation metrics |
| `rankB_paired_noiseaware_vs_clean.csv` | Paired checkpoint comparison |
| `rankB_robustness_degradation.csv` | Clean/noisy trade-off |
| `rankB_additive_vs_substitutive.csv` | Additive vs. substitutive comparison |
| `rankB_retrieval_summary.csv` | Retrieval/context diagnostics |
| `rankB_truncation_summary.csv` | Model-specific truncation diagnostics |
| `rankB_all_metrics_tables.xlsx` | Consolidated paper-level tables |
| `predictions/` | Generated summaries if released |

## Minimum reproducibility expectation

At minimum, the public repository should make it possible to regenerate:

1. clean / additive / substitutive evaluation contexts;
2. the four reported model checkpoints;
3. generated summaries;
4. ROUGE and BERTScore tables;
5. truncation diagnostics;
6. paired statistical comparisons.

## Large files

Large processed JSONL files and checkpoints do not need to be committed to Git if they can be reconstructed from the source corpus using released scripts and fixed configuration.

If large artifacts are hosted elsewhere, add stable download instructions and checksums here.

## Provenance limitation

The current artifacts do not contain post-truncation target/noise token provenance. Do not claim empirical NER/TRR from these aggregate files.
