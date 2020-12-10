SHELL := /bin/bash
MAX_LINE_LENGTH_FLAKE := 88

.PHONY: all deploy tests test-unit test-flake8 clean

all: clean deploy

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	touch venv

deploy: venv
	source venv/bin/activate && bin/run_app

tests: test-unit test-flake8

test-unit: venv
	source venv/bin/activate && pytest -v tests

test-flake8: venv
	source venv/bin/activate && flake8 --max-line-length $(MAX_LINE_LENGTH_FLAKE) wqu_app

clean:
	rm -rf venv
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
