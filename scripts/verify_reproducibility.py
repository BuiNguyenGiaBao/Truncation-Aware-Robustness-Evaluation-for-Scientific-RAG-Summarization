#!/usr/bin/env python3
from pathlib import Path
import sys

required = [
    "README.md",
    "configs/reported_run.yaml",
    "docs/REPRODUCIBILITY.md",
    "docs/DATASET_RECONSTRUCTION.md",
    "docs/ARTIFACTS.md",
    "docs/ENVIRONMENT.md",
    "docs/NOISE_POOL_ALIGNMENT.md",
    "requirements.in",
    "src/databuildt.py",
    "src/eval.py",
    "src/train/train_bart_t5_runpod.py",
    "metrics/metrics_full/eval_config_rankB.json",
    "metrics/metrics_full/rankB_metrics_summary.csv",
    "metrics/metrics_full/rankB_paired_noiseaware_vs_clean.csv",
    "metrics/metrics_full/rankB_truncation_summary.csv",
]

missing = [p for p in required if not Path(p).exists()]

print("Reproducibility file check")
print("=" * 32)
for p in required:
    print(("[OK]   " if Path(p).exists() else "[MISS] ") + p)

cfg = Path("configs/reported_run.yaml")
if cfg.exists():
    txt = cfg.read_text(encoding="utf-8", errors="replace")
    if "MUST_VERIFY_BEFORE_RESUBMISSION" in txt:
        print("\n[BLOCKER] Noise-pool strategy is still unverified in configs/reported_run.yaml")
        missing.append("VERIFY_NOISE_POOL_STRATEGY")

readme = Path("README.md")
if readme.exists():
    txt = readme.read_text(encoding="utf-8", errors="replace")
    if "\n=======\n" in txt or "<<<<<<<" in txt or ">>>>>>>" in txt:
        print("\n[BLOCKER] README contains merge-conflict/duplicate markers.")
        missing.append("FIX_README_MERGE_CONFLICT")

if missing:
    print("\nStatus: NOT READY FOR RESUBMISSION")
    sys.exit(1)

print("\nStatus: BASIC REPRODUCIBILITY FILE CHECK PASSED")
