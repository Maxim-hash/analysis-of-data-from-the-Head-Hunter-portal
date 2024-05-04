import pandas as pd
from structural.src.request_context import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class DataTransmitter:
    def __init__(self, data: dict):
        self.dp = pd.DataFrame(data.values(), index=data.keys())

    def getUniqMeta(self):
        #self.uniq_vacancy_name = self.dp["vacancy_name"].unique()
        self.uniq_area = self.dp["area_id"].unique()
        self.uniq_exp = self.dp['exp'].unique()
        return self.uniq_exp
    
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
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(bottom=0.2) 
        ax.hist(self.dp["salary"], bins=15, color="skyblue", edgecolor='black')
        salaries = [int(i) for i in self.dp["salary"] if pd.notnull(i)]
        mean_salary = np.mean(salaries)
        median_salary = np.median(salaries)
        ax.set_xlabel("Зарплата, Рублей")
        ax.set_ylabel("Количество, Штук")
        ax.set_title(f"Распределение зарплат для вакансии: {self.context['vacancy_name']}\nСредняя зарплата: {mean_salary:.2f}, Медиана зарплаты: {median_salary:.2f}")
        ax.axvline(mean_salary, color="r", linestyle="dashed", linewidth=1)
        ax.axvline(median_salary, color="g", linestyle="dotted", linewidth=1)
        sample_size = len(self.dp["salary"].dropna())  # Исключаем NaN значения
 
        fig.text(0.5, 0.02, f'Размер выборки: {sample_size}', ha='center', va='bottom', fontsize=10)
        ax.legend(["Среднее", "Медиана"])
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


class SalaryByExperienceHistograms(Graph):
    def draw(self, container):
        df = pd.DataFrame(self.data.values(), index=self.data.keys())
        pass