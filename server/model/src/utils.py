from typing import List
from model.src.Orms import SalaryOrm


class СurrencyConverter:
    def __init__(self) -> None:
        self.exchange = {
            "AZN" : 0.0186,
            "BYR" : 0.0356,
            "EUR" : 0.0102,
            "GEL" : 0.0291,
            "KGS" : 0.968,
            "KZT" : 4.82,
            "RUR" : 1,
            "UAH" : 0.431,
            "USD" : 0.0109,
            "UZS" : 136.87,
        }
        
    def convert(self, sal : int, cur : str):
        return int(sal / self.exchange[cur])

def get_salary(salary_ORM_list: List[SalaryOrm]):
    result = []
    conveter = СurrencyConverter()
    for i in salary_ORM_list:
        if i.s_from == None:
            result.append({"salary" : None})
            continue
        if i.s_to == None:
            result.append({"salary" : i.s_from})
            continue
        sum = conveter.convert((i.s_from + i.s_to) / 2, i.currency)
        result.append({"salary" : sum})

    return result