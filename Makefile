# makefile for essay-grader

install:
	pip install -r requirements.txt

run:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=. pytest tests/

docker-build:
	docker build -t essay-autograder .

docker-run:
	docker run -p 8000:8000 --env-file .env essay-autograder

format:
	black .

type-check:
	mypy .

# Grade all essays and save to CSV
grade:
	python batch_grade.py

# Full setup + run server + grade
all: install run grade

