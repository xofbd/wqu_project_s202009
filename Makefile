SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate
MAX_LINE_LENGTH_FLAKE := 88
OUTPUTS = $(wildcard requirements/*.txt) requirements.txt

.DELETE_ON_ERROR:
.PHONY: all deploy tests test-unit test-flake8 clean

all: clean deploy

# Environments
venv:
	python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r requirements/pip-tools.txt

.base: requirements/base.txt venv
	$(ACTIVATE_VENV) && pip-sync $<
	rm -f .dev
	touch .base

base: .base

.dev: requirements/dev.txt requirements/base.txt venv
	$(ACTIVATE_VENV) && pip-sync $(word 1, $^) $(word 2, $^)
	rm -f .base
	touch .dev

dev: .dev

requirements: $(OUTPUTS)

requirements/%.txt: requirements/%.in venv
	$(ACTIVATE_VENV) && pip-compile $<

requirements/dev.txt: requirements/base.txt

requirements.txt: .base
	$(ACTIVATE_VENV) && pip freeze > $@

# Deployment
deploy: .base
	$(ACTIVATE_VENV) && bin/run_app

# Utility
tests: test-unit test-flake8

test-unit: .dev
	$(ACTIVATE_VENV) && pytest -v tests

test-flake8: .dev
	$(ACTIVATE_VENV) && flake8 --max-line-length $(MAX_LINE_LENGTH_FLAKE) wqu_app

clean:
	rm -rf venv
	rm -rf .base .dev
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
