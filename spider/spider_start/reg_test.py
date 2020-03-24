import re
info = "姓名:bobby1987 生日:1987年10月1日 本科:2005年9月1日"
# print(re.findall("\d{4}",info))
match_result = re.match(".*生日.*?(\d{4}).*?本科.*?(\d{4})",info)
print(match_result.group(1))
print(match_result.group(2))

result = re.sub("\d{4}","2020",info)
print(info)
print(result)
# name = """
# my name is
# Jacky
# """
# print(re.match(".*Jacky", name, re.DOTALL).group())