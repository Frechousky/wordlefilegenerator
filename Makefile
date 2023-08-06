# Variables
VENV			= .venv
VENV_PYTHON		= $(VENV)/bin/python
SYSTEM_PYTHON	= python3.11
PYTHON			= $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))

## Dev/build environment

$(VENV_PYTHON):
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV)

venv: $(VENV_PYTHON)

deps:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: venv deps

## Run/test

run:
	$(PYTHON) wordlefilegenerator/wordlefilegenerator.py

test:
	$(PYTHON) -m pytest

.PHONY: run test