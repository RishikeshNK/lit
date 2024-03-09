from hashlib import sha1
from typing import Optional
from pydantic import BaseModel


class Blob(BaseModel):
    """
    Represents a Blob in the Lit repository.
    """

    data: str
    object_id: Optional[str] = None

    @property
    def type(self) -> str:
        """
        Returns the type of the object (in this case, 'blob').

        :return: The type of the object.
        """
        return "blob"

    def __str__(self) -> str:
        """
        Return a string representation of the blob.

        :return: String representation of the blob.
        """
        return self.data
