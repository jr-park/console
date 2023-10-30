from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    role_name: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    pass


class Role(RoleInDBBase):
    pass
