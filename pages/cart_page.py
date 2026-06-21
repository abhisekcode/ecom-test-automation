"""Page object for the SauceDemo cart page."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def get_cart_items(self) -> list[str]:
        return [item.text.strip() for item in self.find_all(self.ITEM_NAMES)]

    def is_product_in_cart(self, product_name: str) -> bool:
        items = self.get_cart_items()
        self.logger.info(f"Cart products: {items}")
        return product_name in items
