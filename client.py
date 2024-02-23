import socket
import config

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((config.host_ip, config.port))

    msg = "hello server"
    sock.send(msg.encode("utf-8"))

    data = sock.recv(1024)
    print(data.decode("utf-8"))
    sock.close()
except:
    print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
          "\nПопробуйте повторить попытку через пару минут")
    sock.close()
