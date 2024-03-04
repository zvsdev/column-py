from typing import Any, Literal, Union

from httpx import AsyncClient, Client, Response
from typing_extensions import Unpack

from column.exceptions import ColumnClientException, ColumnErrorResponse
from column.models.business_entity import BusinessEntity, BusinessEntityDict
from column.models.document import DocumentSubmitDict
from column.models.person_entity import PersonEntity, PersonEntityDict

from .constants import COLUMN_API_ADDRESS
from .types import ColumnEnv


class ColumnClient:
    _api_key: str
    _env: ColumnEnv
    _client: Client
    _async_client: AsyncClient

    def __init__(self, api_key: str) -> None:
        self._env = self._parse_env(api_key)
        self._api_key = api_key
        self._client = Client(base_url=COLUMN_API_ADDRESS, auth=("", api_key))
        self._async_client = AsyncClient(base_url=COLUMN_API_ADDRESS, auth=("", api_key))

    @staticmethod
    def _parse_env(api_key: str) -> Literal["live", "test"]:
        if api_key.startswith("test_"):
            return "test"
        if api_key.startswith("live_"):
            return "live"
        # TODO: assert length of key?
        raise ValueError("Invalid API key")

    @staticmethod
    def _handle_response(response: Response) -> dict[str, Any]:
        data = response.json()
        if response.status_code == 200:
            return data
        if response.status_code in (400, 401, 403, 404, 429) or response.status_code >= 500:
            error_body = ColumnErrorResponse.model_validate(data)
            raise ColumnClientException(error_body, response)
        raise ValueError(f"Unhandled status code: {response.status_code}")

    def _get_entity(self, response: Response) -> Union[BusinessEntity, PersonEntity]:
        data = self._handle_response(response)
        if data["type"] == "PERSON":
            return BusinessEntity.model_validate(data)
        if data["type"] == "BUSINESS":
            return PersonEntity.model_validate(data)
        raise ValueError(f"Unhandled entity type: {data['type']}")

    def get_entity(self, entity_id: str) -> Union[BusinessEntity, PersonEntity]:
        response = self._client.get(f"/entities/{entity_id}")
        return self._get_entity(response)

    async def aget_entity(self, entity_id: str) -> Union[BusinessEntity, PersonEntity]:
        response = await self._async_client.get(f"/entities/{entity_id}")
        return self._get_entity(response)

    def _mutate_person(self, response: Response) -> PersonEntity:
        data = self._handle_response(response)
        return PersonEntity.model_validate(data)

    def create_person(self, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = self._client.post("/entities/person", json=kwargs)
        return self._mutate_person(response)

    async def acreate_person(self, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = await self._async_client.post("/entities/person", json=kwargs)
        return self._mutate_person(response)

    def update_person(self, entity_id: str, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = self._client.put(f"/entities/person/{entity_id}", json=kwargs)
        return self._mutate_person(response)

    async def aupdate_person(
        self, entity_id: str, **kwargs: Unpack[PersonEntityDict]
    ) -> PersonEntity:
        response = await self._async_client.put(f"/entities/person/{entity_id}", json=kwargs)
        return self._mutate_person(response)

    def _mutate_business(self, response: Response) -> BusinessEntity:
        data = self._handle_response(response)
        return BusinessEntity.model_validate(data)

    def create_business(self, **kwargs: Unpack[BusinessEntityDict]) -> BusinessEntity:
        response = self._client.post("/entities/business", json=kwargs)
        return self._mutate_business(response)

    async def acreate_business(self, **kwargs: Unpack[BusinessEntityDict]) -> BusinessEntity:
        response = await self._async_client.post("/entities/business", json=kwargs)
        return self._mutate_business(response)

    def update_business(
        self, entity_id: str, **kwargs: Unpack[BusinessEntityDict]
    ) -> BusinessEntity:
        response = self._client.put(f"/entities/business/{entity_id}", json=kwargs)
        return self._mutate_business(response)

    async def aupdate_business(
        self, entity_id: str, **kwargs: Unpack[BusinessEntityDict]
    ) -> BusinessEntity:
        response = await self._async_client.put(f"/entities/business/{entity_id}", json=kwargs)
        return self._mutate_business(response)

    def delete_entity(self, entity_id: str) -> None:
        response = self._client.delete(f"/entities/{entity_id}")
        self._handle_response(response)

    async def adelete_entity(self, entity_id: str) -> None:
        response = await self._async_client.delete(f"/entities/{entity_id}")
        self._handle_response(response)

    def submit_document(
        self, entity_id: str, **kwargs: Unpack[DocumentSubmitDict]
    ) -> Union[PersonEntity, BusinessEntity]:
        response = self._client.post(f"/entities/{entity_id}/documents", json=kwargs)
        return self._get_entity(response)

    async def asubmit_document(
        self, entity_id: str, **kwargs: Unpack[DocumentSubmitDict]
    ) -> Union[PersonEntity, BusinessEntity]:
        response = await self._async_client.post(f"/entities/{entity_id}/documents", json=kwargs)
        return self._get_entity(response)
