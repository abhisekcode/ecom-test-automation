"""Builds a configured Selenium WebDriver for the requested browser."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

_CHROMIUM_HEADLESS_ARGS = (
    "--headless=new",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--window-size=1920,1080",
)

_CHROMIUM_BROWSERS = {
    "chrome": (webdriver.Chrome, ChromeOptions),
    "edge": (webdriver.Edge, EdgeOptions),
}


class DriverManager:
    """Factory for cross-browser Selenium drivers, used by the `driver` fixture."""

    @staticmethod
    def get_driver(browser: str, headless: bool) -> webdriver.Remote:
        browser = browser.lower()

        if browser in _CHROMIUM_BROWSERS:
            driver_cls, options_cls = _CHROMIUM_BROWSERS[browser]
            options = options_cls()
            if headless:
                for arg in _CHROMIUM_HEADLESS_ARGS:
                    options.add_argument(arg)
            driver = driver_cls(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser!r}")

        if not headless:
            driver.maximize_window()

        return driver
