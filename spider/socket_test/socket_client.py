import socket;

client = socket.socket();
client.connect(('192.168.0.13', 8000));
# server_data = client.recv(1024);
# print("server response:{}".format(server_data.decode("utf8")));
while True:
    input_data = input();
    client.send(input_data.encode("utf8"))
    server_data = client.recv(1024)
    print("server response:{}".format(server_data.decode("utf8")));
# client.close();