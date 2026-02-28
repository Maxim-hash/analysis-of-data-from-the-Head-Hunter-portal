from datetime import datetime

from .base import Base

from .base import Base, intpk
from sqlalchemy.orm import Mapped, mapped_column

class HHParserState(Base):
    __tablename__ = "hh_parse_state"
    id: Mapped[intpk]
    mode: Mapped[str]
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    page: Mapped[int]
    done: Mapped[bool] = mapped_column(default=False)