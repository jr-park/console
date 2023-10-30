from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base


## FK On Delete
# user_group = Table(
#     "user_group",
#     Base.metadata,
#     Column("user_group_id", Integer, primary_key=True),
#     Column("user_id", Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False),
#     Column("group_id", Integer, ForeignKey("group.group_id", ondelete="CASCADE"), nullable=False),
# )


class PermissionRole(Base):
    __tablename__ = "permission_role"
    __table_args__ = (UniqueConstraint('permission_name', 'role_name', name='idx_permission_role'),)
    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(255), ForeignKey("permission.permission_name"), nullable=False)
    role_name = Column(String(255), ForeignKey("role.role_name"), nullable=False)
    permissions = relationship("Permission", back_populates="roles")
    roles = relationship("Role", back_populates="permissions")


class UserRole(Base):
    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint('username', 'role_name', name='idx_user_role'),)
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), ForeignKey("user.username"), nullable=False)
    role_name = Column(String(255), ForeignKey("role.role_name"), nullable=False)
    users = relationship("User", back_populates="roles")
    roles = relationship("Role", back_populates="users")
