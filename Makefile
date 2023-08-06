run:
	poetry run wordlefilegenerator/wordlefilegenerator.py

test:
	poetry run pytest

install-deps:
	poetry install

update-deps:
	poetry update

build:
	poetry build

.PHONY: run test install-deps update-deps build
