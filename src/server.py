import requests
import socket
import config

class Server():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', config.port))
        self.socket.listen(config.max_users)
        print("Server начал работу")

    def mainloop(self):
        while True:
            conn, addr = self.socket.accept()

            print ('connected:', addr)

            data = conn.recv(1024)
            msg = data.decode("utf-8")
            if not data:
                break
            else:
                print(f"{addr} send message {msg}")
            conn.send(data.upper())

        conn.close()

def main():
    server = Server()
    server.mainloop()

if __name__ == "__main__":
    main()
