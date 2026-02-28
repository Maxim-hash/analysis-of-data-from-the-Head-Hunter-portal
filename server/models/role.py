from typing import Annotated

from .base import Base, intpk, str_2048
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Role(Base):
    __tablename__ = "role"
    id: Mapped[intpk]
    name: Mapped[Annotated[str, 30]] = mapped_column(unique=True)

    users: Mapped[list["UserRole"]] = relationship(back_populates="role")