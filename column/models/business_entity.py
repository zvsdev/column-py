from typing import TypedDict

from pydantic import BaseModel

from .address import Address, AddressDict
from .document import Document


class Identification(BaseModel):
    number: str
    country_code: str


class IdentificationDict(TypedDict):
    """
    A dictionary type representing partial information about an identification.

    Attributes:
    - number (str): The identification number.
    - country_code (str): The country code of the identification.
    """

    number: str
    country_code: str


class BeneficialOwner(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None  # Optional field
    ssn: str | None  # Optional field
    passport: Identification | None  # Optional field
    drivers_license: Identification | None  # Optional field
    national_id: Identification | None  # Optional field
    date_of_birth: str
    email: str | None  # Optional field
    is_control_person: bool
    is_beneficial_owner: bool
    ownership_percentage: int | None  # Optional field
    job_title: str | None  # Optional field
    address: Address


class BeneficialOwnerDict(TypedDict):
    """
    A dictionary type representing partial information about a beneficial owner.

    Attributes:
    - first_name (str): The first name of the beneficial owner.
    - last_name (str): The last name of the beneficial owner.
    - middle_name (str | None): The middle name of the beneficial owner, if available.
    - ssn (str | None): The SSN of the beneficial owner, if available.
    - passport (Identification | None): The passport of the beneficial owner, if available.
    - drivers_license (Identification | None): The driver's license of the beneficial owner, if available.
    - national_id (Identification | None): The national ID of the beneficial owner, if available.
    - date_of_birth (str): The date of birth of the beneficial owner.
    - email (str | None): The email of the beneficial owner, if available.
    - is_control_person (bool): Whether the beneficial owner is a control person.
    - is_beneficial_owner (bool): Whether the beneficial owner is a beneficial owner.
    - ownership_percentage (int | None): The ownership percentage of the beneficial owner, if available.
    - job_title (str | None): The job title of the beneficial owner, if available.
    - address (AddressDict): The address of the beneficial owner.
    """

    first_name: str
    last_name: str
    middle_name: str | None  # Optional
    ssn: str | None  # Optional
    passport: IdentificationDict | None  # Optional
    drivers_license: IdentificationDict | None  # Optional
    national_id: IdentificationDict | None  # Optional
    date_of_birth: str
    email: str | None  # Optional
    is_control_person: bool
    is_beneficial_owner: bool
    ownership_percentage: int | None  # Optional
    job_title: str | None  # Optional
    address: AddressDict


class RegistrationID(BaseModel):
    number: str
    country_code: str


class BusinessDetails(BaseModel):
    address: Address
    beneficial_owners: list[BeneficialOwner]
    business_name: str
    ein: str | None  # Optional field
    registration_id: RegistrationID | None  # Optional field
    industry: str
    website: str | None  # Optional field
    legal_type: str
    state_of_incorporation: str | None  # Optional field
    date_of_incorporation: str | None  # Optional field
    account_usage: list[str] | None  # Optional field
    description: str | None  # Optional field
    payment_volumes: str | None  # Optional field
    countries_of_operation: list[str] | None  # Optional field


class BusinessEntity(BaseModel):
    id: str
    is_root: bool
    documents: list[Document]
    business_details: BusinessDetails
    review_reasons: list[str]
    type: str
    verification_status: list[str]
    verification_tags: str


class BusinessEntityDict(TypedDict):
    """
    A dictionary type representing partial information about a business entity.

    Attributes:
    - ein (str): The EIN of the business.
    - business_name (str): The name of the business.
    - website (str | None): The website of the business, if available.
    - legal_type (str | None): The legal type of the business, if available.
    - address (Address): The address of the business.
    - beneficial_owners (list[BeneficialOwner]): A list of beneficial owners of the business.
    """

    ein: str
    business_name: str
    website: str | None  # Optional
    legal_type: str | None  # Optional
    address: AddressDict
    beneficial_owners: list[BeneficialOwnerDict]
