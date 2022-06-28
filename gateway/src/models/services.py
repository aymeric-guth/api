from pydantic import Field

from .base import Base


class Service(Base):
    id_: int = Field(0, alias="id")
    name: str
