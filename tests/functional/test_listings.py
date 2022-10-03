import json

import pytest

from bpify import app
from markets import MARKETS


@pytest.fixture()
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_markets(client):
    """Get available markets"""

    response = client.get("/markets")
    assert response.json == [market.to_dict() for market in MARKETS.get_all()]


def test_post_listing_wrong_currency(client):
    data = {
        "title": "Comfortable Room In Cozy Neighborhood",
        "base_price": 867,
        "currency": "KJY",
        "market": "san-francisco",
        "host_name": "John Smith",
    }
    response = client.post(
        "/listings",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )

    assert response.json == {
        "currency": ["Choose one of the following: ('USD', 'EUR', 'JPY', 'ILS', 'AUD')"]
    }
