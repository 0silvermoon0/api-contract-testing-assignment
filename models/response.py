from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)


class MomoAsk(ContractModel):
    entpCode: str = Field(min_length=1)

    deliveryType: Optional[str] = None
    allowReply: Optional[bool] = None


class ShopHeader(ContractModel):
    shopName: str = Field(min_length=1)

    shopIcon: Optional[str] = None
    shopFitRate: Optional[str] = None
    commentCount: Optional[str] = None
    followCount: Optional[str] = None
    isFollow: Optional[bool] = None
    backgroundURL: Optional[str] = None
    crossBorderShop: Optional[str] = None

    momoAsk: MomoAsk


class ReturnInfo(ContractModel):
    paragraphType: Optional[str] = None
    title: Optional[str] = None
    content: Optional[list[str]] = None


class DefectiveRateInfo(ContractModel):
    defectiveRate: Optional[str] = None
    hidden: Optional[bool] = None


class ShopInfo(ContractModel):
    askResponseRate: Optional[str] = None
    shopIntro: Optional[str] = None
    stockCount: Optional[str] = None
    shopCreateDate: Optional[str] = None
    companyName: Optional[str] = None
    taxId: Optional[str] = None
    shopURL: Optional[str] = None
    displayShopURL: Optional[str] = None

    returnInfo: Optional[list[ReturnInfo]] = None

    hasComments: Optional[bool] = None
    defectiveRateInfo: Optional[DefectiveRateInfo] = None


class ShopDetailData(ContractModel):
    shopHeader: Optional[ShopHeader] = None

    shopInfo: Optional[ShopInfo] = None


class Data(ContractModel):
    shopDetailData: Optional[ShopDetailData] = None


class Response(ContractModel):
    success: bool
    resultCode: str = Field(min_length=1)
    resultMessage: str = Field(min_length=1)

    resultException: str

    timestamp: Optional[str] = None
    trackingNo: Optional[str] = None

    data: Optional[Data] = None

    ConsumerExecuteTime: Optional[str] = None
    inQueueWaitTime: Optional[str] = None
    finishDateTime: Optional[str] = None

    @model_validator(mode="after")
    def validate_success_response(self):

        if not self.success:
            return self

        if self.data is None:
            raise ValueError(
                "data must exist when success is true"
            )

        if self.data.shopDetailData is None:
            raise ValueError(
                "data.shopDetailData must exist when success is true"
            )

        if self.data.shopDetailData.shopHeader is None:
            raise ValueError(
                "data.shopDetailData.shopHeader "
                "must exist when success is true"
            )

        return self