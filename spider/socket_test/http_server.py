import socket
import threading

server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen()


def handle_sock(sock, addr):
    while True:
        tmp_data=sock.recv(1024)
        print(tmp_data.decode("utf8"));
        response_template = '''HTTP/1.1 200 OK
Content-Type: application/json

<html_test>
  <head>
    <title>Build A Web Server</title>
  </head>
  <body>
    Hello World, this is a very simple HTML document.
  </body>
</html_test>

'''
        sock.send(response_template.encode("utf8"))
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