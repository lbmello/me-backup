SHELL := /bin/bash

.PHONY: help
help:		## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build


.PHONY: python
python:		## Install python requirements
	@apt install python3-pip python3-venv

.PHONY: env
env: 		## Create virtual enviropment
	@poetry shell


.PHONY: poetry
poetry:	## upgrade pip and install poetry
	@pip install --upgrade pip
	@pip install poetry


.PHONY: install
install:	## install project via poetry
	@poetry install
