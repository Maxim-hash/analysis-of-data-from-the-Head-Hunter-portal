import socket
from config import port, max_users, encoding
from controller.client_controller import client_controller
from controller.api_controller import api_controller
import asyncio

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen(max_users)
        print(f"Server начал работу по ip: {socket.gethostbyname(socket.gethostname())}")

    def mainloop(self):
        print("Сервер ожидает пользователей")
        while True:
            conn, addr = self.server.accept()

            print ('connected:', addr)

            data = conn.recv(1024).decode(encoding)
            msg = ''
            #data.decode(config.encoding)
            if not data:
                break
            else:
                print(f"{addr} send message {data}")
                msg = client_controller.handle(data)        
                conn.send(msg.encode(encoding))
        
        conn.close()

    def update_database(self):
        self.db = asyncio.run(api_controller.update_database())
        print("Update database done!")

