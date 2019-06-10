test:
	python -m unittest libkol/test/**/test_*.py

install:
	pre-commit install
	pip install -r requirements.txt
