from datetime import datetime
from typing import List, TypedDict

from pydantic import BaseModel


class AccountNumber(BaseModel):
    id: str
    bank_account_id: str
    bic: str  # swift code for this bank account for international wire payments
    created_at: datetime
    description: str
    routing_number: str


class AccountNumberCreateDict(TypedDict):
    description: str


class AccountNumberList(BaseModel):
    has_more: bool
    account_numbers: List[AccountNumber]
