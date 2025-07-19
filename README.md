# Essay Autograder
An easy way to check your essay on a given rubric for iteratively improving your writing.

## File Structure
```
essay-grader-api/
├── api/                      # FastAPI app
│   ├── __init__.py
│   ├── main.py               # API entry point
│   ├── models.py             # Request/response schemas
│   ├── grader.py             # LLM interaction logic
│   └── config.py             # Env/config loader
├── tests/                    # Test cases
│   └── test_grader.py
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container instructions
├── .dockerignore             # Files to ignore in Docker
├── .env                      # API keys and config (never commit this)
└── README.md                 # Project overview
```

## Sample Entry
```
{
  "essay": "The Roman Empire fell because...",
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