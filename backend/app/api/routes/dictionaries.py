import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user, require_roles
from app.core.database import get_db_session
from app.models.identity import DictionaryItem, DictionaryType, User
from app.schemas.admin import DictionaryItemCreate, DictionaryItemUpdate, DictionaryTypeCreate

router = APIRouter()


@router.get("")
async def list_dictionaries(_: User = Depends(current_user), db: AsyncSession = Depends(get_db_session)):
    types = (await db.scalars(select(DictionaryType).order_by(DictionaryType.name))).all()
    result = []
    for item_type in types:
        items = (await db.scalars(select(DictionaryItem).where(DictionaryItem.dictionary_type_id == item_type.id).order_by(DictionaryItem.sort_order))).all()
        result.append({"id": item_type.id, "code": item_type.code, "name": item_type.name,
                       "items": [{"id": x.id, "code": x.code, "name": x.name,
                                  "sort_order": x.sort_order, "is_active": x.is_active} for x in items]})
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_type(payload: DictionaryTypeCreate,
                      _: User = Depends(require_roles("RECRUITMENT_MANAGER", "SYSTEM_ADMIN")),
                      db: AsyncSession = Depends(get_db_session)):
    item_type = DictionaryType(**payload.model_dump())
    db.add(item_type); await db.commit(); await db.refresh(item_type)
    return item_type


@router.post("/{type_id}/items", status_code=status.HTTP_201_CREATED)
async def create_item(type_id: uuid.UUID, payload: DictionaryItemCreate,
                      _: User = Depends(require_roles("RECRUITMENT_MANAGER", "SYSTEM_ADMIN")),
                      db: AsyncSession = Depends(get_db_session)):
    if not await db.get(DictionaryType, type_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "字典类型不存在")
    item = DictionaryItem(dictionary_type_id=type_id, **payload.model_dump())
    db.add(item); await db.commit(); await db.refresh(item)
    return item


@router.patch("/items/{item_id}")
async def update_item(item_id: uuid.UUID, payload: DictionaryItemUpdate,
                      _: User = Depends(require_roles("RECRUITMENT_MANAGER", "SYSTEM_ADMIN")),
                      db: AsyncSession = Depends(get_db_session)):
    item = await db.get(DictionaryItem, item_id)
    if not item: raise HTTPException(status.HTTP_404_NOT_FOUND, "字典项不存在")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    await db.commit(); await db.refresh(item)
    return item
