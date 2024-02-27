import socket
import config


try:
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect((config.host_ip, config.port))
        msg = input()
        if(msg == "exit"):
            sock.send("".encode(config.encoding))
            break
        sock.send(msg.encode(config.encoding))

        data = sock.recv(1024)
        print(data.decode(config.encoding))
        sock.close()
except:
    print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
          "\nПопробуйте повторить попытку через пару минут")
finally:
    sock.close()
