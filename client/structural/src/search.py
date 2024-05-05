import socket
from structural import config
from structural.src.request_builder import *
from structural.src.graphs import *
from structural.src.request_context import *

def search(token, vacancy_name, area, exp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((config.host_ip, config.port))
        request_builder = JSONRequestBuilder(GetRequestTemplate(token, vacancy_name, area, exp))
       
        request = request_builder.build()
        message = request.encode(config.encoding)
        sock.send(message)
        answer = b""
        end_signal = b"<END>"
        while True:
            data = sock.recv(1024)
            answer += data
            if end_signal in data:
                break
        answer = answer[:-5].decode(config.encoding)
        answer = json.loads(answer)
        
        sock.close()
        return RequestContext(answer["data"], json.loads(request))
    except Exception as error:
        print("Произошла ошибка:", error)
    except:
        print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
            "\nПопробуйте повторить попытку через пару минут")
        sock.close()
