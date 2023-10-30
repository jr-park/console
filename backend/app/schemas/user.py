from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserInDBCreate(UserBase):
    username: str
    password: str


class UserInDBUpdate(UserBase):
    password: str = None


class UserInDB(UserBase):

    class Config:
        from_attributes = True


class UserInLinux(UserBase):
    uid: int
    gid: int
    gecos: Optional[str] = None
    home_directory: str
    login_shell: str

    class Config:
        from_attributes = True
