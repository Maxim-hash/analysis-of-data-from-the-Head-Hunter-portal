from typing import List, Type
from sqlalchemy.orm import Session
from model.src.Orms import VacancyOrm, AreaOrm

class FilterInterface:
    def apply(self, query):
        raise NotImplementedError
    
class QueryBuilder:
    def __init__(self, session: Session):
        self.session = session
        self.query = session.query(VacancyOrm)
        self.filters: List[FilterInterface] = []

    def add_filter(self, filter: FilterInterface):
        self.filters.append(filter)
        return self

    def build(self):
        for filter in self.filters:
            self.query = filter.apply(self.query)
        return self.query
    
class ProfessionFilter(FilterInterface):
    def __init__(self, profession: str):
        self.profession = profession

    def apply(self, query):
        if self.profession:
            return query.filter(VacancyOrm.name == self.profession)
        return query
    
class RegionFilter(FilterInterface):
    def __init__(self, session: Session, region_name: str):
            self.session = session
            self.region_name = region_name

    def apply(self, query):
        if self.region_name:
            # Получаем ID региона по его названию
            region_id = self.session.query(AreaOrm.id).filter(AreaOrm.name == self.region_name).scalar()
            if region_id is not None:
                # Получаем все подрегионы для указанного региона
                all_region_ids = self._get_all_subregions(region_id)
                # Применяем фильтр к запросу
                return query.filter(VacancyOrm.area_id.in_(all_region_ids))
        return query

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

    def apply(self, query):
        if self.experience is not None:
            return query.filter(VacancyOrm.exp == self.experience)
        return query

