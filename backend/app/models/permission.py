from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Permission(Base):
    __tablename__ = "permission"
    permission_name = Column(String(255), primary_key=True, index=True)
    roles = relationship("PermissionRole", back_populates="permissions")
