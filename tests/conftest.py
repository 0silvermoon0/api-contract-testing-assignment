import pytest
import requests


API_URL = "https://3pf.momo.com.tw/shop/app/info/detail/query/v1"

HEADERS = {
    "content-type": "application/json",
    "rc": "",
}

PAYLOAD = {
    "host": "momoshop",
    "data": {
        "entpCode": "TP0007070"
    }
}


@pytest.fixture(scope="session")
def shop_detail_response():
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=PAYLOAD,
        timeout=10,
    )

    return response