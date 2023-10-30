from typing import Any, Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.role import Role
from app.models.association import PermissionRole
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.association import PermissionRoleCreate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_role_name(self, db: Session, *, role_name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.role_name == role_name).first()

    def add_permissions_to_role(self, db: Session, *, obj_ins: List[PermissionRoleCreate]) -> Any:
        db_objs = []
        for obj_in in obj_ins:
            db_obj = PermissionRole(permission_name=obj_in.permission_name, role_name=obj_in.role_name)
            db.add(db_obj)
            db_objs.append(db_obj)
        ## try - except 처리 필요
        try:
            db.commit()
        except:
            return []
        return db_objs


role = CRUDRole(Role)
