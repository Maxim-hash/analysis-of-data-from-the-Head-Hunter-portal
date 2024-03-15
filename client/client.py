from structural.mainwindow import Window
from structural.autorizationwindow import AutorizationWindow


if __name__ == "__main__":
    autorizationWindow = AutorizationWindow()
    autorizationWindow.mainloop()
    
    window = Window()
    window.title("HeadHunder client")
    window.geometry("1280x720")
    window.mainloop()
