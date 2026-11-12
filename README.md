# Log Classification

A compact toolkit to classify log messages using multiple strategies: regular expressions, a BERT-based classifier, or an LLM-based classifier (Groq). This project is intended as a starting point for building a production-ready log-labeling pipeline.

---

## 🚀 Features
- Rule-based classification via `processor_regex.py` (fast, deterministic)
- ML-based classification via BERT (`processor_bert.py`) using sentence-transformers and a saved classifier
- LLM-assisted classification via Groq (`processor_llm.py`) for ambiguous cases
- Simple CSV input/output pipeline via `classify.py`

---

## ✅ Quickstart (Windows and cross-platform)
### 1) Create & activate a virtual environment (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
(Unix / macOS)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure environment variables (DON'T commit secrets)
- `GROQ_API_KEY` — Groq API key for LLM classification (optional if not using LLM)
- `LOG_CLASSIFIER_MODEL_PATH` — path to `log_classifier.joblib` (optional, overrides hardcoded path)

Example (PowerShell):
```powershell
$env:GROQ_API_KEY = "<your-groq-key>"
$env:LOG_CLASSIFIER_MODEL_PATH = "C:\models\log_classifier.joblib"
```

### 4) Prepare input CSV
Create `resources/test.csv` with columns: `source` and `log_message`.
Example:
```csv
source,log_message
BillingSystem,User 12345 logged in.
ModernCRM,IP 192.168.1.2 blocked due to potential attack
```

### 5) Run classification
```powershell
python classify.py
```
- Default behavior: reads `resources/test.csv` and writes `resources/output.csv` with an added `target_label` column.

---

## 🔧 Usage details
- `classify.py`
  - `classify_csv(input_file)` reads CSV, classifies messages, writes `resources/output.csv`.
  - `classify(logs)` classifies an iterable of (source, log_message) pairs.

- `processor_regex.py`
  - Fast pattern matching; recommended as the first pass.

- `processor_bert.py`
  - Uses `sentence-transformers` to create embeddings and a pre-trained classifier stored as a `.joblib` file.
  - Configure via `LOG_CLASSIFIER_MODEL_PATH` env var. Currently the repo contains a placeholder for a hardcoded model path — consider changing this to lazy-load and configurable path.

- `processor_llm.py`
  - Calls Groq chat completion; ensure `GROQ_API_KEY` is set and the model/network usage is acceptable for your costs.

---

## 🛠️ Troubleshooting & common issues
- If you see ImportError or FileNotFoundError from `processor_bert.py`, ensure `LOG_CLASSIFIER_MODEL_PATH` points to a valid `.joblib` model file.
- If LLM calls fail, verify `GROQ_API_KEY` and network connectivity. Add timeouts around API calls if needed.
- If `resources/output.csv` doesn't appear, confirm `resources/test.csv` exists and has the required columns.

---

## 🔒 Security note (urgent)
A Groq API key was found in the repository's `.env`. **Please rotate that key immediately** and remove it from the git history if it was committed.
To untrack and remove `.env` from the repo:
```bash
# stop tracking .env but keep a local copy
git rm --cached .env
git commit -m "Remove .env from repository"
# add .env to .gitignore (already included)
```
If the secret was committed in past commits, consider using the BFG Repo-Cleaner or git-filter-repo to remove it from history and rotate credentials.

---

## ✅ Recommended next steps (I can implement)
- [ ] Standardize labels (constants or Enum) across processors
- [ ] Fix `classify_csv` so it writes only label strings and create output dirs as needed
- [ ] Replace hardcoded paths and validate env vars at runtime (lazy-load models)
- [ ] Add unit tests and a CI workflow (GitHub Actions)
- [ ] Add a small CLI (argparse or Typer) and examples

---

## Contributing
Contributions welcome. Please open an issue or a PR describing your change. If you add sensitive keys to local `.env`, do not commit them.

---

## License & Contact
- License: MIT (unlicensed files assume permissive usage; add a `LICENSE` file to be explicit)
- Maintainer: Sumair Salam — open an issue / PR on the repository

---

If you'd like, I can commit this change and push it to your GitHub repository (https://github.com/SumairSalam/log-classification.git). Reply with 'push' to proceed with committing and pushing the updated README, or 'no push' to keep the change local.