# E-Commerce Test Automation Framework

[![CI](https://github.com/abhisekcode/ecom-test-automation/actions/workflows/regression.yml/badge.svg)](https://github.com/abhisekcode/ecom-test-automation/actions/workflows/regression.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Selenium](https://img.shields.io/badge/selenium-4.x-43B02A)
![Pytest](https://img.shields.io/badge/pytest-9.x-0A9EDC)

An end-to-end test automation framework against a live e-commerce demo app
(SauceDemo), covering UI, API, and database layers in one suite, with a
real CI/CD pipeline behind it - not just a script that runs locally.

## Why this is more than a Selenium tutorial clone

* **Parallel-safe by design** - the SQLite persistence layer gives each
  `pytest-xdist` worker its own database file, so `pytest -n auto` doesn't
  race or corrupt state across workers.
* **CI that actually gates on quality** - a `lint` job (Ruff + Black) has
  to pass before the cross-browser test matrix even runs, and
  `fail-fast: false` means one browser's failure never hides the other
  two's results.
* **Negative paths, not just happy paths** - invalid login, empty-cart
  state, and API 404 handling are all covered, not just "click button,
  assert success."
* **Debugged with evidence, not guesses** - every fix in this repo's
  history was reproduced and re-verified against the live app/API before
  being called done, including a CI failure traced to a misencoded
  `requirements.txt` and a failure-screenshot hook that was silently
  swallowing real test failures behind an unrelated crash.

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
ecom-test-automation/

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

## Quickstart

```bash
git clone https://github.com/abhisekcode/ecom-test-automation.git
cd ecom-test-automation
pip install -r requirements-dev.txt   # runtime + lint/format tooling
python setup_db.py                    # provisions the local SQLite cart table
pytest -m smoke --headless
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

* Run a `lint` job (Ruff + Black) that gates the test matrix
* Execute smoke tests on push / pull request
* Execute regression tests on the nightly schedule
* Run across Chrome, Firefox, and Edge without one browser's failure cancelling the others
* Upload the Allure results, HTML report, and failure screenshots as artifacts

---

## Test Coverage

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

**Abhishek Kumar** - [@abhisekcode](https://github.com/abhisekcode)

Built to practice and demonstrate real-world QA automation, API testing, database validation, and CI/CD engineering.
