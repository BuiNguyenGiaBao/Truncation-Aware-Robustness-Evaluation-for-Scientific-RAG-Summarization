#!/usr/bin/env python3
from pathlib import Path
import sys

required = [
    "README.md",
    "CITATION.cff",
    "configs/reported_run.yaml",
    "docs/REPRODUCIBILITY.md",
    "docs/SOURCE_DATA_PREPARATION.md",
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

problems = []

print("HUFLIT reproducibility consistency check")
print("=" * 42)

for p in required:
    ok = Path(p).exists()
    print(("[OK]   " if ok else "[MISS] ") + p)
    if not ok:
        problems.append(f"missing:{p}")

def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace") if Path(p).exists() else ""

readme = read("README.md")
cfg = read("configs/reported_run.yaml")
citation = read("CITATION.cff")
noise_doc = read("docs/NOISE_POOL_ALIGNMENT.md")
repro = read("docs/REPRODUCIBILITY.md")
builder = read("src/databuildt.py")

if any(x in readme for x in ["<<<<<<<", "\n=======\n", ">>>>>>>"]):
    problems.append("README_merge_conflict")

if "Tran Le Van" in readme or ('given-names: "Le Van"' in citation):
    problems.append("obsolete_author_Tran_Le_Van")

if "MUST_VERIFY_BEFORE_RESUBMISSION" in cfg:
    problems.append("obsolete_noise_pool_blocker")

if 'strategy: "shared_training_pool"' not in cfg:
    problems.append("reported_run_missing_shared_training_pool")

if "heldout_train_tail" in noise_doc:
    problems.append("obsolete_heldout_noise_pool_doc")

if "SOURCE_DATA_PREPARATION.md" not in repro:
    problems.append("repro_doc_missing_source_prep_boundary")

if "databuild_huflit_shared_pool.py" in builder:
    problems.append("builder_docstring_old_filename")

print()
if problems:
    print("Status: NOT READY")
    for p in problems:
        print(" -", p)
    sys.exit(1)

print("Status: BASIC CONSISTENCY CHECK PASSED")
print("Note: this does not prove byte-identical historical processed-data reconstruction.")
