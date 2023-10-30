from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Role(Base):
    __tablename__ = "role"
    role_name = Column(String(255), primary_key=True, index=True)
    users = relationship("UserRole", back_populates="roles")
    permissions = relationship("PermissionRole", back_populates="roles")
