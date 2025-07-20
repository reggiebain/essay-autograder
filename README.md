
# 📝 Automated Essay Grading API

This project is a full-featured, containerized FastAPI application that uses OpenAI's language models to automatically grade student essays based on a customizable rubric. It includes an SDK, batch grading script, continuous integration, and optional GitHub Actions testing support.

## 🚀 Features

- 🔧 **FastAPI** backend for real-time grading
- 🧠 **LLM-based scoring** using OpenAI's API
- 📂 **Batch grading support** for PDF and Word documents
- 🔒 **API key authentication**
- 🧪 **Pytest test suite** with optional CI token skipping
- 🐳 **Dockerized** for portability and reproducibility
- 📄 **Markdown docs** and `.env` configuration
- 📈 **CSV or pickle** output with structured rubric scores

---

## 📁 Project Structure

```
review-classifier-deploy/
├── api/                # FastAPI app
│   ├── main.py         # API entrypoint
│   ├── grader.py       # Core grading logic
├── scripts/
│   └── batch_grade.py  # Batch grading script for essays
├── essays/             # Student folders with PDFs/DOCs
├── tests/              # Pytest-based test suite
├── .env                # API keys and config variables
├── requirements.txt    # Python dependencies
├── Dockerfile          # Image definition
├── Makefile            # Automation for linting/testing
├── README.md           # This file
└── .github/workflows/
    └── ci.yml          # GitHub Actions test workflow
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/review-classifier-deploy.git
cd review-classifier-deploy
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` to include:

```env
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_local_api_key
```

---

## 🐳 Run the API (Docker)

```bash
docker build -t essay-grader .
docker run -p 8000:8000 --env-file .env essay-grader
```

The API will be available at `http://localhost:8000`.

---
---
## Run the API (Local)
```bash
make install     # once per machine
make run         # starts the API
make grade       # evaluates essays
make print       # get csv of simplified grades
```
The API will be available at `http://localhost:8000`.

## 🧪 Run Tests

To run tests **without calling the OpenAI API**:

```bash
SKIP_OPENAI_CALLS=true make test
```

To test normally (requires OpenAI key):

```bash
make test
```

---

## 🗃 Batch Grading from Essays Folder

### Folder format

Each folder in the `essays/` directory should be named after the student and contain their PDF or DOCX files.

```
essays/
├── smith--jane/
│   └── smith_jane_essay.docx
├── lee--chris/
│   └── lee_chris_essay.pdf
```

### Run the batch grader

```bash
make grade
make print
```

This will:

- Extract text from each document
- Send it to the API
- Return rubric scores and feedback
- Save the results as a `.pkl` file (preserving types)
- Make a nicely formatted CSV file simplified with student names and total scores
- Make a histogram of the scores.
---

## 📊 Output Example

```python
import pandas as pd
import pickle

with open("graded_essays.pkl", "rb") as f:
    data = pickle.load(f)

df = pd.DataFrame(data)
print(df.head())
```

| student        | filename         | Accuracy_score | Argument_score | ... | Mechanics_score |
|----------------|------------------|----------------|----------------|-----|-----------------|
| smith--jane    | jane_essay.pdf   | 3              | 2              | ... | 3               |
| lee--chris     | chris_essay.docx | 2              | 2              | ... | 2               |

---

## ⚙️ CI/CD with GitHub Actions

Tests automatically run on pull requests and pushes to `main`. The CI skips OpenAI calls unless the token is explicitly provided in GitHub Secrets (`OPENAI_API_KEY`).

---

## 🔐 Authentication

All grading requests require an API key:

```http
POST /grade
x-api-key: your_local_api_key
```

---

## 📌 Future Improvements

- Add user roles and dashboards
- Integrate rubric editing UI
- Caching / deduplication of essay scores
- Web front-end for drag-and-drop batch grading

---

## 🧠 Example Use Cases

- Automating high school or college writing assessment
- Portfolio evidence collection for education programs
- Rapid SLO-based program evaluation

---

## 📄 License

MIT License


## How to run
```
make install     # once per machine
make run         # starts the API
make grade       # evaluates essays
make print       # get csv of simplified grades
```

## Sample Rubric Entry
```
{
  "rubric": {
    "Accuracy": {
      "3": "Factual content is correct and comprehensive.",
      "2": "Mostly correct but with minor inaccuracies.",
      "1": "Major factual errors or missing key information."
    },
    "Argument": {
      "3": "Clear, well-supported argument throughout.",
      "2": "Argument present but inconsistently supported.",
      "1": "Argument is unclear or missing."
    },
    "Conclusions & Extensions": {
      "3": "Draws insightful conclusions or goes beyond prompt.",
      "2": "Basic conclusions relevant to the prompt.",
      "1": "No conclusion or completely off-topic."
    },
    "Mechanics": {
      "3": "Flawless grammar, spelling, and punctuation.",
      "2": "Some errors that don't impede understanding.",
      "1": "Frequent or distracting language issues."
    }
  }
}
```