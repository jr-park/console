from sqlalchemy import Column, String
from app.db.base_class import Base


class Settings(Base):
    __tablename__ = "settings"
    variable_name = Column(String(255), primary_key=True, index=True)
    value = Column(String(255))
