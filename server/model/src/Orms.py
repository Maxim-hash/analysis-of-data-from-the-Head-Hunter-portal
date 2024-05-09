import datetime
from typing import Annotated
from sqlalchemy import ForeignKey
from model.src.BaseOrm import Base, str_512
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]

class ModeOrm(Base):
    __tablename__ = "mode"

    id: Mapped[intpk]
    name: Mapped[str_512]

class JournalOrm(Base):
    __tablename__ = "journal"

    id: Mapped[intpk]
    token: Mapped[str_512]
    action: Mapped[str_512]
    status: Mapped[bool]
    time: Mapped[datetime.datetime]

class UserOrm(Base):
    __tablename__ = "user"

    ip:  Mapped[str_512] 
    email: Mapped[str_512] = mapped_column(primary_key=True)
    password: Mapped[str_512]
    token: Mapped[str_512]
    mode_id: Mapped[int] = mapped_column(ForeignKey("mode.id", ondelete="CASCADE"))

class AreaOrm(Base):
    __tablename__ = "area"
    id: Mapped[intpk]
    parent_id: Mapped[int | None]
    name: Mapped[str_512]

    def __eq__(self, other):
        if not isinstance(other, AreaOrm):
            return False
        return (self.id == other.id and 
                self.parent_id == other.parent_id and 
                self.name == other.name)

    def __hash__(self):
        # Для примера можно использовать хэширование по id
        return hash(self.id)

class EmployerOrm(Base):
    __tablename__ = "employer"
    id: Mapped[intpk]
    name: Mapped[str_512]
    accredited_it_employer: Mapped[bool] 
    trusted: Mapped[bool]

    def __eq__(self, other):
        if not isinstance(other, EmployerOrm):
            return NotImplemented
        return (self.name == other.name and
                self.accredited_it_employer == other.accredited_it_employer and
                self.trusted == other.trusted)

    def __hash__(self):
        return hash((self.name, self.accredited_it_employer, self.trusted))

class VacancyOrm(Base):
    __tablename__ = "vacancy"

    id: Mapped[intpk]
    name: Mapped[str_512]
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id", ondelete="CASCADE"))
    publishied_at: Mapped[str_512]
    requirement: Mapped[str_512 | None]
    responsobility: Mapped[str_512 | None]
    schedule: Mapped[str_512]
    prof_roles: Mapped[str_512]
    exp: Mapped[str_512]
    empoyment: Mapped[str_512]
    employers_name: Mapped[str_512]

    def __eq__(self, other):
        if not isinstance(other, VacancyOrm):
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
    
class SkillOrm(Base):
    __tablename__ = "skills"

    id : Mapped[intpk]
    skill: Mapped[str_512]

class SalaryOrm(Base):
    __tablename__ = "salary"

    id: Mapped[intpk] #= mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"))
    s_from: Mapped[int | None] 
    s_to: Mapped[int | None] 
    currency: Mapped[str_512 | None]
    gross: Mapped[bool | None]

    def __eq__(self, other):
        if not isinstance(other, SalaryOrm):
            return False
        return (self.id == other.id and 
                self.s_from == other.s_from and 
                self.s_to == other.s_to and 
                self.currency == other.currency and 
                self.gross == other.gross)

    def __hash__(self):
        return hash(self.id)