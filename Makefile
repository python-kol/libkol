.PHONY: test install

test:
	python -m unittest test/**/test_*.py

install:
	pre-commit install
	pip install -r requirements.txt
