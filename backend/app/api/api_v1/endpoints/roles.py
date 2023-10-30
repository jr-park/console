from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.Role])
def read_roles(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        permissions: models.Permission = Depends(deps.get_current_user_permission)
) -> Any:
    roles = crud.role.get_multi(db, skip=skip, limit=limit)
    return roles


@router.post("/", response_model=schemas.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new user.
    """
    role = crud.role.get_by_role_name(db, role_name=role_in.role_name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this role name already exists in the system.",
        )
    role = crud.role.create(db, obj_in=role_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return role


@router.put("/{role_name}", response_model=schemas.Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_name: str,
    role_in: schemas.RoleUpdate,
    permissions: models.Permission = Depends(deps.get_current_user_permission)
) -> Any:
    role = crud.role.get_by_role_name(db, role_name=role_name)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this role name does not exist in the system",
        )
    role = crud.role.update(db, db_obj=role, obj_in=role_in)
    return role


@router.post("/add_permissions", response_model=List[schemas.PermissionRole])
def add_permissions_to_role(
        *,
        db: Session = Depends(deps.get_db),
        permission_role_ins: List[schemas.PermissionRoleCreate],
        permissions: models.Permission = Depends(deps.get_current_user_permission),
) -> Any:
    permission_role = crud.role.add_permissions_to_role(db, obj_ins=permission_role_ins)
    if not permission_role:
        raise HTTPException(
            status_code=404,
            detail="can't add permission to the role",
        )

    return permission_role
