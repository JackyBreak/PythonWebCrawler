import socket
import threading
import json

server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen()


def handle_sock(sock, addr):
    while True:
        tmp_data=sock.recv(1024)
        print(tmp_data.decode("utf8"));
        response_template = '''HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin:http://localhost:63343

{}

'''
        data = [
            {
                "name": "django打造在线教育",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/78.html"
            },
            {
                "name": "python高级编程",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/200.html"
            },
            {
                "name": "scrapy分布式爬虫",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/92.html"
            },
            {
                "name": "django rest framework打造生鲜电商",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/131.html"
            },
            {
                "name": "tornado从入门到精通",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/290.html"
            },
        ]
        sock.send(response_template.format(json.dumps(data)).encode("utf8"))
        sock.close()
        break
while True:
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()
#     # sock.send("welcome to my server!".encode("utf8"))
#
#
#
#     # if tmp_data:
#     #     data += tmp_data.decode("utf8")
#     #     if tmp_data.decode("utf8").endswith("#"):
#     #         break;
#     # else:
#     #     break;
# print(data)
# server.close()