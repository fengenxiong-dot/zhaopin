from datetime import UTC, datetime

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db_session
from app.core.security import hash_session_token
from app.models.identity import AuthSession, User


async def current_user(
    token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "请先登录")
    stmt = select(AuthSession).where(
        AuthSession.token_hash == hash_session_token(token),
        AuthSession.revoked_at.is_(None),
        AuthSession.expires_at > datetime.now(UTC),
    )
    auth_session = (await db.scalars(stmt)).first()
    if not auth_session or auth_session.user.status != "active":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "会话已失效")
    return auth_session.user


def require_roles(*allowed: str):
    async def dependency(user: User = Depends(current_user)) -> User:
        if not {role.code for role in user.roles}.intersection(allowed):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "无权执行此操作")
        return user
    return dependency
