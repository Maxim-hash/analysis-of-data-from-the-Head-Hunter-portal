from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column

str_2048 = Annotated[str, 2048]
intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'schema': "hh"}
    type_annotation_map = {
        str_2048: String(2048)
    }
    pass