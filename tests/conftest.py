"""Shared pytest fixtures: CLI options, driver lifecycle, page objects, and failure screenshots."""

import os
import time
from datetime import datetime

import allure
import pytest
from pytest_html import extras

from pages.cart_page import CartPage
from pages.login_page import LogInPage
from pages.products_page import ProductsPage
from utils.config_reader import get_credentials
from utils.driver_manager import DriverManager
from utils.logger import get_logger
from utils.paths import PROJECT_ROOT

os.environ.setdefault("RUN_ID", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


# =========================
# CUSTOM CLI OPTIONS
# =========================


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests against")


# =========================
# ENV SETUP
# =========================


@pytest.fixture(scope="session", autouse=True)
def set_env(request):
    os.environ["TEST_ENV"] = request.config.getoption("--env")


# =========================
# AUTO TEST-BOUNDARY LOGGING
# =========================


@pytest.fixture(autouse=True)
def _log_test_boundaries(request):
    logger = get_logger()
    logger.info(f"START {request.node.nodeid}")
    yield
    logger.info(f"END {request.node.nodeid}")


# =========================
# DRIVER + PAGE OBJECT FIXTURES
# =========================


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drv = DriverManager.get_driver(browser, headless)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LogInPage(driver)


@pytest.fixture
def products_page(driver):
    return ProductsPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def credentials():
    username, password = get_credentials()
    return {"username": username, "password": password}


# =========================
# SCREENSHOTS ON FAILURE
# =========================


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extras", [])

    if report.when == "call" and report.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]

        screenshots_dir = PROJECT_ROOT / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)

        worker = os.getenv("PYTEST_XDIST_WORKER", "main")
        filename = screenshots_dir / f"{worker}_{item.name}_{int(time.time())}.png"

        driver.save_screenshot(str(filename))
        allure.attach.file(
            str(filename),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        extra.append(extras.image(str(filename)))
        print(f"\nScreenshot saved: {filename}")

    report.extras = extra
