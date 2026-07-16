# Tokenizer Benchmark

A lightweight benchmarking tool for comparing how efficiently different tokenizers encode multilingual datasets.

The goal of this project is to provide a simple and extensible framework for evaluating tokenizer performance across different languages and domains.

Typical questions this benchmark can help answer include:

* Which tokenizer performs best on Hindi?
* How efficiently do modern tokenizers handle Indic languages?
* How much improvement does `o200k_base` provide over `gpt2`?
* How do Hugging Face tokenizers compare with TikToken encodings?
* Does tokenizer efficiency change across different domains such as programming or medical terminology?

---

# Design Goals

The project is intentionally designed around a few simple principles:

* Keep datasets easy to contribute.
* Make adding new languages straightforward.
* Support multiple tokenizer implementations.
* Continue benchmarking even if individual tokenizers fail.
* Produce reproducible and comparable results.
* Keep the architecture modular and easy to extend.

---

# Features

* Compare multiple tokenizers in a single run.
* Support for **TikToken** and **Hugging Face** tokenizers.
* Easily add new languages.
* Easily add new datasets.
* JSON-based configuration.
* Console output.
* Export results as TXT.
* Export results as CSV.
* Gracefully skips unavailable tokenizers instead of aborting the benchmark.
* Modular architecture for adding new tokenizer implementations.

---

# Project Structure

