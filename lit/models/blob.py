from hashlib import sha1
from typing import Optional
from pydantic import BaseModel


class Blob(BaseModel):
    data: str
    object_id: Optional[str] = None

    @property
    def type(self) -> str:
        return "blob"

    def __str__(self) -> str:
        return self.data
