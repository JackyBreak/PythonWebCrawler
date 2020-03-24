import requests;

url = "http://127.0.0.1:8000"
params = {
    "username":"jacky",
    "password":"abcd1234"
}
# res = requests.get(url, params = params)
# print(res)
# res = requests.post("https://www.baidu.com")
# print(res.status_code)
# my_headers = {
#     "user-agent":"request",
#     "imooc_uid":"321"
# }
res = requests.get("https://www.baidu.com")
print(res.headers)