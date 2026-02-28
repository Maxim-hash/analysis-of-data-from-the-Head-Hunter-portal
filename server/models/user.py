from .base import Base, intpk
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    roles: Mapped[list["UserRole"]] = relationship(back_populates="user")