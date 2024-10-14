import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Annotated, Optional, List
from mongey.models import TimestampedModel
from mongey.models.fields import StringField, ReferenceField
from pydantic import BaseModel, BeforeValidator
from ashtree.errors import ConfigurationError, IntegrityError
from ashtree.permissions import pm
from app.context import ctx
from ashtree.util import resolve_id
from .role import Role, RoleResponse


class User(TimestampedModel):

    COLLECTION = "users"
    KEY_FIELD = "username"

    username = StringField(required=True, unique=True)
    first_name = StringField(default="")
    last_name = StringField(default="")
    email = StringField(default="", unique=True)
    password_hash = StringField(default="-", rejected=True, restricted=True)
    avatar_url = StringField(default="")
    role_id: ReferenceField[Role] = ReferenceField(reference_model=Role, required=True)

    def set_password(self, password: str) -> None:
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        password_hash = self.password_hash
        if password_hash is None:
            return False
        
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            )
        except ValueError as e:
            ctx.log.error(e)
            # password not set leads to bcrypt raising ValueError("invalid salt")
            return False

    async def role(self) -> Optional[Role]:
        return await Role.get(self.role_id)

    async def generate_token(self, permissions: Optional[List[str]] = None, ttl: Optional[timedelta] = None) -> str:
        if not ctx.cfg.jwt.enabled:
            raise ConfigurationError("jwt is disabled in config")
        
        try:
            import jwt # type: ignore
        except ImportError:
            raise RuntimeError("pyjwt package must be installed to use jwt auth")

        if permissions is None:
            r = await self.role()
            if r is None:
                raise IntegrityError(f"user {self.id} does not have a role")
            permissions = r.permissions
            if permissions is None:
                raise IntegrityError(f"role {r.id} permissions are None")

        now = datetime.now(UTC)
        if ttl is None:
            ttl = timedelta(days=365)
        exp = now + ttl

        payload = {
            "user_id": str(self.id),
            "permissions": pm.to_numeric(permissions),
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, ctx.cfg.jwt.secret_key, algorithm="HS256")


class UserResponse(BaseModel):
    id: Annotated[Optional[str], BeforeValidator(resolve_id)] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    role_id: Annotated[Optional[str], BeforeValidator(resolve_id)] = None
    role: Optional[RoleResponse] = None
