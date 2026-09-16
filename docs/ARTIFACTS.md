# Released Artifacts

Expected public artifacts under `metrics/metrics_full/`:

```text
eval_config_rankB.json
predictions/
rankB_additive_vs_substitutive.csv
rankB_all_metrics_tables.xlsx
rankB_compact_paper_table.csv
rankB_metrics_record_level.csv
rankB_metrics_summary.csv
rankB_paired_noiseaware_vs_clean.csv
rankB_retrieval_summary.csv
rankB_robustness_degradation.csv
rankB_truncation_summary.csv
```

These files support checking:

- paper-level aggregate metrics;
- record-level metrics;
- paired checkpoint statistics;
- truncation diagnostics;
- robustness degradation;
- additive/substitutive comparisons.

Large model checkpoints and processed JSONL files do not need to be committed to Git if they can be reconstructed from the source corpus using the released scripts and exact configuration.
