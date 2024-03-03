from datetime import datetime

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
