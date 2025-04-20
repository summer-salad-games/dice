PYTHON=poetry run python
SRC_DIR=src
MAIN_MODULE=dice.entrypoint

.PHONY: install update lock format lint run clean

install:
	poetry install

update:
	poetry update

lock:
	poetry lock

format:
	poetry run black $(SRC_DIR)
	poetry run isort $(SRC_DIR)

lint:
	poetry run pylint $(SRC_DIR)

run:
	PYTHONPATH=$(SRC_DIR) $(PYTHON) -m $(MAIN_MODULE)

clean:
	poetry env remove python || echo "No virtual environment to remove."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
