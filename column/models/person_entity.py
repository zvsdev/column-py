from typing import Optional, TypedDict

from pydantic import BaseModel

from .address import Address, AddressDict
from .document import Document


class Passport(BaseModel):
    country_code: str
    number: str


class PassportDict(TypedDict):
    """
    A dictionary type representing partial information about a passport.

    Attributes:
    - country_code (str): The country code of the passport.
    - number (str): The passport number.
    """

    country_code: str
    number: str


class PersonDetails(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    ssn: str
    date_of_birth: str
    email: str
    passport: Passport
    address: Address


class PersonEntity(BaseModel):
    id: str
    is_root: bool
    documents: list[Document]
    person_details: PersonDetails
    verification_status: str
    verification_tags: str
    review_reasons: list[str]


class PersonEntityDict(TypedDict):
    """
    A dictionary type representing partial information about a person.

    Attributes:
    - first_name (str): The first name of the person.
    - last_name (str): The last name of the person.
    - middle_name (str | None): The middle name of the person, if available.
    - ssn (str | None): The Social Security Number of the person. Required unless a passport is provided.
    - passport (Passport | None): Passport information of the person. Required unless an SSN is provided.
    - date_of_birth (str): The date of birth of the person in a string format.
    - email (str | None): The email address of the person, if available.
    - address (Address): The address information of the person.
    """

    first_name: str
    last_name: str
    middle_name: Optional[str]  # Optional
    ssn: str | None  # Required unless passport is provided
    passport: Optional[PassportDict]  # Required unless SSN is provided
    date_of_birth: str
    email: Optional[str]  # Optional
    address: AddressDict
