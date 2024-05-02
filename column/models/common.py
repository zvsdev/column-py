from datetime import datetime
from typing import NotRequired, TypedDict


class CreatedParams(TypedDict):
    gt: NotRequired[datetime]
    lt: NotRequired[datetime]
    gte: NotRequired[datetime]
    lte: NotRequired[datetime]
