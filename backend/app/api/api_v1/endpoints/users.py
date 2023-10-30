from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email


router = APIRouter()


@router.get("/", response_model=List[schemas.UserWithAssociation])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.UserWithAssociation)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserInDBCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    try:
        user = crud.user.create(db, obj_in=user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user


@router.put("/me", response_model=schemas.UserInDB)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserInDBUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.UserWithAssociation)
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        permissions: models.Permission = Depends(deps.get_current_user_permission)
) -> Any:
    user_roles = crud.user.get_user_role(db=db,current_user=current_user)
    return current_user, { "roles": list(user_roles) }


@router.post("/open", response_model=schemas.UserInDB)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{username}", response_model=schemas.UserInDB)
def read_user_by_username(
    username: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud.user.get_by_username(db, username=username)
    if user == current_user:
        return user
    return user


@router.put("/{username}", response_model=schemas.UserInDB)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    username: str,
    user_in: schemas.UserInDBUpdate,
    permissions: models.Permission = Depends(deps.get_current_user_permission)
) -> Any:
    user = crud.user.get(db, pk=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
