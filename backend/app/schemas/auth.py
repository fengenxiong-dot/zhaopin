import uuid

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=8, max_length=200)


class CurrentUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    display_name: str
    status: str
    roles: list[str]


class MessageResponse(BaseModel):
    message: str
