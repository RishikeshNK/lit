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
        return [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(self.pathname)
            for filename in filenames
            if os.path.isfile(os.path.join(root, filename)) and filename not in self.IGNORE
        ]

    def read_file(self, file_name: str) -> str:
        """
        Read the contents of a file in the workspace.

        :param file_name: Name of the file to read.
        :return: Contents of the file.
        """
        file_path = os.path.join(self.pathname, file_name)
        with open(file_path, "r") as file:
            return file.read()
