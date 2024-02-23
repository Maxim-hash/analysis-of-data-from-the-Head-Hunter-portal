import socket
import config

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((config.host_ip, config.port))

    msg = "hello server"
    sock.send(msg.encode(config.encoding))

    data = sock.recv(1024)
    print(data.decode(config.encoding))
    sock.close()
except:
    print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
          "\nПопробуйте повторить попытку через пару минут")
    sock.close()
