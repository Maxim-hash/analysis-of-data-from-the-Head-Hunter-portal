from controller.controller import controller
from model.api_model import API_Model

class api_controller(controller):
    @staticmethod
    async def update_database():
        api_model = API_Model()
        await api_model.refresh_tables()
        formatted_data = await api_model.get_API_data("area")
        await api_model.load_data_into_tables(formatted_data)
        formatted_data = await api_model.get_API_data("vacancy")
        #for i in formatted_data["vacancyModel"]:
        #    all_skills = ""
        #    dictionarys = await api_model.get_skill(i.id)
        #    if dictionarys != None:
        #        obj = [value for dictionary in dictionarys for value in dictionary.values()]
        #        all_skills = ".".join(obj)
        #    else:
        #        continue
        #    if all_skills != "":
        #        await api_model.load_skills(i.id, all_skills)
        await api_model.load_data_into_tables(formatted_data)
        

        return 0
