from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.Permission])
def read_permissions(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        permissions: models.Permission = Depends(deps.get_current_user_permission)
) -> Any:
    permissions = crud.permission.get_multi(db, skip=skip, limit=limit)
    return permissions

@router.post("/", response_model=schemas.Permission)
def create_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_in: schemas.PermissionCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new user.
    """
    permission = crud.permission.get_by_permission_name(db, permission_name=permission_in.permission_name)
    if permission:
        raise HTTPException(
            status_code=400,
            detail="The permission with this permission name already exists in the system.",
        )
    permission = crud.permission.create(db, obj_in=permission_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return permission
