from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.config import Settings
from app.schemas.config import SettingsCreate, SettingsUpdate


class CRUDSettings(CRUDBase[Settings, SettingsCreate, SettingsUpdate]):
    def get_by_variable_name(self, db: Session, *, variable_name: str) -> Optional[Settings]:
        return db.query(Settings).filter(Settings.variable_name == variable_name).first()

    def create(self, db: Session, *, obj_in: SettingsCreate) -> Settings:
        db_obj = Settings(
            variable_name=obj_in.variable_name,
            value=obj_in.value
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


settings = CRUDSettings(Settings)
