import os
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Generic, Type, TypeVar
from uuid import UUID

from cloudpathlib import AnyPath
from pydantic import SecretStr
from typing_extensions import Self

from .prodigy_teams_pam_sdk import models as pam_models
from .prodigy_teams_pam_sdk import recipe_client

_KindT = TypeVar("_KindT", bound=str)


@dataclass
class Asset(Generic[_KindT]):
    """Custom type for an asset uploaded to the cluster."""

    id: UUID
    broker_id: UUID
    name: str
    version: str
    kind: ClassVar[str] = ""
    path: str
    meta: Dict[str, Any]

    def load(self, *args: Any, **kwargs: Any) -> AnyPath:
        raise NotImplementedError  # shouldn't happen

    @classmethod
    def create(cls: Type[Self], name: str, path: str, version: str, meta: dict) -> Self:
        cfg = recipe_client.Settings()
        if not cfg.validate():
            raise ValueError("Invalid settings")
        client = recipe_client.get_pam_client(cfg.pam_host, cfg.pam_token)
        broker_id = cfg.broker_id
        if broker_id is None:
            raise ValueError("Cannot create asset: no broker_id specified")
        return cls.create_with_client(
            client, broker_id, name=name, path=path, version=version, meta=meta
        )

    @classmethod
    def create_with_client(
        cls: Type[Self],
        client: recipe_client.Client,
        broker_id: UUID,
        name: str,
        path: str,
        version: str,
        meta: dict,
    ) -> Self:
        response = client.asset.create(
            pam_models.AssetCreating(
                broker_id=broker_id,
                name=name,
                version=version,
                path=path,
                kind=cls.kind,
                meta=meta,
            )
        )
        return cls(
            id=response.id,
            broker_id=response.broker_id,
            name=response.name,
            path=response.path,
            version=response.version,
            meta=response.meta,
        )

    def update(self) -> None:
        cfg = recipe_client.Settings()
        if not cfg.validate():
            raise ValueError("Invalid settings")
        pam_client = recipe_client.get_pam_client(cfg.pam_host, cfg.pam_token)
        return self.update_with_client(pam_client)

    def update_with_client(self, client: recipe_client.Client) -> None:
        _ = client.asset.update(
            pam_models.AssetUpdating(
                id=self.id,
                name=self.name,
                version=self.version,
                path=self.path,
                kind=self.kind,
                meta=self.meta,
            )
        )


@dataclass
class Dataset(Generic[_KindT]):
    """Custom type for a Prodigy dataset on the cluster."""

    id: UUID
    name: str
    broker_id: UUID
    kind: ClassVar[str] = ""

    def load(self, *args: Any, **kwargs: Any) -> AnyPath:
        raise NotImplementedError  # shouldn't happen


@dataclass
class Secret:
    """Custom type for a set of secrets on the cluster."""

    id: UUID
    name: str
    broker_id: UUID
    path: str

    def get(self, name: str) -> SecretStr:
        value = os.getenv(name)
        if value is None:
            raise KeyError(f"No secret value found for key: {name}")
        return SecretStr(value)

    def get_secret_value(self, name: str) -> str:
        val = self.get(name)
        return val.get_secret_value()
