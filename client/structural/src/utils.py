from typing import List

import numpy as np
from scipy import stats


def get_key_exp(exp_meta, exp):
    values = list(exp_meta.values())
    index = values.index(exp)

    key = list(exp_meta.keys())[index]

    return key

def prepare_data(data: List[int]):
    q1 = np.quantile(data, 0.25)  # 25% квантиль
    q3 = np.quantile(data, 0.75)  # 75% квантиль

    iqr = q3 - q1  # Межквартильный размах

    # Определение границ для отсечения выбросов
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Фильтрация выбросов
    filtered_salaries = [x for x in data if lower_bound <= x <= upper_bound]
    mean_salary = np.mean(filtered_salaries)
    median_salary = np.median(filtered_salaries)
    mode = stats.mode(filtered_salaries)

    return filtered_salaries, mean_salary, median_salary, mode