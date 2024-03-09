from pydantic import BaseModel


class Entry(BaseModel):
    """
    Represents an entry in a tree.
    """

    name: str
    oid: str
