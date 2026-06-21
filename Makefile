.PHONY: install test smoke regression lint format report

install:
	pip install -r requirements-dev.txt

smoke:
	pytest -m smoke --headless

regression:
	pytest -m regression --headless

test:
	pytest --headless

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

report:
	pytest --alluredir=allure-results --headless
	allure generate allure-results -o allure-report --clean
