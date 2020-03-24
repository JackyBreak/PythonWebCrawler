import socket;
from collections import defaultdict
import threading
import json

online_users = defaultdict(dict);

user_msgs = defaultdict(list);

server = socket.socket();

server.bind(("0.0.0.0", 8000))
server.listen()

def handle_sock(sock, addr):
    while True:
        data = sock.recv(1024)
        json_data = json.loads(data.decode("utf8"))
        action = json_data.get("action","")
        if action == "login":
            online_users[json_data["user"]] = sock
            sock.send("login successfully".encode("utf8"))
        elif action == "list_user":
            all_users = [user for user, sock in online_users.items()]
            sock.send(json.dumps(all_users).encode("utf8"))
        elif action == "history_msg":
            sock.send(json.dumps(user_msgs.get(json_data["user"], [])).encode("utf8"))
        elif action == "send_msg":
            if json_data["to"] in online_users:
                online_users.get(json_data["to"]).send(json.dumps(json_data).encode("utf8"))
            user_msgs[json_data["to"]].append(json_data)
        elif action == "exit":
            del online_users[json_data["user"]]
            sock.send("Log off successfully!".encode("utf8"))


while True:
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()
