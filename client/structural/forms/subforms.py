from collections import Counter
from tkinter import LEFT, NE, NW, W, Canvas, Frame, Label, Scrollbar
from tkinter import ttk
from tkinter.ttk import Treeview

import uuid
import json
import pandas as pd

from structural.src.graphs import BaseHistogram, DataTransmitter, pieGramm
from structural.src.tree import ExperienceTree, EmployerTree
from structural.src.request_context import RequestContext
from structural.src.utils import prepare_data

class SubForms(Frame):
    def __init__(self, master, data, callback):
        super().__init__(master=master)
        self.canvas = Canvas(self, borderwidth=0, background='white')
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas,background='white')

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Configure>", self.on_resize)
        self.scrollable_frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(canvas))

        self.count_vacancy = Label(self.scrollable_frame, text='')
        self.close_button = ttk.Button(self.scrollable_frame, text='Закрыть', command=lambda: self.close_tab(self, callback))
        self.download_raw_data_button = ttk.Button(self.scrollable_frame, text="Выгрузить данные", command= lambda : self.download_raw_data(data))
        self.close_button.pack(anchor=NE)
        self.download_raw_data_button.pack(anchor=NE)
    
        self.show_stat(data)

    def on_resize(self, event):
        self.canvas.itemconfig(self.scrollable_frame_id, width=self.canvas.winfo_width())

    def download_raw_data(self, data: RequestContext):
        filename = f"{uuid.uuid4()}.json"

        with open(filename, "w", encoding='utf-8') as json_file:
            json.dump(data.data, json_file, ensure_ascii=False, indent=4)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def close_tab(self, tab, callback):
        # Закрытие указанной вкладки
        index = self.master.index(tab)
        self.master.forget(index)
        callback(index)

    def show_stat(self, request:RequestContext):
        data = DataTransmitter(request.data)
        base_histogram1 = BaseHistogram(request)
        base_histogram1.draw(self.scrollable_frame)
        uniq_exp = data.getUniqExp()
        unic_emp = data.getUniqEmployer()
        tree = ExperienceTree(self.scrollable_frame)

        # Добавление данных в таблицу
        for i in uniq_exp:
            filtered_by_exp_dataframe = data.filterDataByExp(i)
            salaries = [int(j) for j in filtered_by_exp_dataframe["salary"] if pd.notnull(j)]

            if not salaries:
                continue
            result = prepare_data(salaries)
 
            tree_data = [i, result[1],result[2], result[3].mode, len(result[0])]
            tree.insert("", "end", values=tree_data)

        tree.pack(expand=True, fill="both")
        key_skills_frame = Frame(self.scrollable_frame)
        key_skills_frame.pack()
        texts = data.get_dataframe()["key_skills"].dropna().tolist()
        temp = [i for item in texts for i in item]
        key_skills_tree = Treeview(key_skills_frame, columns=("Ключевой навык", "Кол-во"), show="headings")
        key_skills_tree.heading("Ключевой навык", text="Ключевой навык")
        key_skills_tree.heading("Кол-во", text="Кол-во")

        # Установка ширины столбцов
        key_skills_tree.column("Ключевой навык", width=100)
        key_skills_tree.column("Кол-во", width=100)
        key_skill_data = Counter(temp).most_common(100)

        for i in key_skill_data:
            key_skills_tree.insert("", "end", values=i)
        key_skills_tree.pack(expand=True, fill="both", side=LEFT)
        pie_gramm = pieGramm(request)
        pie_gramm.draw(key_skills_frame, key_skill_data)

        emp_tree = EmployerTree(self.scrollable_frame)

        # Добавление данных в таблицу
        for i in unic_emp:
            filtered_by_emp_dataframe = data.filterDataByEmp(i)
            salaries = [int(j) for j in filtered_by_emp_dataframe["salary"] if pd.notnull(j)]

            if not salaries:
                continue
            result = prepare_data(salaries)

            tree_data = [i, result[1],result[2], result[3].mode, len(result[0])]
            emp_tree.insert("", "end", values=tree_data)

        emp_tree.pack(anchor=W,expand=True, fill="both")

    def _update_result_labels(self, result:dict):
        if self.result_labels != []:
            for i in self.result_labels:
                i["text"] = ''
                i.destroy()
            self.result_labels = []
        self.count_vacancy["text"] = f"Количество вакансий: {len(result)}"
        self.count_vacancy.pack(anchor=NW)
        self.result_labels.extend(list(map(lambda x: Label(self, text=x).pack(), result.values())))