from sqlalchemy import create_engine, text
from config import settings
from model.src.BaseOrm import Base
from model.src.Orms import *
from model.src.Query_Builder import Query_Builder

class Database_handler:
    def __init__(self) -> None:
        self.engine = create_engine(url=settings.DATABASE_URL(), echo=True)

    def execute(self, string, commit = False):
        with self.engine.connect() as conn:
            res = conn.execute(text(string))
            if commit:
                conn.commit()
        return res

    def create_tables(self):
        Base.metadata.create_all(self.engine)
            
    def select_from_table(self, table):
        pass

    def insert_into_table(self, table):
        pass

    def update_table(data):
        pass

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
