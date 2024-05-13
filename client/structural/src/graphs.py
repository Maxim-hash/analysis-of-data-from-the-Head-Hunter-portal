import pandas as pd
from structural.src.request_context import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class DataTransmitter:
    def __init__(self, data: dict):
        self.dp = pd.DataFrame(data.values(), index=data.keys())

    def get_dataframe(self):
        return self.dp

    def getUniqExp(self):
        return self.dp['exp'].unique()
    
    def getUniqEmployer(self):
        return self.dp["employers_name"].unique()
    
    def filterDataByEmp(self, filter):
        return self.dp[self.dp["employers_name"] == filter]
    
    def filterDataByExp(self, filter):
        return self.dp[self.dp['exp'] == filter]

class Graph:
    def __init__(self, request:RequestContext) -> None:
        self.data = request.data
        self.context = request.context
        self.dp = pd.DataFrame(self.data.values(), index=self.data.keys())

    def draw(self, container) -> None:
        raise NotImplementedError("Вы должны определить метод draw")
    
    def set_data_frame(self, dataframe: pd.DataFrame) -> None:
        self.dp = dataframe
    
class BaseHistogram(Graph):
    def draw(self, container) -> None:
        salaries = [int(i) for i in self.dp["salary"] if pd.notnull(i)] 
        if len(salaries) <= 1:
            return None
        q1 = np.quantile(salaries, 0.25)  # 25% квантиль
        q3 = np.quantile(salaries, 0.75)  # 75% квантиль

        iqr = q3 - q1  # Межквартильный размах
        # Определение границ для отсечения выбросов

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        # Фильтрация выбросов
        filtered_salaries = [x for x in salaries if lower_bound <= x <= upper_bound]

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(bottom=0.2) 
        ax.hist(filtered_salaries, bins=15, color="skyblue", edgecolor='black')
        
        mean_salary = np.mean(filtered_salaries)
        median_salary = np.median(filtered_salaries)
        
        ax.set_xlabel("Зарплата, Рублей")
        ax.set_ylabel("Количество, Штук")
        ax.set_title(f"Распределение зарплат для вакансии: {self.context['vacancy_name']}\nСредняя зарплата: {mean_salary:.2f}, Медиана зарплаты: {median_salary:.2f}")
        ax.axvline(mean_salary, color="r", linestyle="dashed", linewidth=1)
        ax.axvline(median_salary, color="g", linestyle="dotted", linewidth=1)
        sample_size = len(filtered_salaries)  # Исключаем NaN значения
 
        fig.text(0.5, 0.02, f'Размер выборки: {sample_size}', ha='center', va='bottom', fontsize=10)
        ax.legend(["Среднее", "Медиана"])
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


class pieGramm(Graph):
    def draw(self, container, data):
        labels = [i[0] for i in data[:20]]
        count = [i[1] for i in data[:20]]
   
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(bottom=0.2) 

        ax.pie(count, autopct='%1.1f%%', startangle=90)
        ax.legend(labels, title="Ключевые навыки", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()

        canvas.get_tk_widget().pack(side="right")
        

class SalaryByExperienceHistograms(Graph):
    def draw(self, container):
        df = pd.DataFrame(self.data.values(), index=self.data.keys())
        pass