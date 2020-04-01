from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from PIL import Image
from io import BytesIO
import random

url = "https://passport.bilibili.com/login"
browser = webdriver.Chrome(executable_path="D:\PycharmProj\PythonWebCrawlerPersonal\spider\chromedriver.exe")


def compare_pixel(image1, image2, i, j):
    pixel1 = image1.load()[i,j]
    pixel2 = image2.load()[i,j]

    threshold = 60
    if abs(pixel1[0]-pixel2[0]) < threshold and abs(pixel1[1]-pixel2[1]) < threshold and abs(pixel1[2]-pixel2[2]) < threshold:
        return True
    return False


def crop_image(image_file_name, image_div):
    location = image_div.location
    size = image_div.size
    top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size[
        "width"]
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))

    capture = screenshot.crop((int(left), int(top), int(right), int(bottom)))
    capture.save(image_file_name)
    return capture


def login():

    username = "username"
    password = "password"
    browser.get(url)
    browser.maximize_window()
    username_input = browser.find_element_by_xpath("//input[@id='login-username']")
    password_input = browser.find_element_by_xpath("//input[@id='login-passwd']")
    username_input.send_keys(username)
    password_input.send_keys(password)
    time.sleep(2)
    login_btn = browser.find_element_by_xpath("//a[@class='btn btn-login']")
    login_btn.click()
    time.sleep(2)
    # browser.execute_script('document.querySelectorAll("canvas")[3].style=""')
    browser.execute_script('document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].style=""')
    time.sleep(2)
    img = browser.find_element_by_xpath("//*[@class='geetest_canvas_fullbg geetest_fade geetest_absolute']")
    image1 = crop_image("capture1.png", img)
    browser.execute_script('document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].style="display :none;"')
    time.sleep(2)
    img_2 = browser.find_element_by_xpath("//*[@class='geetest_canvas_slice geetest_absolute']")
    image2 = crop_image("capture2.png", img_2)

    left_offset = 60
    has_find = False
    for i in range(left_offset, int(image1.size[0])):
        for j in range(int(image1.size[1])):
            if not compare_pixel(image1, image2, i, j):
                left = i
                has_find = True
                break;
        if has_find:
            break;
    left -= 6

    # 拖动图片
    # 根据偏移量获取移动轨迹
    # 一开始加速，然后减速，生长曲线，且加入点随机变动
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = left * 3 / 4
    # 间隔时间
    t = 0.1
    v = 0
    while current < left:
        if current < mid:
            a = random.randint(2, 3)
        else:
            a = - random.randint(6, 7)
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        track.append(round(move))

    slider_btn = browser.find_element_by_xpath("//div[@class='geetest_slider_button']")
    ActionChains(browser).click_and_hold(slider_btn).perform()
    for x in track:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()
    time.sleep(2)
    if_success_url = "https://www.bilibili.com/"
    browser.get(if_success_url)
    time.sleep(2)
    try:
        browser.find_element_by_xpath("//*[@class='mini-vip van-popover__reference']")
        print("login successfully")
    except Exception as e:
        print("retrying")
        login()


if __name__ == "__main__":
    login()


