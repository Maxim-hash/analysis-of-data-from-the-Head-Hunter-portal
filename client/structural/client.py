from structural.mainwindow import MainWindow
from structural.autorizationwindow import AutorizationWindow

class App_Controller:
    def __init__(self) -> None:
        self.mainWindow = None
        self.autorizationWindow = AutorizationWindow(self.on_login_success)
    
    def run(self) -> None:
        self.autorizationWindow.mainloop()

    def on_login_success(self):
        self.autorizationWindow.destroy()
        self.window = MainWindow()
        self.window.title("HeadHunder client")
        self.window.geometry("1280x720")
        self.window.mainloop()
