import socket

http_client = socket.socket();
http_client.connect(("www.baidu.com", 80))
http_client.send("GET / HTTP/1.1\r\nConnection:close\r\n\r\n".encode("utf8"))

data = b""

while True:
    tmp = http_client.recv(1024)
    if tmp:
        data+=tmp
    else:
        break
print(data.decode("utf8"))