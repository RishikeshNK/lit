from pydantic import BaseModel
from typing import List, Optional, ClassVar

from lit.models.entry import Entry


class Tree(BaseModel):
    """
    Represents a Tree in the Lit repository.
    """

    ENTRY_FORMAT: ClassVar[str] = "Z*H40"
    MODE: ClassVar[str] = "100644"

    entries: List[Entry]
    object_id: Optional[str] = None

    @property
    def type(self) -> str:
        """
        Returns the type of the object (in this case, 'tree').

        :return: the type of the object.
        """
        return "tree"

    def __str__(self) -> str:
        """
        Return a string representation of the tree.

        :return: String representation of the tree.
        """
        # TODO: Entry format is probably incorrect.
        sorted_entries = sorted(self.entries, key=lambda x: x.name)
        formatted_entries = [
            f"{self.MODE} {entry.name}\0{entry.oid}" for entry in sorted_entries
        ]
        return "\n".join(formatted_entries)