| Path                           | Purpose                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------- |
| **main.py**                    | Entry point of the application. Loads the configuration and starts the benchmark. |
| **README.md**                  | Project documentation.                                                            |
| **requirements.txt**           | Python dependencies required to run the project.                                  |
| **benchmark/**                 | Core benchmark package containing the application logic.                          |
| ├── **__init__.py**            | Marks the directory as a Python package.                                          |
| ├── **runner.py**              | Coordinates the benchmark workflow.                                               |
| ├── **config.py**              | Loads and validates the benchmark configuration.                                  |
| ├── **dataset_loader.py**      | Loads datasets and validates language alignment.                                  |
| ├── **tokenizer_factory.py**   | Creates tokenizer instances from the configuration.                               |
| ├── **report.py**              | Generates console, TXT and CSV reports.                                           |
| └── **tokenizers/**            | Tokenizer implementations.                                                        |
|     ├── **__init__.py**        | Marks the directory as a Python package.                                          |
|     ├── **base.py**            | Defines the tokenizer interface.                                                  |
|     ├── **tiktoken.py**        | TikToken adapter.                                                                 |
|     └── **huggingface.py**     | Hugging Face adapter.                                                             |
| **configs/**                   | Configuration files.                                                              |
| ├── **benchmark.json**         | Benchmark configuration used by the application.                                  |
| └── **benchmark.example.json** | Example configuration with available options.                                     |
| **datasets/**                  | Contains benchmark datasets.                                                      |
| ├── **common100/**             | Top 100 aligned words.                                                            |
| ├── **common1000/**            | Top 1000 aligned words.                                                           |
| └── **programming/**           | Programming terminology dataset.                                                  |
| **output/**                    | Generated benchmark reports.                                                      |

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
cd tokenizer-benchmark
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

# Running

Run using the default configuration.

```bash
python main.py
```

Or specify a custom configuration.

```bash
python main.py --config configs/benchmark.json
```

---

# Configuration

The benchmark is configured using a JSON file.

Example:

```json
{
    "dataset": "common1000",

    "languages": [
        "english",
        "hindi",
        "punjabi"
    ],

    "tokenizers": [
        "gpt2",
        "cl100k_base",
        "o200k_base",

        {
            "type": "huggingface",
            "name": "sarvam",
            "model": "sarvamai/sarvam-m",
            "trust_remote_code": true,
            "fix_mistral_regex": true
        }
    ],

    "output": {
        "directory": "output",
        "console": true,
        "txt": true,
        "csv": true
    }
}
```

---

# Datasets

Datasets are organized by domain.

```
datasets/

    common100/

    common1000/

    programming/

    medical/

    legal/
```

Each dataset contains one file per language.

Example:

```
common1000/

    english.txt

    hindi.txt

    punjabi.txt
```

---

# Dataset Format

Each language file contains a space-separated list of words.

Example:

```
English

house water food
```

```
Hindi

घर पानी खाना
```

```
Punjabi

ਘਰ ਪਾਣੀ ਖਾਣਾ
```

## Important

The benchmark assumes that every language file is **aligned by meaning**.

For example:

| English | Hindi | Punjabi |
| ------- | ----- | ------- |
| house   | घर    | ਘਰ      |
| water   | पानी  | ਪਾਣੀ    |
| food    | खाना  | ਖਾਣਾ    |

Every language file must:

* Contain the same number of words.
* Preserve the same ordering.
* Represent the same meaning at each position.

The benchmark validates the word count but **cannot verify semantic alignment**.

---

# Adding a New Language

Suppose you want to add Gujarati.

Create

```
datasets/common1000/gujarati.txt
```

Populate it using the same word order as every other language.

Update the configuration.

```json
{
    "languages": [
        "english",
        "hindi",
        "punjabi",
        "gujarati"
    ]
}
```

No Python code changes are required.

---

# Adding a New Dataset

Create a new directory.

```
datasets/

    programming/

        english.txt

        hindi.txt

        punjabi.txt
```

Update the configuration.

```json
{
    "dataset": "programming"
}
```

---

# Supported Tokenizers

## TikToken

The benchmark supports every encoding provided by TikToken, including:

* gpt2
* r50k_base
* p50k_base
* p50k_edit
* cl100k_base
* o200k_base
* o200k_harmony

---

## Hugging Face

Any tokenizer supported by `transformers.AutoTokenizer` can be used.

Example:

```json
{
    "type": "huggingface",
    "name": "gemma",
    "model": "google/gemma-3-1b-it"
}
```

Additional arguments accepted by `AutoTokenizer.from_pretrained()` may also be supplied.

Example:

```json
{
    "type": "huggingface",
    "name": "sarvam",
    "model": "sarvamai/sarvam-m",
    "trust_remote_code": true,
    "fix_mistral_regex": true
}
```

---

# Output

Console

```
Tokenizer      english  hindi  punjabi  french  
------------------------------------------------
gpt2           100      652    722      184     
cl100k_base    100      447    722      114     
o200k_base     100      115    215      101     
o200k_harmony  100      115    215      101     
sarvam         100      127    277      101     
```

TXT

```
output/benchmark.txt
```

CSV

```
output/benchmark.csv
```

---

# Error Handling

The benchmark distinguishes between fatal and recoverable errors.

## Fatal Errors

The benchmark stops execution if:

* Configuration file is missing.
* Dataset directory does not exist.
* A configured language file is missing.
* Language datasets have different word counts.

## Recoverable Errors

Individual tokenizer failures do **not** stop the benchmark.

Examples include:

* Invalid Hugging Face model.
* Repository unavailable.
* Network timeout.
* Authentication required.
* Unknown TikToken encoding.

Skipped tokenizers are reported at the end of the benchmark.

---

# Future Ideas

* Average characters per token.
* Bytes per token.
* Vocabulary coverage.
* Tokenization speed.
* Token boundary visualization.
* Sentence-level benchmarking.
* Domain-specific benchmark suites.
* Interactive HTML reports.
* Charts and visualizations.

---

# Contributing

Contributions are welcome.

Possible contributions include:

* New language datasets.
* Domain-specific datasets.
* Additional tokenizer adapters.
* Performance improvements.
* Bug fixes.
* Documentation improvements.

Before submitting a dataset, ensure that:

* Every language file contains the same number of words.
* Words remain aligned across languages.
* Files are UTF-8 encoded.
* Duplicate or missing entries are avoided.

---

# License

MIT License.
