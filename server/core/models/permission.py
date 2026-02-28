from typing import Annotated

from .base import Base, intpk, str_2048
from sqlalchemy.orm import Mapped, mapped_column

class Permission(Base):
    __tablename__ = "permission"
    id: Mapped[intpk]
    name: Mapped[Annotated[str, 30]] = mapped_column(unique=True)
    description: Mapped[str_2048 | None]