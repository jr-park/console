from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_permission_name(self, db: Session, *, permission_name: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.permission_name == permission_name).first()


permission = CRUDPermission(Permission)
