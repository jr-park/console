from typing import Any, Dict, List, Optional, Union
from sqlalchemy import URL
from pydantic import AnyHttpUrl, validator, Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    PRIVATE_KEY : str = Field(default='', validation_alias='jwt_private_key')
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str = 'localhost'
    # SERVER_HOST: AnyHttpUrl = 'http://localhost'
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]']

    ## CORS는 Main에서 하드코딩하는게 맞는거 같음...
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'console'
    # SENTRY_DSN: Optional[HttpUrl] = None
    # SENTRY_DSN: Optional[str] = 'http://localhost'
    #
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    MYSQL_SERVER: str = Field(default='', validation_alias='mysql_server')
    MYSQL_PORT: int = Field(default=3306, validation_alias='mysql_port')
    MYSQL_USERNAME: str = Field(default='', validation_alias='mysql_user')
    MYSQL_PASSWORD: str = Field(default='', validation_alias='mysql_password')
    MYSQL_DB: str = Field(default='', validation_alias='mysql_db')

    SQLALCHEMY_DATABASE_URI: Union[str, URL] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    @classmethod
    def assemble_db_connection(cls, v: Optional[URL], values: Dict[str, Any]) -> URL:
        if isinstance(v, URL):
            return v
        return URL.create(
            drivername="mysql",
            username=values.get("MYSQL_USERNAME"),
            password=values.get("MYSQL_PASSWORD"),
            host=values.get("MYSQL_SERVER"),
            port=values.get("MYSQL_PORT"),
            database=f"{values.get('MYSQL_DB') or ''}",
        )

    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = 25
    SMTP_HOST: Optional[str] = 'localhost'
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = "ggaeuk@naver.com"
    EMAILS_FROM_NAME: Optional[str] = "jrpark"
    #
    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v
    #
    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"
    EMAILS_ENABLED: bool = True
    #
    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )
    #
    # EMAIL_TEST_USER: EmailStr = "test@samsung.com"  # type: ignore
    # FIRST_SUPERUSER: EmailStr = "admin@samsung.com"
    # FIRST_SUPERUSER_PASSWORD: str = "imsi0000"
    # USERS_OPEN_REGISTRATION: bool = False

    JWT_PRIVATE_KEY: str = Field(default='', validation_alias='jwt_private_key')
    SLURM_CTL_HOST: str = Field(default='localhost', validation_alias='slurm_ctl_host')
    SSH_PORT: int = Field(default=22, validation_alias='ssh_port')
    SLURM_REST_PORT: int = Field(default=6820, validation_alias='slurm_rest_port')
    SLURM_USER: str = Field(default='', validation_alias='slurm_user')
    SLURM_PASSWORD: str = Field(default='', validation_alias='slurm_password')

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
