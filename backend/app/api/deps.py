from typing import Generator, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import JWT
from jwt.jwk import jwk_from_dict
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), jwt: JWT = Depends(security.get_jwt), token: str = Depends(reusable_oauth2)
) -> Union[models.User, schemas.UserInLinux]:
    try:
        signing_key = jwk_from_dict({
            'kty': 'oct',
            'k': settings.PRIVATE_KEY
        })
        payload = jwt.decode(
            token, signing_key, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.InvalidTokenError, jwt.ExpiredSignature, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get_by_username(db, username=token_data.sun)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_user_permission(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
) -> models.Permission:
    user_permission: models.Permission = crud.user.get_user_permission(db=db,current_user=current_user)
    return list(user_permission)
