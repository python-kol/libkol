.PHONY: test install install-dev

export PATH := $(HOME)/.local/bin:$(PATH)

test:
	python -m unittest test/**/test_*.py

coverage:
	coverage run -m unittest test/**/test_*.py
	coverage report
	coverage html
	coverage-badge -o htmlcov/coverage.svg

dev:
	pip install -r requirements.dev.txt
	pip install -e .

install:
	pip install -r requirements.txt --user

install-dev:
	pip install -r requirements.dev.txt --user

package:
	python setup.py sdist
	python setup.py bdist_wheel


ifndef CI
	pre-commit install
endif
