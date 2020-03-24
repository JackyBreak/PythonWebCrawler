import time
from selenium import webdriver

browser = webdriver.Chrome(executable_path="C:/Users/JackyBreak/Downloads/chromedriver_win32/chromedriver.exe")
browser.get("https://item.jd.com/100004323294.html")
print(browser.page_source)
time.sleep(30)
