from typing import TypeVar, Generic
from pydantic import BaseModel, ConfigDict

from tortoise_api_model.enum import UserStatus, UserRole


RootModelType = TypeVar("RootModelType")


class PydList(BaseModel, Generic[RootModelType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: list[RootModelType]
    total: int


class UserPwd(BaseModel):
    password: str


class UserReg(UserPwd):
    username: str
    email: str | None = None
    phone: int | None = None


class UserUpdate(BaseModel):
    username: str
    status: UserStatus
    email: str | None
    phone: int | None
    role: UserRole


class UserAuth(UserUpdate):
    id: int
    username: str
    status: UserStatus
    role: UserRole
    # ref_id: int | None


class Names(BaseModel):
    # models for name endpoint for select2 inputs
    class Name(BaseModel):
        id: int
        text: str
        logo: str | None = None
        selected: bool | None = None

    class Pagination(BaseModel):
        more: bool

    results: list[Name]
    pagination: Pagination
