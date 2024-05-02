from datetime import datetime
from typing import List, Literal, NotRequired, TypedDict

from models.address import Address, AddressDict
from pydantic import BaseModel

from column.models.common import CreatedParams


class Wire(BaseModel):
    """
    A model representing wire information.

    Attributes:
    - beneficiary_address (Address): The address of the beneficiary.
    - beneficiary_email (str): The email of the beneficiary.
    - beneficiary_legal_id (str): The legal ID of the beneficiary.
    - beneficiary_name (str): The name of the beneficiary.
    - beneficiary_phone (str): The phone number of the beneficiary.
    - beneficiary_type (str): The type of the beneficiary.
    - local_account_number (str): The local account number.
    - local_bank_code (str): The local bank code.
    """

    beneficiary_address: Address
    beneficiary_email: str
    beneficiary_legal_id: str
    beneficiary_name: str
    beneficiary_phone: str
    beneficiary_type: str
    local_account_number: str
    local_bank_code: str


class Counterparty(BaseModel):
    """
    A model representing a counterparty.

    Attributes:
    - account_number (str): The account number of the counterparty.
    - account_type (str): The type of account of the counterparty.
    - address (Address): The address of the counterparty.
    - created_at (datetime): The timestamp when the counterparty was created.
    - description (str): A brief description of the counterparty.
    - email (str): The email address of the counterparty.
    - id (str): The unique identifier of the counterparty.
    - is_column_account (bool): Whether the counterparty is a Column account.
    - legal_id (str): The legal identifier of the counterparty.
    - legal_type (str): The legal type of the counterparty.
    - local_account_number (str): The local account number of the counterparty.
    - local_bank_code (str): The local bank code of the counterparty.
    - local_bank_country_code (str): The local bank country code of the counterparty.
    - local_bank_name (str): The local bank name of the counterparty.
    - name (str): The name of the counterparty.
    - phone (str): The phone number of the counterparty.
    - routing_number (str): The routing number of the counterparty.
    - routing_number_type (str): The type of routing number of the counterparty.
    - updated_at (datetime): The timestamp when the counterparty was last updated.
    - wire (Wire): The wire information of the counterparty.
    - wire_drawdown_allowed (bool): Whether wire drawdown is allowed for the counterparty.
    """

    account_number: str
    account_type: str
    address: Address
    created_at: datetime
    description: str
    email: str
    id: str
    is_column_account: bool
    legal_id: str
    legal_type: str
    local_account_number: str
    local_bank_code: str
    local_bank_country_code: str
    local_bank_name: str
    name: str
    phone: str
    routing_number: str
    routing_number_type: str
    updated_at: datetime
    wire: Wire
    wire_drawdown_allowed: bool


class CounterpartyList(BaseModel):
    """
    A model representing a list of counterparties.

    Attributes:
    - counterparties (List[Counterparty]): A list of counterparties.
    """

    counterparties: List[Counterparty]
    has_more: bool


class CounterpartyListParams(TypedDict):
    """
    A model representing the parameters for listing counterparties.
    """

    limit: NotRequired[int]
    starting_after: NotRequired[str]
    starting_before: NotRequired[str]
    account_number: NotRequired[str]
    routing_number: NotRequired[str]
    created: NotRequired[CreatedParams]


class CounterpartyCreateDict(TypedDict):
    """
    A model representing the parameters for creating a counterparty.
    """

    routing_number: str
    routing_number_type: NotRequired[Literal["bic", "aba"]]
    account_number: str
    account_type: NotRequired[Literal["checking", "savings"]]
    description: NotRequired[str]
    wire_drawdown_allowed: NotRequired[bool]
    name: NotRequired[str]
    address: NotRequired[AddressDict]
    phone: NotRequired[str]
    email: NotRequired[str]
    legal_id: NotRequired[str]
    legal_type: NotRequired[Literal["business", "non_profit", "individual", "sole_proprietor"]]
    local_bank_code: NotRequired[str]
    local_account_number: NotRequired[str]


# Example Financial Institution
# {
#   "ach_eligible": true,
#   "city": "TAMPA",
#   "country_code": "US",
#   "created_at": "2021-10-13T16:39:55Z",
#   "full_name": "JPMORGAN CHASE BANK, NA",
#   "phone_number": "8134323700",
#   "routing_number": "322271627",
#   "routing_number_type": "aba",
#   "short_name": "WASH MUT BANK",
#   "state": "FL",
#   "street_address": "10430 HIGHLAND MANOR DRIVE",
#   "updated_at": "2021-10-28T13:00:35Z",
#   "wire_eligible": true,
#   "wire_settlement_only": false,
#   "zip_code": "33610"
# }


class FinancialInstitution(BaseModel):
    """
    A model representing a financial institution.
    """

    ach_eligible: bool
    city: str
    country_code: str
    created_at: str
    full_name: str
    phone_number: str
    routing_number: str
    routing_number_type: Literal["aba", "bic"]
    short_name: str
    state: str
    street_address: str
    updated_at: str
    wire_eligible: bool
    wire_settlement_only: bool
    zip_code: str


class FinancialInstitutionList(BaseModel):
    """
    A model representing a list of financial institutions.
    """

    financial_institutions: List[FinancialInstitution]
    has_more: bool


class FinancialInstitutionListParams(TypedDict):
    """
    A model representing the parameters for listing financial institutions.
    """

    limit: NotRequired[int]
    starting_after: NotRequired[str]
    starting_before: NotRequired[str]
    country_code: NotRequired[str]
    name: NotRequired[str]
    routing_number_type: NotRequired[str]


class IBANValidationObject(BaseModel):
    """
    A model representing the response from the IBAN validation API.
    """

    account_number: str
    bank_id: str
    bic: str
    branch_id: str
    check_digits: str
    country_code: str
    iban: str
    institution_name: str
    national_id: str
