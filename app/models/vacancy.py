from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, intpk, str_2048

if TYPE_CHECKING:
    from .area import Area
    from .salary import Salary


class Vacancy(Base):
    __tablename__ = "vacancy"

    id: Mapped[intpk]
    name: Mapped[str_2048]
    area_id: Mapped[int] = mapped_column(ForeignKey("hh.area.id", ondelete="CASCADE"))
    publishied_at: Mapped[str_2048]
    requirement: Mapped[str_2048 | None]
    responsobility: Mapped[str_2048 | None]
    schedule: Mapped[str_2048]
    prof_roles: Mapped[str_2048]
    exp: Mapped[str_2048]
    empoyment: Mapped[str_2048]
    employers_name: Mapped[str_2048]

    salary: Mapped["Salary | None"] = relationship("Salary", back_populates="vacancy")
    area: Mapped["Area"] = relationship("Area", back_populates="vacancies")

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return False
        return (self.id == other.id and 
                self.name == other.name and 
                self.area_id == other.area_id and 
                self.publishied_at == other.publishied_at and 
                self.requirement == other.requirement and 
                self.responsobility == other.responsobility and 
                self.schedule == other.schedule and 
                self.prof_roles == other.prof_roles and 
                self.exp == other.exp and 
                self.empoyment == other.empoyment and 
                self.employers_name == other.employers_name)

    def __hash__(self):
        return hash(self.id)
    
