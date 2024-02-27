from controller.client_controller import client_controller
from controller.api_controller import api_controller
import socket
import config

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), config.port))
        self.server.listen(config.max_users)
        print(f"Server начал работу по ip: {socket.gethostbyname(socket.gethostname())}")

    def mainloop(self):
        print("Сервер ожидает пользователей")
        while True:
            conn, addr = self.server.accept()

            print ('connected:', addr)

            data = conn.recv(1024)
            msg = data.decode(config.encoding)
            if not data:
                break
            else:
                print(f"{addr} send message {msg}")
                msg = client_controller.handle(msg)        
                conn.send(msg.encode(config.encoding))
        
        conn.close()

    def update_database(self):
        self.db = api_controller.update_database()
        print("Update database done!")

def main():
    server = Server()
    command = input()
    while command == 'r':
        server.update_database()
        command = input()
    else:
        server.mainloop()

if __name__ == "__main__":
    main()
