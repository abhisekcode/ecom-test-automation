"""UI tests for the SauceDemo login and cart flow."""

import allure
import pytest


@pytest.mark.smoke
@pytest.mark.ui
def test_add_to_cart(login_page, products_page, cart_page, credentials):
    with allure.step("Login with standard user"):
        login_page.open()
        login_page.login(credentials["username"], credentials["password"])

    with allure.step("Add Sauce Labs Bike Light to cart"):
        products_page.add_product_to_cart("Sauce Labs Bike Light")

    with allure.step("Verify cart count"):
        assert products_page.get_cart_count() == 1

    with allure.step("Open cart"):
        products_page.go_to_cart()

    with allure.step("Verify product exists in cart"):
        assert cart_page.is_product_in_cart("Sauce Labs Bike Light")


@pytest.mark.smoke
@pytest.mark.ui
def test_cart_is_empty_before_adding_products(login_page, products_page, credentials):
    with allure.step("Login with standard user"):
        login_page.open()
        login_page.login(credentials["username"], credentials["password"])

    with allure.step("Verify cart starts empty"):
        assert products_page.get_cart_count() == 0


@pytest.mark.ui
@pytest.mark.regression
def test_login_with_invalid_credentials(login_page, credentials):
    with allure.step("Attempt login with a bad password"):
        login_page.open()
        login_page.login(credentials["username"], "wrong_password")

    with allure.step("Verify login is rejected with an error message"):
        assert not login_page.is_logged_in()
        assert "do not match" in login_page.get_error_message().lower()
