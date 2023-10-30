from typing import Optional

from pydantic import BaseModel


class SettingsBase(BaseModel):
    variable_name: Optional[str] = None
    value: Optional[str] = None


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(SettingsBase):
    pass


class SettingsInDBBase(SettingsBase):
    class Config:
        from_attributes = True


class Settings(SettingsInDBBase):
    pass
