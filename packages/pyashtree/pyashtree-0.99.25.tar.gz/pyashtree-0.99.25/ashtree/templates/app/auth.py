from typing import Iterable, List, Callable, Optional, Awaitable
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ashtree.errors import ConfigurationError, AuthenticationError, Forbidden, IntegrityError
from ashtree.permissions import pm
from app.models import User, Session
from app.context import ctx

bearer = HTTPBearer(auto_error=False)


class AuthData:
    user: User
    permissions: List[str]

    def __init__(self, user: User, permissions: Iterable[str]):
        self.user = user
        self.permissions = list(permissions)


async def current_session(request: Request) -> Session:
    return request.state.session


def auth_required(required: Iterable[str]) -> Callable[..., Awaitable[AuthData]]:
    for action in required:
        pm.add_action(action)

    if ctx.cfg.jwt.enabled:
        try:
            import jwt # type: ignore
        except ImportError:
            raise RuntimeError("pyjwt package must be installed to use jwt auth")

    if ctx.cfg.jwt.enabled and ctx.cfg.jwt.secret_key is None:
        raise ConfigurationError("jwt.secret_key must be configured to use jwt")

    bin_required: Optional[int] = None

    async def inner(
        session: Session = Depends(current_session),
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer)
    ) -> AuthData:

        nonlocal bin_required
        if bin_required is None:
            bin_required = pm.to_numeric(required)

        if credentials:
            if not ctx.cfg.jwt.enabled:
                raise AuthenticationError("jwt auth is disabled")
            if credentials.scheme != "Bearer":
                raise Forbidden(f"scheme {credentials.scheme} is not supported")

            token = credentials.credentials
            try:
                payload = jwt.decode(
                    token,
                    ctx.cfg.jwt.secret_key,
                    options={"require": ["exp", "iat"]},
                    algorithms=["HS256"]
                )
            except jwt.InvalidSignatureError:
                raise Forbidden("token signature verification failed")
            except jwt.ExpiredSignatureError:
                raise Forbidden("token expired")
            except jwt.MissingRequiredClaimError as e:
                raise Forbidden(f"token is missing claim {e.claim}")

            user_id = payload.get("user_id")
            if user_id is None:
                raise Forbidden("user_id is missing from token")

            user = await User.get(user_id)
            if user is None:
                raise Forbidden("user provided in the token was not found")

            # todo check permissions
            token_permissions: int = payload.get("permissions", [])
            if not pm.check(token_permissions, bin_required):
                raise Forbidden("you don't have permissions required for this action")

            ctx.log.debug(f"session authorized with JWT as username={user.username}, permissions={pm.from_numeric(token_permissions)} "
                          f"({token_permissions})")
            return AuthData(user=user, permissions=pm.from_numeric(token_permissions))

        user = await User.get(session.user_id)
        if user is None:
            raise AuthenticationError()

        role = await user.role()
        if role is None:
            raise IntegrityError(f"user {user.id} does not have a role")

        permissions = role.permissions
        if permissions is None:
            raise IntegrityError(f"role {role.id} permissions are None")

        if not pm.check(pm.to_numeric(permissions), required):
            raise Forbidden("you don't have permissions required for this action")

        ctx.log.debug(f"session authorized with cookie as username={user.username}, permissions={role.permissions}")
        return AuthData(user=user, permissions=permissions)

    return inner
