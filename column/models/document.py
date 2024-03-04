from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel


class Document(BaseModel):
    checksum: str
    created_at: datetime
    description: str
    id: str
    size: int
    type: str
    updated_at: datetime
    url: str


class DocumentSubmitDict(TypedDict):
    document_front_id: str
    document_back_id: Optional[str]
    description: Optional[str]
