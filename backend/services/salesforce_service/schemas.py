from pydantic import BaseModel
from typing import Optional

class SyncRequest(BaseModel):
    entity_type: str
    data: dict
