from typing import List, Literal, Optional, Annotated
from uuid import uuid4
from datetime import datetime, UTC
from logging import getLevelNamesMapping
from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from bson.objectid import ObjectId
from bson.errors import InvalidId

LogLevelName = Literal["debug", "info", "warn", "error", "critical"]


def uuid4_string() -> str:
    return str(uuid4())


def resolve_id(id_: str | ObjectId | None) -> ObjectId | str | None:
    # ObjectId(None) generates a new unique object id
    # We need to handle that case and return None instead
    if id_ is not None:
        if not isinstance(id_, ObjectId):
            try:
                objid_expr = ObjectId(id_)
                if str(objid_expr) == id_:
                    return objid_expr
            except (InvalidId, TypeError):
                pass
    return id_


# Mongo stores datetime rounded to milliseconds as its datetime
# capabilities are limited by v8 engine
def now() -> datetime:
    dt = datetime.now(UTC)
    dt = dt.replace(microsecond=dt.microsecond // 1000 * 1000)
    return dt


NilObjectId: ObjectId = ObjectId("000000000000000000000000")


def validate_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("invalid object id")


def validate_object_id_list(value: str) -> List[ObjectId]:
    try:
        return [ObjectId(token) for token in validate_string_list(value)]
    except InvalidId:
        raise ValueError("invalid object id list")


def validate_string_list(value: str) -> List[str]:
    return [token.strip() for token in value.split(",")]


def convert_object_id_to_str(value: Optional[ObjectId]) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def convert_log_level(log_level: LogLevelName) -> int:
    return getLevelNamesMapping().get(log_level.upper()) # type: ignore


class MongeyBaseModel(BaseModel):
    """
    MongeyBaseModel is a preconfigured pydantic BaseModel for easier convertion
    from mongey models to FastAPI response objects.
    """
    id: Annotated[Optional[str], BeforeValidator(convert_object_id_to_str)]

    class Config:
        from_attributes = True
