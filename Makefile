SHELL := /bin/bash

.PHONY: all tests clean

all: clean venv

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	touch venv

deploy: venv
	source venv/bin/activate && bin/run_app

tests: venv
	source venv/bin/activate && pytest -v tests

clean:
	rm -rf venv
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
