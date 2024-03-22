from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from model.src.BaseOrm import Base
from model.src.Orms import *
from model.src.Query_Builder import Query_Builder

class Database_handler:
    def __init__(self) -> None:
        self.engine = create_engine(url=settings.DATABASE_URL(), echo=True)
        self.session_factory = sessionmaker(self.engine)

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

    def insert_into_table(self, formatted_data):
        with self.session_factory() as session:
            for model in formatted_data:
                for entries in formatted_data[model]:
                    for entry in entries:
                        try:
                            session.add(entry)  # Попытка добавить каждую запись индивидуально
                            session.commit()
                        except IntegrityError as e:
                            print(f"A database integrity error occurred: {e}")
                            session.rollback() 

    def update_table(data):
        pass

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
