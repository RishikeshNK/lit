import hashlib
import os
import random
import string
import zlib
from typing import Union
from lit.models.blob import Blob
from pydantic import BaseModel


class Database(BaseModel):
    pathname: str

    def store(self, obj: Blob) -> None:
        """
        Store a blob object in the database.

        :param obj: Blob object to store.
        """
        content = f"{obj.type} {len(obj.data)}\0{obj.data}".encode("utf-8")
        oid = hashlib.sha1(content).hexdigest()
        self.__write_object(oid, content)

    def __write_object(self, oid: str, content: bytes) -> None:
        """
        Write object content to the database.

        :param oid: Object ID.
        :param content: Content of the object.
        """
        object_path = os.path.join(self.pathname, oid[:2], oid[2:])
        dirname = os.path.dirname(object_path)
        temp_path = os.path.join(dirname, self.__generate_temp_name())

        os.makedirs(dirname, exist_ok=True)
        with open(temp_path, "wb") as file:
            compressed = zlib.compress(content, level=zlib.Z_BEST_SPEED)
            file.write(compressed)
        os.rename(temp_path, object_path)

    def __generate_temp_name(self) -> str:
        """
        Generate a temporary file name.

        :return: Temporary file name.
        """
        return f"tmp_obj_{''.join(random.choices(string.ascii_letters + string.digits, k=6))}"
