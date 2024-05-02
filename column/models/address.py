from typing import NotRequired, Optional, TypedDict

from pydantic import BaseModel


class Address(BaseModel):
    """
    A model representing an address.

    Attributes:
    - city (str): The city of the address.
    - country_code (str): The country code of the address.
    - postal_code (str): The postal code of the address.
    - state (str | None): The state of the address.
    - line_1 (str): The first line of the address.
    - line_2 (str | None): The second line of the address, if available.
    """

    city: str
    country_code: str
    postal_code: str
    state: Optional[str]  # Optional if country is not US
    line_1: str
    line_2: Optional[str]  # Optional field


class AddressDict(TypedDict):
    """
    A dictionary type representing an address.

    Attributes:
    - city (str): The city of the address.
    - country_code (str): The country code of the address.
    - postal_code (str): The postal code of the address.
    - state (str | None): The state of the address.
    - line_1 (str): The first line of the address.
    - line_2 (str | None): The second line of the address, if available.
    """

    city: str
    country_code: str
    postal_code: NotRequired[str]
    state: NotRequired[str]  # Optional if country is not US
    line_1: str
    line_2: NotRequired[str]  # Optional field
