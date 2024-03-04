from datetime import datetime
from typing import List, Optional, TypedDict

from pydantic import BaseModel


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


class BankAccountCreateDict(TypedDict):
    entity_id: str
    description: Optional[str]
    is_overdraftable: Optional[bool]
    overdraft_reserve_account_id: Optional[str]


class BankAccountUpdateDict(TypedDict):
    description: Optional[str]
    is_overdraftable: Optional[bool]
    overdraft_reserve_account_id: Optional[str]
