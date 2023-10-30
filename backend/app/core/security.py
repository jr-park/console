import time
from typing import Any, Union

from passlib.context import CryptContext

from jwt import JWT
from jwt.jwk import jwk_from_dict

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def get_jwt() -> JWT:
    return JWT()


def create_access_token(
        subject: Union[str, Any], expires_delta: int = None
) -> str:
    signing_key = jwk_from_dict({
        'kty': 'oct',
        'k': settings.PRIVATE_KEY
    })
    if expires_delta:
        expire = int(time.time() + expires_delta)
    else:
        expire = int(time.time() + settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "iat": int(time.time()),
        "sun": str(subject)
    }
    encoded_jwt = get_jwt().encode(to_encode, signing_key, alg=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
