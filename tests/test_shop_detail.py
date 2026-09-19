import pytest
from copy import deepcopy
from pydantic import ValidationError

from models.response import Response


def test_status_code(shop_detail_response):
    assert shop_detail_response.status_code == 200


def test_response_schema(shop_detail_response):
    body = shop_detail_response.json()

    Response.model_validate(body)


def test_shop_name_not_empty(shop_detail_response):
    body = shop_detail_response.json()
    validated = Response.model_validate(body)

    shop_name = validated.data.shopDetailData.shopHeader.shopName

    assert shop_name.strip()


def test_entp_code_not_empty(shop_detail_response):
    body = shop_detail_response.json()
    validated = Response.model_validate(body)

    entp_code = validated.data.shopDetailData.shopHeader.momoAsk.entpCode

    assert entp_code.strip()


def remove_shop_name(body):
    del body["data"]["shopDetailData"]["shopHeader"]["shopName"]


def change_success_type(body):
    body["success"] = "true"


@pytest.mark.parametrize(
    "modify_response",
    [
        remove_shop_name,
        change_success_type,
    ],
)
def test_invalid_response_is_rejected(
    shop_detail_response,
    modify_response,
):
    body = deepcopy(shop_detail_response.json())

    modify_response(body)

    with pytest.raises(ValidationError):
        Response.model_validate(body)