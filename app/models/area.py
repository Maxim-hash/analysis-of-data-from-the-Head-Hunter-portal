from app.db.base import Base, intpk
from sqlalchemy.orm import Mapped

class Area(Base):
    __tablename__ = "area"
    id: Mapped[intpk]
    parent_id: Mapped[int | None]
    name: Mapped[str]

    def __eq__(self, other):
        if not isinstance(other, Area):
            return False
        return (self.id == other.id and 
                self.parent_id == other.parent_id and 
                self.name == other.name)

    def __hash__(self):
        # Для примера можно использовать хэширование по id
        return hash(self.id)