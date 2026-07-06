from sqlalchemy import ForeignKey

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class RolePermission(Base):
    __tablename__ = "role_permission"
    permission_id: Mapped[int] = mapped_column(ForeignKey("hh.permission.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("hh.role.id"), primary_key=True)
    