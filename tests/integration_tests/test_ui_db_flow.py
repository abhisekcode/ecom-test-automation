"""UI -> external API -> SQLite integration checks for the cart flow."""

import json

import pytest
import requests

from data.product_mapping import UI_TO_API_MAP
from utils.db_utils import clear_cart, get_products, insert_product
from utils.paths import PROJECT_ROOT

API_PRODUCTS_URL = "https://dummyjson.com/products"

with open(PROJECT_ROOT / "data" / "test_data.json") as f:
    PRODUCT_NAMES = json.load(f)["products"]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.db
@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_ui_db_integration(login_page, products_page, cart_page, credentials, product_name):
    clear_cart()

    # Step 1: UI actions
    login_page.open()
    login_page.login(credentials["username"], credentials["password"])
    products_page.add_product_to_cart(product_name)
    assert products_page.get_cart_count() == 1
    products_page.go_to_cart()

    # Step 2: UI validation
    assert cart_page.is_product_in_cart(product_name)

    # Step 3: cross-check against the external products API
    api_product = UI_TO_API_MAP[product_name]
    response = requests.get(API_PRODUCTS_URL, timeout=5)
    api_titles = [p["title"] for p in response.json()["products"]]
    assert api_product in api_titles

    # Step 4: persist + verify in SQLite
    insert_product(product_name)
    assert product_name in get_products()


@pytest.mark.db
@pytest.mark.regression
def test_clear_cart_removes_all_products():
    clear_cart()
    insert_product("Sauce Labs Backpack")
    insert_product("Sauce Labs Bike Light")
    assert len(get_products()) == 2

    clear_cart()

    assert get_products() == []
