from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user
from app.core.config import settings
from app.core.database import get_db_session
from app.core.security import hash_session_token, new_session_token, verify_password
from app.models.identity import AuthSession, User
from app.schemas.auth import CurrentUser, LoginRequest, MessageResponse

router = APIRouter()


def serialize_user(user: User) -> CurrentUser:
    return CurrentUser(id=user.id, username=user.username, display_name=user.display_name,
                       status=user.status, roles=[role.code for role in user.roles])


@router.post("/login", response_model=CurrentUser)
async def login(payload: LoginRequest, request: Request, response: Response,
                db: AsyncSession = Depends(get_db_session)) -> CurrentUser:
    user = (await db.scalars(select(User).where(User.username == payload.username))).first()
    if not user or user.status != "active" or not verify_password(user.password_hash, payload.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "用户名或密码错误")
    now = datetime.now(UTC)
    token = new_session_token()
    db.add(AuthSession(token_hash=hash_session_token(token), user_id=user.id, created_at=now,
                       expires_at=now + timedelta(hours=settings.session_ttl_hours)))
    user.last_login_at = now
    await db.commit()
    response.set_cookie(settings.session_cookie_name, token, httponly=True,
                        secure=settings.cookie_secure, samesite="lax", max_age=settings.session_ttl_hours * 3600)
    return serialize_user(user)


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response,
                 token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
                 db: AsyncSession = Depends(get_db_session)) -> MessageResponse:
    if token:
        session = (await db.scalars(select(AuthSession).where(AuthSession.token_hash == hash_session_token(token)))).first()
        if session:
            session.revoked_at = datetime.now(UTC)
            await db.commit()
    response.delete_cookie(settings.session_cookie_name)
    return MessageResponse(message="已退出")


@router.get("/me", response_model=CurrentUser)
async def me(user: User = Depends(current_user)) -> CurrentUser:
    return serialize_user(user)
