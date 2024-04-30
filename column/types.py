from typing import Literal

ColumnEnv = Literal["live", "test"]
ColumnErrorResponseType = Literal[
    "authentication_error",
    "bank_account_error",
    "dashboard_error",
    "entity_error",
    "limit_error",
    "loan_error",
    "request_validation_error",
    "server_error",
    "transfer_error",
]
