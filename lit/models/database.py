from pydantic import BaseModel


class Database(BaseModel):
    pathname: str
