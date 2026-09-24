from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.db.base import Base, intpk

if TYPE_CHECKING:
    from .vacancy import Vacancy


class Area(Base):
    __tablename__ = "area"
    id: Mapped[intpk]
    parent_id: Mapped[int | None]
    name: Mapped[str]

    vacancies: Mapped[list["Vacancy"]] = relationship("Vacancy", back_populates="area")

    def __eq__(self, other):
        if not isinstance(other, Area):
            return False
        return (self.id == other.id and 
                self.parent_id == other.parent_id and 
                self.name == other.name)

    def __hash__(self):
        # Для примера можно использовать хэширование по id
        return hash(self.id)