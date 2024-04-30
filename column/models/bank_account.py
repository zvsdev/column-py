from datetime import date, datetime
from typing import List, Literal, Optional, TypedDict

from pydantic import BaseModel
from typing_extensions import NotRequired

BankAccountType = Literal["CHECKING", "OVERDRAFT_RESERVE", "PROGRAM_RESERVE"]


class Balances(BaseModel):
    """Represents the various balance amounts for a bank account."""

    available_amount: int  # Amount available to spend
    holding_amount: int  # Balance in HOLD state
    locked_amount: int  # Locked balance, applicable for root accounts
    pending_amount: int  # Total amount in pending state


class BankAccount(BaseModel):
    """
    Represents a bank account, including balances, identifiers, and account-specific details.
    """

    balances: Balances
    bic: str  # Swift BIC code for international wire payments
    created_at: datetime  # Timestamp of account creation
    currency_code: str  # Currency of the balances (e.g., USD)
    default_account_number: str  # Default account number
    default_account_number_id: str  # Default account number ID
    description: str  # Name for the bank account
    id: str  # Unique ID for the account
    is_overdraftable: bool  # Indicates if account supports overdraft
    overdraft_reserve_account_id: Optional[str]  # Linked overdraft reserve account ID
    owners: List[str]  # List of entity_id's tied to this bank account
    routing_number: str  # 9-digit ABA routing number
    type: str  # Bank account type (e.g., CHECKING, OVERDRAFT_RESERVE, PROGRAM_RESERVE)


class BankAccountList(BaseModel):
    has_more: bool
    bank_accounts: List[BankAccount]


class CreatedParams(TypedDict):
    gt: NotRequired[datetime]
    lt: NotRequired[datetime]
    gte: NotRequired[datetime]
    lte: NotRequired[datetime]


class BankAccountListParams(TypedDict):
    entity_id: NotRequired[str]
    is_overdraftable: NotRequired[bool]
    type: NotRequired[BankAccountType]
    overdraft_reserve_account_id: NotRequired[str]
    limit: NotRequired[int]
    starting_after: NotRequired[str]
    ending_before: NotRequired[str]
    created: NotRequired[CreatedParams]


class BankAccountCreateDict(TypedDict):
    """
    A dictionary type representing the creation of a bank account.

    Attributes:
    - entity_id (str): The entity ID associated with the bank account.
    - description (Optional[str]): The description of the bank account.
    - is_overdraftable (Optional[bool]): Whether the account supports overdraft.
    - overdraft_reserve_account_id (Optional[str]): The ID of the linked overdraft reserve account.
    - display_name (Optional[str]): The display name of the bank account.
    """

    entity_id: str  # Entity ID associated with the bank account
    description: Optional[str]  # Description of the bank account
    is_overdraftable: Optional[bool]  # Whether the account supports overdraft
    overdraft_reserve_account_id: Optional[str]  # ID of the linked overdraft reserve account
    display_name: Optional[str]  # Display name for the bank account


class BankAccountUpdateDict(TypedDict):
    """
    A dictionary type representing the update of a bank account.

    Attributes:
    - description (Optional[str]): The description of the bank account.
    - is_overdraftable (Optional[bool]): Whether the account supports overdraft.
    - overdraft_reserve_account_id (Optional[str]): The ID of the linked overdraft reserve account.
    - display_name (Optional[str]): The display name of the bank account.
    """

    description: Optional[str]  # Description of the bank account
    is_overdraftable: Optional[bool]  # Whether the account supports overdraft
    overdraft_reserve_account_id: Optional[str]  # ID of the linked overdraft reserve account
    display_name: Optional[str]  # Display name for the bank account


class BankAccountSummary(BaseModel):
    """
    A model representing a summary of a bank account.

    Attributes:
    - available_balance_credit (str): Total credit amount in cents applied to available_balance, Zero or positive.
    - available_balance_debit (str): Total debit amount in cents applied to available_balance. Zero or negative.
    - available_balance_close (str): Close available_balance in cents at the end of effective_on in time_zone.
    - currency (str): Currency code of the balances.
    - effective_on (date): Date of the balances.
    - holding_balance_credit (str): Total credit amount in cents applied to holding_balance. Zero or positive.
    - holding_balance_debit (str): Total debit amount in cents applied to holding_balance. Zero or negative.
    - holding_balance_close (str): Close holding_balance in cents at the end of effective_on in time_zone.
    - locked_balance_credit (str): Total credit amount in cents applied to locked_balance. Zero or positive.
    - locked_balance_debit (str): Total debit amount in cents applied to locked_balance. Zero or negative.
    - locked_balance_close (str): Close locked_balance in cents at the end of effective_on in time_zone.
    - pending_balance_credit (str): Total credit amount in cents applied to pending_balance. Zero or positive.
    - pending_balance_debit (str): Total debit amount in cents applied to pending_balance. Zero or negative.
    - pending_balance_close (str): Close pending_balance in cents at the end of effective_on in time_zone.
    - time_zone (str): Time zone of effective_on to decide day boundaries. You can set your platform reporting time zone in Platform Settings on Dashboard.
    - transaction_count (int): Total number of transactions on the day of effective_on.
    """

    available_balance_credit: (
        str  # Total credit amount in cents applied to available_balance, Zero or positive
    )
    available_balance_debit: (
        str  # Total debit amount in cents applied to available_balance. Zero or negative
    )
    available_balance_close: (
        str  # Close available_balance in cents at the end of effective_on in time_zone.
    )
    currency: str  # Currency code of the balances
    effective_on: date  # Date of the balances
    holding_balance_credit: (
        str  # Total credit amount in cents applied to holding_balance. Zero or positive.
    )
    holding_balance_debit: (
        str  # Total debit amount in cents applied to holding_balance. Zero or negative.
    )
    holding_balance_close: (
        str  # Close holding_balance in cents at the end of effective_on in time_zone.
    )
    locked_balance_credit: (
        str  # Total credit amount in cents applied to locked_balance. Zero or positive.
    )
    locked_balance_debit: (
        str  # Total debit amount in cents applied to locked_balance. Zero or negative.
    )
    locked_balance_close: (
        str  # Close locked_balance in cents at the end of effective_on in time_zone.
    )
    pending_balance_credit: (
        str  # Total credit amount in cents applied to pending_balance. Zero or positive.
    )
    pending_balance_debit: (
        str  # Total debit amount in cents applied to pending_balance. Zero or negative.
    )
    pending_balance_close: (
        str  # Close pending_balance in cents at the end of effective_on in time_zone.
    )
    time_zone: str  # Time zone of effective_on to decide day boundaries. You can set your platform reporting time zone in Platform Settings on Dashboard.
    transaction_count: int  # Total number of transactions on the day of effective_on.


class BankAccountSummaryHistory(BaseModel):
    """
    A model representing a history of bank account summaries.
    """

    id: str  # Unique ID for the account
    history: List[BankAccountSummary]  # List of bank account summaries


class Money(BaseModel):
    cents: int
    currency_code: str


class OverdraftAlert(BaseModel):
    available_balance: Money
    bank_account_id: str
    overdraft_amount: Money
    reserve_account_id: str
    transfer_id: str
