from datetime import datetime
from typing import List, Literal, NotRequired, Optional, TypedDict

from pydantic import BaseModel

from column.models.address import Address, AddressDict

# Transfer

# Transfers are powerful in that they can be used to both ledger events on an account, as well as move and receive money.
# ACH Transfer

# An ACH transfer is created when you initiate or receive an ACH transaction. Column relies on the Federal Reserve's FedACH system and we plan to enable support for TCH's ACH and RTP system in the future. ACH transfers do not settle immediately like wires, but are faster than you might think. We support incoming ACH transfers as well as outgoing ACH credit (push) and debit (pull) transfers. Learn more in the ACH section.
# Domestic Wire Transfer

# A wire transfer is created when you send or receive a wire transaction. Outgoing wire transfers occur in real-time and are sent through the Federal Reserve over their FedWire system. Learn more about wires in the wire section.
# International Wire Transfer

# A Swift transfer is created when you send or receive an international wire transaction. Learn more about international wires in the international wires section.
# Check Transfer

# A check transfer is created when you issue or deposit a check through Column. Column conducts postive pay validation and thus requires you provide a payee name when issuing a check transfer. Learn more about check transfers in the checks section.
# Book Transfers (single platform)

# Book transfers give you speed and cost efficiency. They are a ledger event that immediately moves funds between two accounts on your platform and can be sent 24/7.
# Common examples:

#     Payments between users: You can transfer funds between two of your users with immediate settlement.
#     Account transfers: You can transfer funds between two accounts owned by the same entity. This could serve to pay off a loan, transfer money between different checking accounts, etc.
#     Transfers to a settlement account: If Column is your debit card BIN sponsor, you can use a book transfer to ledger and transfer money from a user's account to your network settlement account instantly upon authorization.

# Sample Book Transfer object
# {
#   "allow_overdraft": false,
#   "amount": 50000,
#   "created_at": "2022-03-02T22:44:35Z",
#   "currency_code": "USD",
#   "description": "For documents",
#   "id": "book_25qiZnUKr2AP8Rb5Vs3PGzpcttC",
#   "idempotency_key": "",
#   "receiver_account_number_id": "acno_25FyF49P2SE4PJJOmfx6kYCzkeI",
#   "receiver_bank_account_id": "bacc_25FyEyuKX3KlRAciUs3BzXag1RI",
#   "sender_account_number_id": "acno_25nVQkqfCU6Okpn66QWi1xX9riD",
#   "sender_bank_account_id": "bacc_25nVQr05nZybpyEzw8j0wV6VRUh",
#   "status": "COMPLETED",
#   "updated_at": "2022-03-02T22:44:35Z"
# }

TransferStatus = Literal["REJECTED", "COMPLETED", "HOLD", "CANCELED"]


class TransferDetailsDict(TypedDict):
    """Represents the details of a transfer object, which captures the current state of a single transfer initiated in Column.
    This object encapsulates the instantaneous movement of funds between two bank accounts under your platform, available 24/7.
    """

    sender_name: NotRequired[str]
    merchant_name: NotRequired[str]
    merchant_category_code: NotRequired[str]
    authorization_method: NotRequired[str]
    website: NotRequired[str]
    internal_transfer_type: NotRequired[str]
    statement_description: NotRequired[str]
    address: AddressDict


class TransferDetails(BaseModel):
    sender_name: Optional[str]
    merchant_name: Optional[str]
    merchant_category_code: Optional[str]
    authorization_method: Optional[str]
    website: Optional[str]
    internal_transfer_type: Optional[str]
    statement_description: Optional[str]
    address: Address


class BookTransfer(BaseModel):
    """Represents a Book Transfer object, which captures the current state of a single book transfer initiated in Column.
    This object encapsulates the instantaneous movement of funds between two bank accounts under your platform, available 24/7.

    Attributes:
    allow_overdraft (bool): Indicates whether the transfer allows overdraft.
    amount (int): The amount of the transfer in cents.
    created_at (datetime): The timestamp when the transfer was created.
    currency_code (str): The currency code of the transfer (e.g., USD).
    description (str): A description of the transfer.
    id (str): A unique identifier for the transfer.
    idempotency_key (str): A unique identifier for the transfer, used for idempotent requests.
    receiver_account_number_id (str): The ID of the receiving account number.
    receiver_bank_account_id (str): The ID of the receiving bank account.
    sender_account_number_id (str): The ID of the sending account number.
    sender_bank_account_id (str): The ID of the sending bank account.
    status (str): The status of the transfer (e.g., COMPLETED).
    updated_at (datetime): The timestamp when the transfer was last updated."""

    allow_overdraft: bool
    amount: int
    created_at: datetime
    currency_code: str
    description: str
    id: str
    idempotency_key: str
    receiver_account_number_id: str
    receiver_bank_account_id: str
    sender_account_number_id: str
    sender_bank_account_id: str
    status: TransferStatus
    updated_at: datetime
    details: TransferDetails


class BookTransferList(BaseModel):
    """Represents a list of book transfers, which captures the current state of a list of book transfers initiated in Column.
    This object encapsulates the instantaneous movement of funds between two bank accounts under your platform, available 24/7.
    """

    data: List[BookTransfer]
    has_more: bool


class CreateBookTransferBody(BaseModel):
    """Represents a request to create a book transfer."""

    amount: int
    currency_code: str
    description: Optional[str] = None
    sender_bank_account_id: Optional[str] = None
    sender_account_number_id: Optional[str] = None
    receiver_bank_account_id: Optional[str] = None
    receiver_account_number_id: Optional[str] = None
    allow_overdraft: Optional[bool] = None
    hold: Optional[bool] = None
    details: Optional[TransferDetailsDict] = None
