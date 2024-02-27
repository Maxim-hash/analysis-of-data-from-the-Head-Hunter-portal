from model.model import model
import config
import psycopg2
import requests

class api_model(model):
    @staticmethod
    def get_API_data():
        per_page = 100
        
        url = f"https://api.hh.ru/vacancies?per_page={per_page}"
        response = requests.get(url).json()
        quantity_pagination = round(response['found'] / per_page, 0) + 1
        data = list()
        page = 0
        while page <= quantity_pagination:
            response = requests.get(url, timeout=5).json()
            data.append(response)
            page += 1

        return data
    
    @staticmethod
    def create_tables():
        try:
            connect = psycopg2.connect(dbname=config.db_name, user=config.db_name, 
                        password=config.password, host=config.host)
            with connect.cursor as cursor:
                for i in config.database_tables:
                    cursor.execute(f"CREATE TABLE {i} ({config.database_tables[i]})")
            connect.commit()
            
        except Exception as _ex:
            print("Не удалось подкючиться к Базе Данных", _ex)
        finally:
            connect.close()

    @staticmethod
    def update_database(data):
        pass

    @staticmethod
    def drop_database():
        try:
            connect = psycopg2.connect(dbname=config.db_name, user=config.db_name, 
                        password=config.password, host=config.host)
            with connect.cursor as cursor:
                for i in config.database_tables:
                    cursor.execute(f"DROP TABLE {i}")
                    cursor.fetchone()
            connect.close()
        except:
            print("Не удалось подкючиться к Базе Данных")
            