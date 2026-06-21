# E-Commerce Test Automation Framework

## Overview

End-to-end test automation framework built with Python, Selenium, and Pytest. It demonstrates UI testing, API testing, database validation, and integration testing across all three layers, with cross-browser CI/CD execution via GitHub Actions.

The framework follows the Page Object Model (POM), is safe to run under `pytest-xdist` (each worker gets its own SQLite file), and supports cross-browser execution across Chrome, Firefox, and Edge.

---

## Tech Stack

* Python
* Selenium WebDriver
* Pytest
* Requests
* SQLite
* GitHub Actions
* Allure Reporting
* Docker
* Ruff / Black / pre-commit

---

## Features

### UI Automation

* Selenium WebDriver
* Page Object Model (POM), wired up as pytest fixtures (`login_page`, `products_page`, `cart_page`)
* Explicit waits, no `time.sleep`
* Cross-browser testing (Chrome, Firefox, Edge)

### Test Framework

* Pytest fixtures for driver lifecycle, page objects, and credentials
* Custom CLI options: `--browser`, `--headless`, `--env`
* Test markers: `smoke`, `regression`, `ui`, `api`, `db`
* Data-driven testing via `data/test_data.json`
* Auto-retry on network-flaky external API tests (`pytest-rerunfailures`)
* Parallel execution support via `pytest-xdist`

### API Testing

* REST API validation using `requests` (happy-path and 404 cases)

### Database Testing

* SQLite persistence validation
* UI + API + DB integration testing in a single flow

### Reporting & Logging

* HTML reports (`pytest-html`)
* Allure reporting
* Screenshot capture on UI test failure (skipped safely for non-UI tests)
* Per-run, per-worker file logging under `logs/<run-id>/<worker>.log`

### CI/CD

* GitHub Actions: lint gate -> cross-browser test matrix
* Push / PR smoke validation, nightly scheduled regression
* `fail-fast: false` so one browser failing doesn't cancel the others
* Allure results + HTML report + failure screenshots uploaded as artifacts
* Dependency caching

### Containerization

* `Dockerfile` for running the smoke suite in a container (Chromium headless)

---

## Project Structure

```text
ecom_test/

├── .github/
│   └── workflows/
│       └── regression.yml
│
├── config/
│   └── config.json
│
├── data/
│   ├── product_mapping.py
│   └── test_data.json
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── products_page.py
│   └── cart_page.py
│
├── tests/
│   ├── api_tests/
│   ├── integration_tests/
│   ├── ui_tests/
│   └── conftest.py
│
├── utils/
│   ├── config_reader.py
│   ├── db_utils.py
│   ├── driver_manager.py
│   ├── logger.py
│   └── paths.py
│
├── Dockerfile
├── Makefile
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── setup_db.py
└── README.md
```

---

## Setup

```bash
pip install -r requirements-dev.txt   # runtime + lint/format tooling
python setup_db.py                    # provisions the local SQLite cart table
```

## Credentials

Tests default to SauceDemo's public demo credentials (`standard_user` / `secret_sauce`). To override (e.g. for a different environment), set:

```bash
export TEST_USERNAME=standard_user
export TEST_PASSWORD=secret_sauce
```

## Test Markers

```bash
pytest -m smoke
pytest -m regression
pytest -m ui
pytest -m api
pytest -m db
```

## Custom Execution Options

```bash
pytest --browser chrome        # chrome | firefox | edge
pytest --headless
pytest --env qa                # qa | staging
pytest -m smoke --headless
pytest -n auto --headless      # parallel execution; DB layer is worker-isolated
```

## Linting / Formatting

```bash
make lint     # ruff check + black --check
make format   # ruff --fix + black
```

Optionally enable as a git hook: `pre-commit install`.

## Reporting

```bash
pytest --alluredir=allure-results --html=report.html --self-contained-html
allure serve allure-results     # requires the Allure CLI
```

## Docker

```bash
docker build -t ecom-test .
docker run --rm ecom-test
```

---

## CI/CD Workflow

GitHub Actions is configured to:

* Run a `lint` job (ruff + black) that gates the test matrix
* Execute Smoke Tests on Push / Pull Request
* Execute Regression Tests on the nightly schedule
* Run across Chrome, Firefox, and Edge without one browser's failure cancelling the others
* Upload the Allure results, HTML report, and failure screenshots as artifacts

---

## Sample Test Coverage

### UI Tests

* Login validation (happy path + invalid credentials)
* Add product to cart, cart verification
* Empty-cart state

### API Tests

* Product list retrieval
* 404 handling for a non-existent product

### Integration Tests

* UI action -> external API cross-check -> SQLite persistence, data-driven over `data/test_data.json`
* DB-only cart-clearing validation

---

## Future Enhancements

* Jenkins integration
* Selenium Grid / cloud execution
* Allure report publishing (e.g. GitHub Pages) instead of raw artifact upload

---

## Author

Abhishek Kumar

Automation framework built for learning and demonstrating real-world QA automation, API testing, database validation, and CI/CD practices.
