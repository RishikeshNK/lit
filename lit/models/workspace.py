from typing import ClassVar, List
from pydantic import BaseModel
from lit.constants import REPO_NAME
import os


class Workspace(BaseModel):
    IGNORE: ClassVar[set[str]] = {REPO_NAME, ".git"}

    pathname: str

    def list_files(self) -> List[str]:
        """
        List files in the workspace, excluding ignored files/directories. Might have a cubic runtime complexity.

        :return: List of files in the workspace.
        """
        return [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(self.pathname)
            for filename in filenames
            if not any(
                ignore_dir in root.split(os.path.sep) for ignore_dir in self.IGNORE
            )
        ]

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """
        Read the contents of a file in the workspace.

        :param path: Path of the file to read.
        :param encoding: Encoding to use for reading the file (default is 'utf-8').
        :return: Contents of the file.
        """
        with open(path, "r", encoding=encoding) as file:
            try:
                return file.read()
            except UnicodeDecodeError:
                # Temporary fix till I figure out a better way to handle this!
                alternative_encodings = ["latin-1", "utf-16", "iso-8859-1", "cp1252"]
                for alt_encoding in alternative_encodings:
                    try:
                        with open(path, "r", encoding=alt_encoding) as alt_file:
                            return alt_file.read()
                    except UnicodeDecodeError:
                        pass
                raise UnicodeDecodeError(
                    f"Unable to decode file '{path}' using any of the specified encodings."
                )
