# Log Classification

A Python project exploring three approaches to classifying application logs:

- **Regular expressions** for recognizable log patterns
- **Sentence-transformer embeddings** with a saved machine learning classifier
- **LLM classification** through the Groq API

The repository includes separate processors and a prototype CSV classification workflow.

## Project Overview

Application logs contain user actions, system notifications, security events, and workflow errors. This project explores how rules and language models can organize these messages into useful categories.

**Current implementation status:** The processors are separate modules. `classify.py` uses its own regex rules, a placeholder BERT function, and a keyword-based LLM simulation. It does not currently call the transformer or Groq processors.

## Technologies

| Technology | Purpose |
|------------|---------|
| Python | Classification logic |
| Regular expressions | Pattern matching |
| Pandas | CSV processing |
| Sentence Transformers | Log message embeddings |
| scikit-learn | Saved classifier interface |
| Joblib | Loading the trained classifier |
| Groq | LLM inference |
| python-dotenv | Environment variable loading |

## Classification Approaches

### 1. Regex Processor

`processor_regex.py` matches predefined patterns for events such as:

- User login and logout
- Backup operations
- File uploads
- System updates and reboots
- API requests
- Resource tracking
- Certificate errors
- Access control events
- Data format errors

Messages that do not match a pattern return `Other`.

### 2. Embedding-Based Processor

`processor_bert.py`:

1. Encodes a log message using `all-MiniLM-L6-v2`.
2. Loads a saved classifier through Joblib.
3. Obtains class probabilities.
4. Returns `unclassified` when the highest probability is below `0.5`.
5. Otherwise returns the predicted label.

The trained classifier is not included in the repository. Its expected class labels depend on the missing model artifact.

### 3. LLM Processor

`processor_llm.py` sends a log message to the Groq API and asks for one of:

- `Workflow Error`
- `Deprecation Warning`
- `Unclassified`

It requires a `GROQ_API_KEY`.

The configured model identifier is `llama3-70b-8192`. Verify its availability for your Groq account and update it if necessary.

## Repository Contents

| File | Description |
|------|-------------|
| `classify.py` | Prototype routing logic and CSV processing |
| `processor_regex.py` | Standalone regex classifier |
| `processor_bert.py` | Sentence embeddings and saved classifier inference |
| `processor_llm.py` | Groq-based classification |
| `requirements.txt` | Dependency declarations |
| `main.py` | Default PyCharm starter script |
| `Untitled.ipynb` | Empty notebook |

## Current Routing in `classify.py`

| Source / Condition | Behavior |
|--------------------|----------|
| Source is exactly `LegacyCRM` | Uses local keyword-based classification |
| Other sources with a regex match | Returns the matching category |
| Other sources without a match | Calls the placeholder BERT function, which returns `Other` |

The local regex categories include:

- `Security Alert`
- `User Action`
- `System Notification`
- `Deprecation Warning`
- `Workflow Error`

These rules differ from those in `processor_regex.py`.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SumairSalam/log-classification.git
cd log-classification
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The requirements combine older machine learning packages with additional version constraints. Installation compatibility may require adjustments for your Python version and platform.

For the standalone regex processor, no third-party packages are required.

## Usage

### Run the Regex Examples

```bash
python processor_regex.py
```

Or import the function:

```python
from processor_regex import classify_with_regex

message = "Backup completed successfully."
label = classify_with_regex(message)

print(label)
# System Notification
```

### Use the Prototype Classifier

Install Pandas if you have not installed the full requirements:

```bash
python -m pip install pandas
```

Then classify a list of source/message pairs:

```python
from classify import classify

logs = [
    ("BillingSystem", "User 12345 logged in."),
    ("ModernCRM", "IP address blocked due to potential attack"),
    ("AnalyticsEngine", "Backup completed successfully."),
    ("LegacyCRM", "Invoice generation process aborted."),
]

for source, label, message in classify(logs):
    print(f"[{source}] {label}: {message}")
```

This example uses the local implementations in `classify.py`, not the standalone transformer or Groq processors.

### Use the Embedding-Based Processor

Before running `processor_bert.py`:

1. Obtain a compatible trained classifier.
2. Place it in a local `models` directory.
3. Replace the machine-specific Windows path with a project-relative path.

For example:

```python
from pathlib import Path

model_path = Path(__file__).resolve().parent / "models" / "log_classifier.joblib"
```

Then run:

```bash
python processor_bert.py
```

The sentence-transformer model requires an initial download unless it is already cached.

### Use the Groq Processor

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Verify the model identifier in `processor_llm.py`, then run:

```bash
python processor_llm.py
```

Never commit your API key or `.env` file.

Log messages passed to this processor are sent to the external API. Remove sensitive information before submitting them.

## CSV Classification

The intended input CSV contains:

| Column | Description |
|--------|-------------|
| `source` | Application or system name |
| `log_message` | Message to classify |

Example:

```csv
source,log_message
BillingSystem,User 12345 logged in.
AnalyticsEngine,Backup completed successfully.
LegacyCRM,Invoice generation process aborted.
```

The script expects input at `resources/test.csv` and writes to `resources/output.csv`. The `resources` directory and sample CSV are not included.

### Required Output Correction

Currently, `classify_csv()` assigns complete `(source, label, message)` tuples to the `target_label` column.

To store only labels, replace that assignment with:

```python
df["target_label"] = [
    classify_log(source, message)
    for source, message in zip(df["source"], df["log_message"])
]
```

Create the `resources` directory, add `test.csv`, apply the correction, and run:

```bash
python classify.py
```

## Current Limitations

- The trained classifier and datasets are missing.
- The standalone processors are not integrated into `classify.py`.
- The BERT function inside `classify.py` is a placeholder.
- The LLM function inside `classify.py` uses keywords rather than an API.
- Processor labels and fallback capitalization are inconsistent.
- The Groq response is not validated against the allowed categories.
- No training workflow, evaluation metrics, or automated test suite is included.
- FastAPI is listed as a dependency, but no API application is implemented.

## Future Improvements

- Integrate the standalone processors into one classification pipeline.
- Standardize category names and fallback behavior.
- Add a reproducible classifier training workflow.
- Include labeled sample data and evaluation results.
- Correct CSV output and support configurable file paths.
- Add API error handling and response validation.
- Add tests for routing, regex precedence, and fallback behavior.
- Provide a FastAPI endpoint for batch classification.

## Maintainer

[Sumair Salam](https://github.com/SumairSalam)
