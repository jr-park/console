from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.association import UserRole, PermissionRole
from app.schemas.user import UserInDBCreate, UserInDBUpdate


class CRUDUser(CRUDBase[User, UserInDBCreate, UserInDBUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_user_permission(self, db: Session, *, current_user: User) -> Any:
        permissions_in_user = db.query(Permission).join(PermissionRole, PermissionRole.permission_name == Permission.permission_name)\
            .join(UserRole, UserRole.role_name == PermissionRole.role_name)\
            .join(User, UserRole.username == User.username).filter(User.username == current_user.username).all()

        return permissions_in_user


    def get_user_role(self, db: Session, *, current_user: User) -> Any:
        roles_in_user = db.query(Role).join(UserRole, Role.role_name == UserRole.role_name)\
            .join(User, User.username == UserRole.username)\
            .filter(User.username == current_user.username).all()

        return roles_in_user


    def create(self, db: Session, *, obj_in: UserInDBCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserInDBUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
