import psycopg2
import config
from model.src.Query_Builder import Query_Builder

class Database_handler:
    def __init__(self) -> None:
        try:
            self.connect = psycopg2.connect(dbname=config.db_name, user=config.db_name, 
                        password=config.password, host=config.host)
        except Exception as _ex:
            print("Не удалось подкючиться к Базе Данных", _ex)

    def __del__(self):
        self.connect.close()
        print("Соединение с БД было закрыто деструктором")

    def create_tables(self):
        q_builder = Query_Builder()
        with self.connect.cursor() as cursor:
            for i in config.database_tables:
                query = q_builder.create().table(i)
                for j in config.database_tables[i]:
                    pass
                cursor.execute(f"CREATE TABLE {i} ({config.database_tables[i]})")
            self.connect.commit()
            
    def select_from_table(self, table):
        pass

    def insert_into_table(self, table):
        pass

    def update_table(data):
        pass

    def drop_tables(self):
        with self.connect.cursor() as cursor:
            for i in config.database_tables:
                cursor.execute(f"DROP TABLE {i}")
