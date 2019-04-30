test:
	python -m pykollib.test.TestAll [username] [password]

install:
	pre-commit install
	pip install -r requirements.txt
