from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=schemas.Settings)
def read_settings_by_variable_name(
        variable_name: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    settings = crud.settings.get_by_variable_name(db, variable_name=variable_name)
    if not settings:
        raise HTTPException(
            status_code=400, detail="아직 ldap 설정이 되지 않았습니다."
        )
    return settings


@router.post("/", response_model=schemas.Settings)
def create_variable(
        *,
        db: Session = Depends(deps.get_db),
        variable_in: schemas.SettingsCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    settings = crud.settings.get_by_variable_name(db, variable_name=variable_in.variable_name)
    if settings:
        raise HTTPException(
            status_code=400,
            detail="The variable with this name already exists in the system."
        )
    settings = crud.settings.create(db, obj_in=variable_in)
    return settings
