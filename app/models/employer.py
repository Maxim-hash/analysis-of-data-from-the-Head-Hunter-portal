from app.db.base import Base, intpk, str_2048
from sqlalchemy.orm import Mapped, mapped_column

class Employer(Base):
    __tablename__ = "employer"
    id: Mapped[int]
    name: Mapped[str] = mapped_column(primary_key=True)
    accredited_it_employer: Mapped[bool] 
    trusted: Mapped[bool]

    def __eq__(self, other):
        if not isinstance(other, Employer):
            return NotImplemented
        return (self.name == other.name and
                self.accredited_it_employer == other.accredited_it_employer and
                self.trusted == other.trusted)

    def __hash__(self):
        return hash((self.name, self.accredited_it_employer, self.trusted))