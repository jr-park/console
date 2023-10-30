from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserInDB
from app.schemas.role import Role


class UserWithAssociation(UserInDB):
    roles: List[Role]


class PermissionRoleBase(BaseModel):
    permission_name: str
    role_name: str


class PermissionRoleInDBBase(PermissionRoleBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class PermissionRole(PermissionRoleInDBBase):
    pass


class PermissionRoleCreate(PermissionRoleBase):
    pass
