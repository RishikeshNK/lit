from typing import ClassVar, List
from pydantic import BaseModel
from lit.constants import REPO_NAME
import os

class Workspace(BaseModel):
    IGNORE: ClassVar[set[str]] = {REPO_NAME, ".git"}

    pathname: str

    def list_files(self) -> List[str]:
        """
        List files in the workspace, excluding ignored files/directories.

        :return: List of files in the workspace.
        """
        return [entry for entry in os.listdir(self.pathname) if entry not in self.IGNORE]
