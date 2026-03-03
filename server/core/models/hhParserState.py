from datetime import datetime

from pydantic import Field

from .base import Base

from .base import Base, intpk
from sqlalchemy.orm import Mapped, mapped_column

class HHParserState(Base):
    __tablename__ = "hh_parse_state"
    id: Mapped[intpk]
    mode: Mapped[str] = mapped_column(default="/vacancies")
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    per_page: Mapped[int]
    page: Mapped[int]
    done: Mapped[bool] = mapped_column(default=False)