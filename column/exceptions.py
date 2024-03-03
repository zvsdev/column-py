from typing import Literal

from httpx import Response
from pydantic import BaseModel

type ColumnErrorResponseType = Literal[
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


class ColumnErrorResponse(BaseModel):
    type: ColumnErrorResponseType
    code: str
    message: str
    documentation_url: str
    details: dict[str, str]


class ColumnClientException(Exception):
    type: ColumnErrorResponseType
    code: str
    documentation_url: str
    detaisl: dict[str, str]
    status_code: int
    url: str

    def __init__(self, response_body: ColumnErrorResponse, response: Response) -> None:
        self.type = response_body.type
        self.code = response_body.code
        self.documentation_url = response_body.documentation_url
        self.details = response_body.details
        self.status_code = response.status_code
        self.url = str(response.url)
        super().__init__(
            f"Error calling {self.url}, {self.type}: {self.code} - {self.details}, Server returned status: {self.status_code}"
        )
