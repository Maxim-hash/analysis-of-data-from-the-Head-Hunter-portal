from sqlalchemy import ForeignKey

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class RolePermission(Base):
    __tablename__ = "role_permission"
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"), primary_key=True)