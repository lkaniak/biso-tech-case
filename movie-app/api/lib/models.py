from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator
from sqlmodel import SQLModel

from api.lib.utils import convert_datetime_to_gmt


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        """zera os microssegundos do datetime"""
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Retorna um dict apenas com os campos serializaveis"""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)


class ListData(BaseModel):
    count: int
    data: list[Any]


class Message(SQLModel):
    message: str
