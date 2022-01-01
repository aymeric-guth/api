from typing import List, Any
import datetime

import orjson
from pydantic import BaseConfig, BaseModel, Field, validator


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


# class Base(BaseModel):
#     class Config(BaseConfig):
#         allow_population_by_field_name = True
#         json_encoders = {datetime.datetime: convert_datetime_to_realworld}
#         alias_generator = convert_field_to_camel_case
#
#     id_: int = Field(0, alias="id")
#     created_at: datetime.datetime = None
#     updated_at: datetime.datetime = None
#
#     @validator("created_at", "updated_at", pre=True)
#     def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
#         return value or datetime.datetime.now()


class Base(BaseModel):
    class Config(BaseConfig):
        json_loads = orjson.loads
        json_dumps = orjson.dumps

    @classmethod
    def get_keys(cls) -> List[str]:
        return cls.schema().get('properties').keys()

    def tuple(self) -> List[Any]:
        keys = self.get_keys()
        return [getattr(self, i) for i in keys]
