import pandas as pd
from structural.src.request_context import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class Graph:
    def __init__(self, request:RequestContext) -> None:
        self.data = request.data
        self.context = request.context

    def draw(self, container) -> None:
        raise NotImplementedError("Вы должны определить метод draw")
    
class BaseHistogram(Graph):
    def draw(self, container) -> None:
        df = pd.DataFrame(self.data.values(), index=self.data.keys())
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2) 
        ax.hist(df["salary"], bins=10, color="skyblue", edgecolor='black')
        salaries = [int(i) for i in df["salary"] if pd.notnull(i)]
        mean_salary = np.mean(salaries)
        median_salary = np.median(salaries)
        ax.set_xlabel("Зарплата, Рублей")
        ax.set_ylabel("Количество, Штук")
        ax.set_title(f"Распределение зарплат для вакансии: {self.context['vacancy_name']}\nСредняя зарплата: {mean_salary:.2f}, Медиана зарплаты: {median_salary:.2f}")
        ax.axvline(mean_salary, color="r", linestyle="dashed", linewidth=1)
        ax.axvline(median_salary, color="g", linestyle="dotted", linewidth=1)
        sample_size = len(df["salary"].dropna())  # Исключаем NaN значения
        # Добавление надписи на график
        #ax.text(0.95, 0.95, f'Размер выборки: {sample_size}', verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='green', fontsize=12)
        fig.text(0.5, 0.02, f'Размер выборки: {sample_size}', ha='center', va='bottom', fontsize=10)
        ax.legend(["Среднее", "Медиана"])
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack()