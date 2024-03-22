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

    name: Mapped[str_256] = mapped_column(primary_key=True)
    accredited_it_employer: Mapped[bool] 
    trusted: Mapped[bool]

class VacancyOrm(Base):
    __tablename__ = "vacancy"

    id: Mapped[intpk]
    name: Mapped[str_256]
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id", ondelete="CASCADE"))
    publishied_at: Mapped[datetime.datetime]
    requirement: Mapped[str_256]
    responsobility: Mapped[str_256]
    schedule: Mapped[str_256]
    prof_roles: Mapped[str_256]
    exp: Mapped[str_256]
    empoyment: Mapped[str_256]
    employers_name: Mapped[int] = mapped_column(ForeignKey("employer.name", ondelete="CASCADE"))
    

class SalaryOrm(Base):
    __tablename__ = "salary"

    id: Mapped[intpk] = mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"))
    s_from: Mapped[int | None] 
    s_to: Mapped[int | None] 
    currency: Mapped[str_256 | None]
    gross: Mapped[bool | None]