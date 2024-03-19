from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }
    pass