from typing import Optional, Literal, Annotated
from pydantic import BaseModel, BeforeValidator
from fastapi import APIRouter, Depends, Body
from datetime import datetime
from ashtree.errors import AuthenticationError, BadRequest
from app.auth import AuthData, current_session, auth_required
from app.models import User, Session

account_ctrl = APIRouter(prefix="/api/v1/account")


class AccountMeResponse(BaseModel):
    id: Annotated[Optional[str], BeforeValidator(str)]
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    ext_id: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LogoutResponse(BaseModel):
    detail: Literal["logged out"] = "logged out"


class AuthenticationRequest(BaseModel):
    username: str
    password: str


@account_ctrl.get("/me")
async def me(auth_data: AuthData = Depends(auth_required(["users:read:me"]))) -> AccountMeResponse:
    return AccountMeResponse(**auth_data.user.to_dict())


@account_ctrl.post("/authenticate")
async def authenticate(
        auth_request: AuthenticationRequest = Body(),
        session: Session = Depends(current_session)) -> AccountMeResponse:

    user = await session.user()
    if user:
        raise BadRequest("already authenticated")

    user = await User.get(auth_request.username)
    if user is None or not user.check_password(auth_request.password):
        raise AuthenticationError()
    session.user_id = user.id

    return AccountMeResponse(**user.to_dict())


@account_ctrl.post("/logout")
async def logout(session: Session = Depends(current_session)) -> LogoutResponse:
    session.user_id = None
    return LogoutResponse(detail="logged out")
