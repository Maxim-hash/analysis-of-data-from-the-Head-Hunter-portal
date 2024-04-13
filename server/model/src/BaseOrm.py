from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_512 = Annotated[str, 512]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_512: String(512)
    }
    pass