from datetime import datetime
from typing import Any, Literal, Optional, Type, TypeVar, Union

from httpx import AsyncClient, Client, Response
from pydantic import BaseModel
from typing_extensions import Unpack

from column.exceptions import ColumnClientException, ColumnErrorResponse
from column.models.account_number import AccountNumber, AccountNumberCreateDict, AccountNumberList
from column.models.bank_account import (
    BankAccount,
    BankAccountCreateDict,
    BankAccountList,
    BankAccountListParams,
    BankAccountSummaryHistory,
    BankAccountUpdateDict,
)
from column.models.business_entity import BusinessEntity, BusinessEntityDict
from column.models.counterparty import (
    Counterparty,
    CounterpartyCreateDict,
    CounterpartyList,
    CounterpartyListParams,
    FinancialInstitution,
    FinancialInstitutionList,
    FinancialInstitutionListParams,
    IBANValidationObject,
)
from column.models.document import DocumentSubmitDict
from column.models.person_entity import PersonEntity, PersonEntityDict
from column.models.transfer import (
    BookTransfer,
    BookTransferList,
    CreateBookTransferBody,
    TransferDetailsDict,
    TransferStatus,
)

from .constants import COLUMN_API_ADDRESS
from .types import ColumnEnv

T = TypeVar("T", bound=BaseModel)


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
        if data["type"] == "BUSINESS":
            return BusinessEntity.model_validate(data)
        if data["type"] == "PERSON":
            return PersonEntity.model_validate(data)
        raise ValueError(f"Unhandled entity type: {data['type']}")

    def get_entity(self, entity_id: str) -> Union[BusinessEntity, PersonEntity]:
        response = self._client.get(f"/entities/{entity_id}")
        return self._get_entity(response)

    async def aget_entity(self, entity_id: str) -> Union[BusinessEntity, PersonEntity]:
        response = await self._async_client.get(f"/entities/{entity_id}")
        return self._get_entity(response)

    def _parse_response(self, response: Response, model: Type[T]) -> T:
        data = self._handle_response(response)
        return model.model_validate(data)

    def create_person(self, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = self._client.post("/entities/person", json=kwargs)
        return self._parse_response(response, PersonEntity)

    async def acreate_person(self, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = await self._async_client.post("/entities/person", json=kwargs)
        return self._parse_response(response, PersonEntity)

    def update_person(self, entity_id: str, **kwargs: Unpack[PersonEntityDict]) -> PersonEntity:
        response = self._client.put(f"/entities/person/{entity_id}", json=kwargs)
        return self._parse_response(response, PersonEntity)

    async def aupdate_person(
        self, entity_id: str, **kwargs: Unpack[PersonEntityDict]
    ) -> PersonEntity:
        response = await self._async_client.put(f"/entities/person/{entity_id}", json=kwargs)
        return self._parse_response(response, PersonEntity)

    def create_business(self, **kwargs: Unpack[BusinessEntityDict]) -> BusinessEntity:
        response = self._client.post("/entities/business", json=kwargs)
        return self._parse_response(response, BusinessEntity)

    async def acreate_business(self, **kwargs: Unpack[BusinessEntityDict]) -> BusinessEntity:
        response = await self._async_client.post("/entities/business", json=kwargs)
        return self._parse_response(response, BusinessEntity)

    def update_business(
        self, entity_id: str, **kwargs: Unpack[BusinessEntityDict]
    ) -> BusinessEntity:
        response = self._client.put(f"/entities/business/{entity_id}", json=kwargs)
        return self._parse_response(response, BusinessEntity)

    async def aupdate_business(
        self, entity_id: str, **kwargs: Unpack[BusinessEntityDict]
    ) -> BusinessEntity:
        response = await self._async_client.put(f"/entities/business/{entity_id}", json=kwargs)
        return self._parse_response(response, BusinessEntity)

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

    def create_bank_account(self, **kwargs: Unpack[BankAccountCreateDict]) -> BankAccount:
        response = self._client.post("/entities/bank-account", json=kwargs)
        return self._parse_response(response, BankAccount)

    async def acreate_bank_account(self, **kwargs: Unpack[BankAccountCreateDict]) -> BankAccount:
        response = await self._async_client.post("/entities/bank-account", json=kwargs)
        return self._parse_response(response, BankAccount)

    def list_bank_accounts(
        self, entity_id: str, **kwargs: Unpack[BankAccountListParams]
    ) -> BankAccountList:
        base_params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        created = kwargs.get("created", None)
        if created:
            for key in ["gt", "lt", "gte", "lte"]:
                if date_value := created.get(key):
                    base_params[f"created.{key}"] = date_value.isoformat()

        response = self._client.get(f"/entities/{entity_id}/bank-accounts", params=base_params)
        return self._parse_response(response, BankAccountList)

    async def alist_bank_accounts(
        self, entity_id: str, **kwargs: Unpack[BankAccountListParams]
    ) -> BankAccountList:
        base_params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        created = kwargs.get("created", None)
        if created:
            for key in ["gt", "lt", "gte", "lte"]:
                if date_value := created.get(key):
                    base_params[f"created.{key}"] = date_value.isoformat()
        response = await self._async_client.get(
            f"/entities/{entity_id}/bank-accounts", params=base_params
        )
        return self._parse_response(response, BankAccountList)

    def get_bank_account(self, bank_account_id: str) -> BankAccount:
        response = self._client.get(f"/entities/bank-account/{bank_account_id}")
        return self._parse_response(response, BankAccount)

    async def aget_bank_account(self, bank_account_id: str) -> BankAccount:
        response = await self._async_client.get(f"/entities/bank-account/{bank_account_id}")
        return self._parse_response(response, BankAccount)

    def update_bank_account(
        self, bank_account_id: str, **kwargs: Unpack[BankAccountUpdateDict]
    ) -> BankAccount:
        response = self._client.put(f"/entities/bank-account/{bank_account_id}", json=kwargs)
        return self._parse_response(response, BankAccount)

    async def aupdate_bank_account(
        self, bank_account_id: str, **kwargs: Unpack[BankAccountUpdateDict]
    ) -> BankAccount:
        response = await self._async_client.put(
            f"/entities/bank-account/{bank_account_id}", json=kwargs
        )
        return self._parse_response(response, BankAccount)

    def delete_bank_account(self, bank_account_id: str) -> None:
        response = self._client.delete(f"/entities/bank-account/{bank_account_id}")
        self._handle_response(response)

    async def adelete_bank_account(self, bank_account_id: str) -> None:
        response = await self._async_client.delete(f"/entities/bank-account/{bank_account_id}")
        self._handle_response(response)

    def get_bank_account_summary_history(self, bank_account_id: str) -> BankAccountSummaryHistory:
        response = self._client.get(f"/entities/bank-account/{bank_account_id}/summary-history")
        return self._parse_response(response, BankAccountSummaryHistory)

    async def aget_bank_account_summary_history(
        self, bank_account_id: str
    ) -> BankAccountSummaryHistory:
        response = await self._async_client.get(
            f"/entities/bank-account/{bank_account_id}/summary-history"
        )
        return self._parse_response(response, BankAccountSummaryHistory)

    def create_account_number(
        self, bank_account_id: str, **kwargs: Unpack[AccountNumberCreateDict]
    ) -> AccountNumber:
        response = self._client.post(
            f"/bank-accounts/{bank_account_id}/account-number", json=kwargs
        )
        return self._parse_response(response, AccountNumber)

    async def acreate_account_number(
        self, bank_account_id: str, **kwargs: Unpack[AccountNumberCreateDict]
    ) -> AccountNumber:
        response = await self._async_client.post(
            f"/bank-accounts/{bank_account_id}/account-number", json=kwargs
        )
        return self._parse_response(response, AccountNumber)

    def list_account_numbers(
        self,
        bank_account_id: str,
        limit: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> AccountNumberList:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if starting_after is not None:
            params["starting_after"] = starting_after
        if ending_before is not None:
            params["ending_before"] = ending_before
        response = self._client.get(
            f"/bank-accounts/{bank_account_id}/account-numbers",
            params=params,
        )
        return self._parse_response(response, AccountNumberList)

    async def alist_account_numbers(
        self,
        bank_account_id: str,
        limit: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> AccountNumberList:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if starting_after is not None:
            params["starting_after"] = starting_after
        if ending_before is not None:
            params["ending_before"] = ending_before
        response = await self._async_client.get(
            f"/bank-accounts/{bank_account_id}/account-numbers",
            params=params,
        )
        return self._parse_response(response, AccountNumberList)

    def get_account_number(self, account_number_id: str) -> AccountNumber:
        response = self._client.get(f"/account-numbers/{account_number_id}")
        return self._parse_response(response, AccountNumber)

    async def aget_account_number(self, account_number_id: str) -> AccountNumber:
        response = await self._async_client.get(f"/account-numbers/{account_number_id}")
        return self._parse_response(response, AccountNumber)

    def get_counterparty(self, counterparty_id: str) -> Counterparty:
        response = self._client.get(f"/counterparties/{counterparty_id}")
        return self._parse_response(response, Counterparty)

    async def aget_counterparty(self, counterparty_id: str) -> Counterparty:
        response = await self._async_client.get(f"/counterparties/{counterparty_id}")
        return self._parse_response(response, Counterparty)

    def list_counterparties(self, **kwargs: Unpack[CounterpartyListParams]) -> CounterpartyList:
        base_params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        created = kwargs.get("created", None)
        if created:
            for key in ["gt", "lt", "gte", "lte"]:
                if date_value := created.get(key):
                    base_params[f"created.{key}"] = date_value.isoformat()
        response = self._client.get("/counterparties", params=base_params)
        return self._parse_response(response, CounterpartyList)

    async def alist_counterparties(
        self, **kwargs: Unpack[CounterpartyListParams]
    ) -> CounterpartyList:
        base_params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        created = kwargs.get("created", None)
        if created:
            for key in ["gt", "lt", "gte", "lte"]:
                if date_value := created.get(key):
                    base_params[f"created.{key}"] = date_value.isoformat()
        response = await self._async_client.get("/counterparties", params=base_params)
        return self._parse_response(response, CounterpartyList)

    def create_counterparty(self, **kwargs: Unpack[CounterpartyCreateDict]) -> Counterparty:
        response = self._client.post("/counterparties", json=kwargs)
        return self._parse_response(response, Counterparty)

    async def acreate_counterparty(self, **kwargs: Unpack[CounterpartyCreateDict]) -> Counterparty:
        response = await self._async_client.post("/counterparties", json=kwargs)
        return self._parse_response(response, Counterparty)

    def delete_counterparty(self, counterparty_id: str) -> None:
        response = self._client.delete(f"/counterparties/{counterparty_id}")
        self._handle_response(response)

    async def adelete_counterparty(self, counterparty_id: str) -> None:
        response = await self._async_client.delete(f"/counterparties/{counterparty_id}")
        self._handle_response(response)

    def get_financial_institution(self, routing_number: str) -> FinancialInstitution:
        response = self._client.get(f"/institutions/{routing_number}")
        return self._parse_response(response, FinancialInstitution)

    async def aget_financial_institution(self, routing_number: str) -> FinancialInstitution:
        response = await self._async_client.get(f"/institutions/{routing_number}")
        return self._parse_response(response, FinancialInstitution)

    def list_financial_institutions(
        self, **kwargs: Unpack[FinancialInstitutionListParams]
    ) -> FinancialInstitutionList:
        params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        response = self._client.get("/institutions", params=params)
        return self._parse_response(response, FinancialInstitutionList)

    async def alist_financial_institutions(
        self, **kwargs: Unpack[FinancialInstitutionListParams]
    ) -> FinancialInstitutionList:
        params = {k: v for k, v in kwargs.items() if isinstance(v, (int, str, bool))}
        response = await self._async_client.get("/institutions", params=params)
        return self._parse_response(response, FinancialInstitutionList)

    def validate_iban(self, iban: str) -> IBANValidationObject:
        response = self._client.get(f"/iban/{iban}")
        return self._parse_response(response, IBANValidationObject)

    async def avalidate_iban(self, iban: str) -> IBANValidationObject:
        response = await self._async_client.get(f"/iban/{iban}")
        return self._parse_response(response, IBANValidationObject)

    def create_book_transfer(
        self,
        amount: int,
        currency_code: str,
        description: Optional[str] = None,
        sender_bank_account_id: Optional[str] = None,
        sender_account_number_id: Optional[str] = None,
        receiver_bank_account_id: Optional[str] = None,
        receiver_account_number_id: Optional[str] = None,
        allow_overdraft: Optional[bool] = None,
        hold: Optional[bool] = None,
        details: Optional[TransferDetailsDict] = None,
    ) -> BookTransfer:
        body = CreateBookTransferBody(
            amount=amount,
            currency_code=currency_code,
            description=description,
            sender_bank_account_id=sender_bank_account_id,
            sender_account_number_id=sender_account_number_id,
            receiver_bank_account_id=receiver_bank_account_id,
            receiver_account_number_id=receiver_account_number_id,
            allow_overdraft=allow_overdraft,
            hold=hold,
            details=details,
        )
        response = self._client.post("/transfers/book", json=body.model_dump(exclude_none=True))
        return self._parse_response(response, BookTransfer)

    async def acreate_book_transfer(
        self,
        amount: int,
        currency_code: str,
        description: Optional[str] = None,
        sender_bank_account_id: Optional[str] = None,
        sender_account_number_id: Optional[str] = None,
        receiver_bank_account_id: Optional[str] = None,
        receiver_account_number_id: Optional[str] = None,
        allow_overdraft: Optional[bool] = None,
        hold: Optional[bool] = None,
        details: Optional[TransferDetailsDict] = None,
    ) -> BookTransfer:
        body = CreateBookTransferBody(
            amount=amount,
            currency_code=currency_code,
            description=description,
            sender_bank_account_id=sender_bank_account_id,
            sender_account_number_id=sender_account_number_id,
            receiver_bank_account_id=receiver_bank_account_id,
            receiver_account_number_id=receiver_account_number_id,
            allow_overdraft=allow_overdraft,
            hold=hold,
            details=details,
        )
        response = await self._async_client.post(
            "/transfers/book", json=body.model_dump(exclude_none=True)
        )
        return self._parse_response(response, BookTransfer)

    def list_book_transfers(
        self,
        limit: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        created_gt: Optional[datetime] = None,
        created_lt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        sender_bank_account_id: Optional[str] = None,
        receiver_bank_account_id: Optional[str] = None,
        status: Optional[TransferStatus] = None,
    ) -> BookTransferList:
        params = {k: v for k, v in locals().items() if v is not None and "created" not in k}
        if created_gt:
            params["created.gt"] = created_gt.isoformat()
        if created_lt:
            params["created.lt"] = created_lt.isoformat()
        if created_gte:
            params["created.gte"] = created_gte.isoformat()
        if created_lte:
            params["created.lte"] = created_lte.isoformat()
        response = self._client.get("/transfers/book", params=params)
        return self._parse_response(response, BookTransferList)

    async def alist_book_transfers(
        self,
        limit: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        created_gt: Optional[datetime] = None,
        created_lt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        sender_bank_account_id: Optional[str] = None,
        receiver_bank_account_id: Optional[str] = None,
        status: Optional[TransferStatus] = None,
    ) -> BookTransferList:
        params = {k: v for k, v in locals().items() if v is not None and "created" not in k}
        if created_gt:
            params["created.gt"] = created_gt.isoformat()
        if created_lt:
            params["created.lt"] = created_lt.isoformat()
        if created_gte:
            params["created.gte"] = created_gte.isoformat()
        if created_lte:
            params["created.lte"] = created_lte.isoformat()
        response = await self._async_client.get("/transfers/book", params=params)
        return self._parse_response(response, BookTransferList)

    def get_book_transfer(self, book_transfer_id: str) -> BookTransfer:
        response = self._client.get(f"/transfers/book/{book_transfer_id}")
        return self._parse_response(response, BookTransfer)

    async def aget_book_transfer(self, book_transfer_id: str) -> BookTransfer:
        response = await self._async_client.get(f"/transfers/book/{book_transfer_id}")
        return self._parse_response(response, BookTransfer)

    def cancel_book_transfer(self, book_transfer_id: str) -> None:
        """Cancel a book transfer hold by its ID. Transfer must be in a HOLD state."""
        response = self._client.post(f"/transfers/book/{book_transfer_id}/cancel")
        self._handle_response(response)

    async def acancel_book_transfer(self, book_transfer_id: str) -> None:
        """Cancel a book transfer hold by its ID. Transfer must be in a HOLD state."""
        response = await self._async_client.post(f"/transfers/book/{book_transfer_id}/cancel")
        self._handle_response(response)

    def clear_book_transfer(self, book_transfer_id: str) -> None:
        """Clear a book transfer hold by its ID. Transfer must be in a HOLD state.
        If the amount is specified, then that amount will be cleared, regardless of the amount of the hold.
        If no amount is specified, then the entire hold will be cleared."""
        response = self._client.post(f"/transfers/book/{book_transfer_id}/clear")
        self._handle_response(response)

    async def aclear_book_transfer(self, book_transfer_id: str) -> None:
        """Clear a book transfer hold by its ID. Transfer must be in a HOLD state.
        If the amount is specified, then that amount will be cleared, regardless of the amount of the hold.
        If no amount is specified, then the entire hold will be cleared."""
        response = await self._async_client.post(f"/transfers/book/{book_transfer_id}/clear")
        self._handle_response(response)


# TODO: Idempotency headers
# TODO: Currency Codes, ISO 4217
