from typing import Optional

from pydantic import BaseModel


class PermissionBase(BaseModel):
    permission_name: Optional[str] = None


class PermissionInDBBase(PermissionBase):
    id: Optional[int] = None


class Permission(PermissionInDBBase):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass
