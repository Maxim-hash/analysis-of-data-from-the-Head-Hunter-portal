import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from structural.config import *
from creational.singleton import Singleton
from structural.src.request_builder import *
from structural.src.localstoragemanager import LocalStorageManager

class AutorizationWindow(Tk, Singleton):
    def init(self, on_success=None):
        self.on_success = on_success
        lsm = LocalStorageManager()
        users = {user[0] : user[1] for user in lsm.getUsers()}
        super().__init__() 
        self.errorLabel = ttk.Label(self)
        self.title("Панель авторизации")
        self.geometry("400x300")
        ttk.Style().configure(".",  font="helvetica 13", foreground="#004D40", padding=8) 
        ttk.Label(self, text="Login").pack(padx=5, pady=5)
        self.entry_login = ttk.Entry(self, width=40)

        users_var = Variable(value=list(users.keys()))
        listbox_users = Listbox(self, listvariable=users_var, selectmode=SINGLE, height=len(list(users.keys())))
        def handleReturn(event):
            
            def selected(event):
                # получаем индексы выделенных элементов
                self.entry_login.delete(0, END)
                self.entry_password.delete(0, END)
                selected_indices = listbox_users.curselection()
                
                self.entry_login.insert(0, listbox_users.get(selected_indices))
                self.entry_password.insert(0, users[listbox_users.get(selected_indices)])
                
                #self.entry_password.insert(0, users)
                #listbox_users.pack_forget()
            listbox_users.bind("<<ListboxSelect>>", selected)
            listbox_users.pack()

        self.entry_login.bind("<Button-1>", handleReturn)
        self.entry_login.pack(padx=5, pady=5)
        ttk.Label(self, text="Password").pack(padx=5, pady=5)
        self.entry_password = ttk.Entry(self, width=40, show="*")
        #self.entry_login.insert(0, users[0][0])
        #self.entry_password.insert(0, users[0][1])
        self.entry_password.pack(padx=5, pady=5)
        ttk.Button(self, text="Log in", command=self.login).pack(padx=5, pady=5)
        ttk.Button(self, text="Registration", command=self.auth).pack(padx=5, pady=5)

    def login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()
        builder = JSONRequestBuilder(LoginRequestTemplate(login, password))
        message = builder.build()
        self.data = authorization(message)

        if self.data["status"] == "Access":
            self.on_success(self.data["data"])
        else:
            self.errorLabel['text'] = self.data["data"]
            self.entry_password.delete(0, END)
            self.errorLabel.pack()
            
    def auth(self):
        login = self.entry_login.get()
        password = self.entry_password.get()
        builder = JSONRequestBuilder(AuthRequestTemplate(login, password))
        message = builder.build()
        self.data = authorization(message)

        if self.data["status"] == "Access":
            self.on_success()
        else:
            self.errorLabel['text'] = "Такой пользователь уже зарегистрирован"
            self.entry_login.delete(0, END)
            self.entry_password.delete(0, END)
            self.errorLabel.pack()

    def __init__(self, *args):
        pass

def authorization(message:str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host_ip, port))
        sock.send(message.encode(encoding))
        resp = sock.recv(1024)
        data = resp.decode(encoding)[:-5]
    except Exception as e:
        messagebox.showerror("Connection failed", f"{e}")
    except:
        data = "Error"
        print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
              "\nПопробуйте повторить попытку через пару минут")
    sock.close()
    return json.loads(data)