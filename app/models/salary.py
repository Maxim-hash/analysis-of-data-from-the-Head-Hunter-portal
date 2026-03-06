from app.db.base import Base, intpk, str_2048
from sqlalchemy.orm import Mapped, mapped_column

class Salary(Base):
    __tablename__ = "salary"

    id: Mapped[intpk] #= mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"))
    s_from: Mapped[int | None] 
    s_to: Mapped[int | None] 
    currency: Mapped[str_2048 | None]
    gross: Mapped[bool | None]

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