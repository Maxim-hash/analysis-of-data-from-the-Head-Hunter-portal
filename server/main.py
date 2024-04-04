from App_controller import Server

if __name__ == "__main__":
    server = Server()
    command = input()
    while command == 'r':
        server.update_database()
        command = input()
    else:
        server.mainloop() 