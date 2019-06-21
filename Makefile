.PHONY: test install install-dev

export PATH := $(HOME)/.local/bin:$(PATH)

test:
	python -m unittest test/**/test_*.py

coverage:
	coverage run -m unittest test/**/test_*.py
	coverage report
	coverage html

install:
	pip install -r requirements.txt --user

install-dev:
	pip install -r requirements.txt --user
	pip install -r requirements.dev.txt --user
ifndef CI
	pre-commit install
endif
