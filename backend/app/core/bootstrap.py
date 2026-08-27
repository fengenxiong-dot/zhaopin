from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session_factory
from app.core.security import hash_password
from app.models.identity import Role, User

ROLE_NAMES = {
    "HR": "普通 HR",
    "RECRUITMENT_MANAGER": "招聘管理者",
    "SYSTEM_ADMIN": "系统管理员",
}


async def bootstrap_identity() -> None:
    async with async_session_factory() as db:
        roles: dict[str, Role] = {}
        for code, name in ROLE_NAMES.items():
            role = (await db.scalars(select(Role).where(Role.code == code))).first()
            if not role:
                role = Role(code=code, name=name)
                db.add(role)
            roles[code] = role
        await db.flush()
        admin = (await db.scalars(select(User).where(User.username == settings.bootstrap_admin_username))).first()
        if not admin:
            admin = User(
                username=settings.bootstrap_admin_username,
                display_name=settings.bootstrap_admin_display_name,
                password_hash=hash_password(settings.bootstrap_admin_password),
                status="active",
                roles=[roles["SYSTEM_ADMIN"]],
            )
            db.add(admin)
        await db.commit()
