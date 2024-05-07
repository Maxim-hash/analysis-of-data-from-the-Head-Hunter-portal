from typing import List, Type
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from model.src.Orms import VacancyOrm, AreaOrm, SalaryOrm, Base, JournalOrm, UserOrm

class FilterInterface:
    def apply(self) -> None:
        raise NotImplementedError
    
    def should_use_or_operator(self) -> bool:
        return False
    
class DBQueryBuilder:
    def __init__(self, session: Session, mode):
        self.session = session
        self.mode = mode
        self.query = session.query(mode)
        self.filters: List[FilterInterface] = []

    def add_filter(self, filter: FilterInterface):
        self.filters.append(filter)
        return self

    def build(self):
        or_filters = []
        and_filters = []
        
        for filter in self.filters:
            if filter.should_use_or_operator():
                or_filters.append(filter.apply())
            else:
                and_filters.append(filter.apply())

        or_filters = [item for item in or_filters if item is not None]
        and_filters = [item for item in and_filters if item is not None]

        if or_filters:
            or_filter = or_(*or_filters)
            if and_filters:
                and_filter = and_(*and_filters)
                self.query = self.query.filter(and_(or_filter, and_filter))
            else:
                self.query = self.query.filter(or_filter)
        elif and_filters:
            self.query = self.query.filter(and_(*and_filters))

        return self.query
    
class ProfessionNameFilter(FilterInterface):
    def __init__(self, profession: str):
        self.profession = profession

    def apply(self):
        if self.profession:
            return VacancyOrm.name.like(f"%{self.profession}%")
        return None
    
    def should_use_or_operator(self) -> bool:
        return True
    
class LoginFilter(FilterInterface):
    def __init__(self, login : str) -> None:
        self.login = login

    def apply(self) -> None:
        if self.login:
            return JournalOrm.token.like(self.login)
        return None
    
class RequirementFilter(FilterInterface):
    def __init__(self, requirement) -> None:
        self.requirement = requirement

    def apply(self):
        if self.requirement:
            requirement = self.requirement.split()
            filters = [VacancyOrm.requirement.like(f"%{filter}%") for filter in requirement]
            return or_(*filters)
        return None
    
    def should_use_or_operator(self) -> bool:
        return True
    
class ProffessionRoleFilter(FilterInterface):
    def __init__(self, requirement) -> None:
        self.prof_role = requirement

    def apply(self):
        if self.prof_role:
            prof_roles = self.prof_role.split()
            filters = [VacancyOrm.prof_roles.like(f"%{filter}%") for filter in prof_roles]
            return or_(*filters)
        return None
    
    def should_use_or_operator(self) -> bool:
        return True
    
class RegionFilter(FilterInterface):
    def __init__(self, session: Session, region_name: str):
            self.session = session
            self.region_name = region_name

    def apply(self):
        if self.region_name:
            # Получаем ID региона по его названию
            region_id = self.session.query(AreaOrm.id).filter(AreaOrm.name == self.region_name).scalar()
            if region_id is not None:
                # Получаем все подрегионы для указанного региона
                all_region_ids = self._get_all_subregions(region_id)
                # Применяем фильтр к запросу
                return VacancyOrm.area_id.in_(all_region_ids)
        return None

    def _get_all_subregions(self, parent_id):
        """Рекурсивный поиск всех подрегионов для указанного региона"""
        all_region_ids = [parent_id]
        subregions = self.session.query(AreaOrm.id).filter(AreaOrm.parent_id == parent_id).all()
        for subregion_id, in subregions:
            all_region_ids.extend(self._get_all_subregions(subregion_id))
        return all_region_ids

class ExperienceFilter(FilterInterface):
    def __init__(self, experience: int):
        self.experience = experience

    def apply(self):
        if self.experience:
            return VacancyOrm.exp.like(f"%{self.experience}%")
        return None
    
class ModeFilter(FilterInterface):
    def __init__(self, mode_id: int):
        self.mode_id = mode_id

    def apply(self):
        if self.mode_id:
            return UserOrm.mode_id == self.mode_id
        return None
    
class IdFilter(FilterInterface):
    def __init__(self, id: int, orm: Base):
        self.id = id
        self.orm = orm

    def apply(self):
        if self.id is not None:
            return self.orm.id == self.id
        return None

