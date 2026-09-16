# Environment

Exact historical package versions from the original RunPod experiment should only be published if they can be recovered from the original environment or logs.

Do not copy versions from unrelated experiments.

Minimum package families:

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

If the original environment is available:

```bash
python --version
pip freeze > requirements.txt
nvidia-smi
python -c "import torch; print(torch.__version__); print(torch.version.cuda)"
python -c "import transformers; print(transformers.__version__)"
```
