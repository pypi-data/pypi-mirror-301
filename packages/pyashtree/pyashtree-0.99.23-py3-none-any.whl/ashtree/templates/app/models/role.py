from typing import Annotated, List, Optional
from mongey.models import TimestampedModel
from mongey.models.fields import StringField, ListField
from pydantic import BaseModel, BeforeValidator

from ashtree.util import resolve_id


SUPERVISOR_ROLE_NAME = "supervisor"
DEFAULT_ROLE_NAME = "user"

SUPERVISOR_ROLE_PERMISSIONS = [
    "users:read:me",
    "users:read:others"
]

DEFAULT_ROLE_PERMISSIONS = [
    "users:read:me",
    "users:read:others"
]


class Role(TimestampedModel):

    COLLECTION = "roles"
    KEY_FIELD = "name"

    name = StringField(required=True, unique=True)
    permissions: ListField[str] = ListField(required=True, default=list)

    @classmethod
    async def supervisor(cls) -> "Role":
        role = await Role.get(SUPERVISOR_ROLE_NAME)
        if role is None:
            role = Role({"name": SUPERVISOR_ROLE_NAME, "permissions": SUPERVISOR_ROLE_PERMISSIONS})
            await role.save()
        return role

    @classmethod
    async def default(cls) -> "Role":
        role = await Role.get(DEFAULT_ROLE_NAME)
        if role is None:
            role = Role({"name": DEFAULT_ROLE_NAME, "permissions": DEFAULT_ROLE_PERMISSIONS})
            await role.save()
        return role


class RoleResponse(BaseModel):
    id: Annotated[Optional[str], BeforeValidator(resolve_id)] = None
    name: Optional[str] = None
    permissions: Optional[List[str]] = None
