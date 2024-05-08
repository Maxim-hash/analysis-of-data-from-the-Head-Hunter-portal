import json
import socket
from config import port, max_users, encoding
from controller.client_controller import client_controller
from controller.api_controller import api_controller
import asyncio
from threading import Lock

class Server:
    def __init__(self):
        self.block_size = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen(max_users)
        print(f"Server начал работу по ip: {socket.gethostbyname(socket.gethostname())}")
        self.lock = Lock()

    def mainloop(self):
        print("Сервер ожидает пользователей")
        while True:
            if not self.lock.locked():
                conn, addr = self.server.accept()

                data = conn.recv(1024).decode(encoding)
                parsed_data = json.loads(data)
                msg = ''

                print(f"{addr} send message {parsed_data}")
                msg = client_controller.handle(addr[0], parsed_data).encode(encoding)
                end_signal = b"<END>"
                conn.sendall(msg + end_signal)

        conn.close()

    def update_database(self):
        with self.lock:
            self.db = asyncio.run(api_controller.update_database())
            print("Update database done!")

