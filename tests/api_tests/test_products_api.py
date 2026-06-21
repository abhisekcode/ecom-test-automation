"""API tests against the public dummyjson.com products endpoint."""

import pytest
import requests

BASE_URL = "https://dummyjson.com/products"


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_get_products():
    try:
        response = requests.get(BASE_URL, timeout=5)
    except requests.exceptions.RequestException:
        pytest.skip("API not reachable")

    assert response.status_code == 200

    data = response.json()
    assert "products" in data
    assert len(data["products"]) > 0
    assert "title" in data["products"][0]


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_get_single_product_not_found():
    try:
        response = requests.get(f"{BASE_URL}/99999999", timeout=5)
    except requests.exceptions.RequestException:
        pytest.skip("API not reachable")

    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
