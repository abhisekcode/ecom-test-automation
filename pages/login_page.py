"""Page object for the SauceDemo login page."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import load_config


class LogInPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> None:
        self.driver.get(load_config()["base_url"])

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def is_logged_in(self) -> bool:
        return "inventory" in self.driver.current_url

    def get_error_message(self) -> str:
        return self.find(self.ERROR_MESSAGE).text
