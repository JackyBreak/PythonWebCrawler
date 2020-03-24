import socket;
import json;
import threading;

client = socket.socket();
client.connect(('192.168.0.13', 8000));

user = "jacky2"

login_template = {
    "action":"login",
    "user":user
}

client.send(json.dumps(login_template).encode("utf8"))
res = client.recv(1024)
print(res.decode("utf8"))

get_user_template = {
    "action":"list_user"
}
client.send(json.dumps(get_user_template).encode("utf8"))
res = client.recv(1024)
print("current online users are:{}".format(res.decode("utf8")))

offline_msg_template = {
    "action":"history_msg",
    "user":user
}

client.send(json.dumps(offline_msg_template).encode("utf8"))
res = client.recv(1024)
print("history messages are:{}".format(res.decode("utf8")))

exit = False


def handle_receive():
    while True:
        if not exit:
            try:
                res = client.recv(1024)
            except:
                break
            res = res.decode("utf8")
            try:
                res_json = json.loads(res)
                msg = res_json["data"]
                from_user = res_json["from"]
                print("")
                print("receive message from {}:{}".format(from_user,msg))
            except:
                print("")
                print(res)
        else:
            break

def handle_send():
    while True:
        user_input = input("please input your operation: 1. send messages 2. log off 3. get current online users")
        if user_input not in ["1","2","3"]:
            print("operation not recognized")
            user_input = input("please input your operation: 1. send messages 2. log off 3. get current online users")
        elif user_input == "1":
            to_user = input("Please enter the user you want to send to:")
            msg = input("Please enter your message")
            send_data_template = {
                "action":"send_msg",
                "to": to_user,
                "from": user,
                "data": msg
            }
            client.send(json.dumps(send_data_template).encode("utf8"))

        elif user_input == "2":
            exit_template = {
                "action": "exit",
                "user":user
            }
            client.send(json.dumps(exit_template).encode("utf8"))
            exit = True
            client.close()
            break

        elif user_input == "3":
            get_user_template = {
                "action" : "list_user"
            }
            client.send(json.dumps(get_user_template).encode("utf8"))


if __name__ == "__main__":
    send_thread = threading.Thread(target = handle_send)
    receive_thread = threading.Thread(target = handle_receive)
    send_thread.start()
    receive_thread.start()