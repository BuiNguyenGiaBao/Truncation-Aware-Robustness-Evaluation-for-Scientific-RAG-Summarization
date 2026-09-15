# Environment and Package Versions

## Important

The exact package versions from the original reported run were not preserved in the materials currently available for this revision.

Do **not** invent or backfill package versions from a different experiment.

## Packages required by the pipeline

The project requires the following package families:

```text
torch
transformers
datasets
evaluate
sentence-transformers
faiss-cpu or faiss-gpu
numpy
pandas
scipy
scikit-learn
rouge-score
bert-score
tqdm
pyyaml
openpyxl
```

A non-pinned package list is provided in `requirements.in`.

## Best way to complete exact environment reproducibility

If the original RunPod environment or logs are still available, run:

```bash
python --version
pip freeze > requirements.txt
```

Also record:

```bash
nvidia-smi
python -c "import torch; print(torch.__version__); print(torch.version.cuda)"
python -c "import transformers; print(transformers.__version__)"
```

Then commit the recovered `requirements.txt` to the repository.

## If the exact environment cannot be recovered

Keep this document and `requirements.in`, and state transparently in the manuscript/repository that exact historical package versions were not preserved.

This is preferable to reporting guessed versions.
