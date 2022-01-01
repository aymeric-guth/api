import datetime

from pydantic import BaseConfig, BaseModel

import orjson


class Base(BaseModel):
    # id_: int = Field(0, alias="id")

    class Config(BaseConfig):
        json_loads = orjson.loads
        json_dumps = orjson.dumps
        allow_population_by_field_name = True
        json_encoders = {
            datetime.datetime: lambda dt: dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }
        # alias_generator = convert_field_to_camel_case

    # @validator("created_at", "updated_at", pre=True)
    # def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
    #     return value or datetime.datetime.now()
