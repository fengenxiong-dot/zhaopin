import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_roles
from app.core.database import get_db_session
from app.core.security import hash_password
from app.models.identity import Role, User
from app.schemas.admin import UserCreate, UserUpdate, UserView

router = APIRouter(dependencies=[Depends(require_roles("SYSTEM_ADMIN"))])


def view(user: User) -> UserView:
    return UserView(id=user.id, username=user.username, display_name=user.display_name,
                    status=user.status, roles=[role.code for role in user.roles])


async def resolve_roles(db: AsyncSession, codes: list[str]) -> list[Role]:
    roles = list((await db.scalars(select(Role).where(Role.code.in_(codes)))).all())
    if len(roles) != len(set(codes)):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "存在无效角色")
    return roles


@router.get("", response_model=list[UserView])
async def list_users(db: AsyncSession = Depends(get_db_session)) -> list[UserView]:
    return [view(user) for user in (await db.scalars(select(User).order_by(User.created_at))).unique().all()]


@router.post("", response_model=UserView, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session)) -> UserView:
    if (await db.scalars(select(User).where(User.username == payload.username))).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "用户名已存在")
    user = User(username=payload.username, display_name=payload.display_name,
                password_hash=hash_password(payload.password), status="active",
                roles=await resolve_roles(db, payload.role_codes))
    db.add(user)
    await db.commit()
    await db.refresh(user, attribute_names=["roles"])
    return view(user)


@router.patch("/{user_id}", response_model=UserView)
async def update_user(user_id: uuid.UUID, payload: UserUpdate,
                      db: AsyncSession = Depends(get_db_session)) -> UserView:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "用户不存在")
    if payload.display_name is not None: user.display_name = payload.display_name
    if payload.status is not None:
        if payload.status not in {"active", "disabled"}:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "账号状态无效")
        user.status = payload.status
    if payload.password is not None: user.password_hash = hash_password(payload.password)
    if payload.role_codes is not None: user.roles = await resolve_roles(db, payload.role_codes)
    await db.commit()
    await db.refresh(user, attribute_names=["roles"])
    return view(user)
