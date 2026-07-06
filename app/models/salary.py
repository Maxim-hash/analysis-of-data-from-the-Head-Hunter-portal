from sqlalchemy import ForeignKey

from app.db.base import Base, intpk, str_2048
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Salary(Base):
    __tablename__ = "salary"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    vacancy_id : Mapped[int] = mapped_column(ForeignKey("hh.vacancy.id", ondelete="CASCADE"), nullable=False)
    s_from: Mapped[int | None] 
    s_to: Mapped[int | None] 
    currency: Mapped[str_2048 | None]
    gross: Mapped[bool | None]

    vacancy: Mapped["Vacancy"] = relationship(back_populates="salary")

    def __eq__(self, other):
        if not isinstance(other, Salary):
            return False
        return (self.id == other.id and 
                self.s_from == other.s_from and 
                self.s_to == other.s_to and 
                self.currency == other.currency and 
                self.gross == other.gross)

    def __hash__(self):
        return hash(self.id)