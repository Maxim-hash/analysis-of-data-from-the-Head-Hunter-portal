from controller.client_controller import client_controller
import socket
import config

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), config.port))
        self.server.listen(config.max_users)
        print(f"Server начал работу по ip: {socket.gethostbyname(socket.gethostname())}")

    def mainloop(self):
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

def main():
    server = Server()
    server.mainloop()

if __name__ == "__main__":
    main()
