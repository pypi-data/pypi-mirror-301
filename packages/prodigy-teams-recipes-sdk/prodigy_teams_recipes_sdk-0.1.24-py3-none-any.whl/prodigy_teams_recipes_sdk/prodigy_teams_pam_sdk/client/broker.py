from .. import ty
from ..models import (
    BrokerCreating,
    BrokerCredentials,
    BrokerDeleting,
    BrokerDetail,
    BrokerReading,
    BrokerSummary,
    BrokerUpdating,
)
from .base import ModelClient


class Broker(
    ModelClient[
        BrokerCreating,
        BrokerReading,
        BrokerUpdating,
        BrokerDeleting,
        BrokerSummary,
        BrokerDetail,
    ]
):
    Creating = BrokerCreating
    Reading = BrokerReading
    Updating = BrokerUpdating
    Deleting = BrokerDeleting
    Summary = BrokerSummary
    Detail = BrokerDetail

    class Token(ty.BaseModel):
        token: str

    def create(
        self, data: ty.Optional[BrokerCreating] = None, **kwargs: ty.Any
    ) -> BrokerDetail:
        data = data if data else BrokerCreating(**kwargs)
        res = self.request(
            "POST",
            endpoint="create",
            data=data,
            return_model=BrokerDetail,
        )
        assert isinstance(res, BrokerDetail)
        return res

    async def create_async(
        self, data: ty.Optional[BrokerCreating] = None, **kwargs: ty.Any
    ) -> BrokerDetail:
        data = data if data else BrokerCreating(**kwargs)
        res = await self.request_async(
            "POST",
            endpoint="create",
            data=data,
            return_model=BrokerDetail,
        )
        assert isinstance(res, BrokerDetail)
        return res

    def credentials(self, broker_id: ty.UUID) -> BrokerCredentials:
        res = self.request(
            "GET",
            endpoint=f"{broker_id}/credentials",
            return_model=BrokerCredentials,
        )
        assert isinstance(res, BrokerCredentials)
        return res

    def download_gcloud_files(self) -> ty.IO:
        res = self.request("GET", endpoint="files/gcloud", stream=True)
        return ty.cast(ty.IO, res)
