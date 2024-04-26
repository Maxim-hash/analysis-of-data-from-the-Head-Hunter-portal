from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_512 = Annotated[str, 2048]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_512: String(2048)
    }
    pass