from typing import Annotated

from sqlalchemy import ForeignKey

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(Base):
    __tablename__ = "user_role"
    user_id: Mapped[int] = mapped_column(ForeignKey("hh.user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("hh.role.id"), primary_key=True)

    role: Mapped["Role"] = relationship(back_populates="users")
    user: Mapped["User"] = relationship(back_populates="roles")
    