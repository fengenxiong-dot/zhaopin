import uuid

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=80)
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=200)
    role_codes: list[str] = Field(min_length=1)


class UserUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    status: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=200)
    role_codes: list[str] | None = None


class UserView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    username: str
    display_name: str
    status: str
    roles: list[str]


class DictionaryTypeCreate(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class DictionaryItemCreate(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=100)
    sort_order: int = 0


class DictionaryItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    sort_order: int | None = None
    is_active: bool | None = None
