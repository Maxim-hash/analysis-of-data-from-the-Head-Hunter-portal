import datetime
from typing import Annotated
from sqlalchemy import ForeignKey
from model.src.BaseOrm import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]

class AreaOrm(Base):
    __tablename__ = "area"
    id: Mapped[intpk]
    name: Mapped[str_256]

class EmployerOrm(Base):
    __tablename__ = "employer"

    id: Mapped[intpk]
    name: Mapped[str_256]
    accredited_it_empoloyer: Mapped[bool]
    trusted: Mapped[bool]

class VacansyOrm(Base):
    __tablename__ = "vacancy"

    id: Mapped[intpk]
    name: Mapped[str_256]
    publishied_at: Mapped[datetime.datetime]
    schedule: Mapped[str_256]
    prof_roles: Mapped[str_256]
    exp: Mapped[str_256]
    empoyment: Mapped[str_256]
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id", ondelete="CASCADE"))
    employers_id: Mapped[int] = mapped_column(ForeignKey("employer.id", ondelete="CASCADE"))
    requirement: Mapped[str_256]
    responsobility: Mapped[str_256]

class SalaryOrm(Base):
    __tablename__ = "salary"

    id: Mapped[intpk] = mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"))
    s_from: Mapped[int | None] 
    s_to: Mapped[int | None] 
    currency: Mapped[str_256]
    gross: Mapped[bool]