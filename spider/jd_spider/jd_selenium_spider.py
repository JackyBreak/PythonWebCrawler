from selenium import webdriver
from scrapy import Selector
import json
import time
import re
from datetime import datetime
from jd_spider.models import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("blink-settings=imagesEnabled=false")

browser = webdriver.Chrome(executable_path="C:/Users/JackyBreak/Downloads/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)#replace it with the path of chrome webdriver in your local repo


def process_value(num_str):
    """
    extract number from a string
    :param num_str: a string contains number and other characters
    :return: success: the number in the string; failure: 0
    """
    nums = 0
    re_match = re.search("(\d+)", num_str)
    if re_match:
        return int(re_match.group(1))
    else:
        return 0


def parse_good(goodid):
    browser.get("https://item.jd.com/{}.html".format(goodid))

    sel = Selector(text=browser.page_source)

    good = Good(id=goodid)
    name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract()).strip()
    price = "".join(sel.xpath("//span[@class='price J-p-{}']/text()".format(goodid)).extract()).strip()
    detail = "".join(sel.xpath("//div[@id='detail']/div[@class='tab-con']").extract()).strip()
    good_images = sel.xpath("//div[@id='spec-list']//img/@src").extract()
    supplier_info = "".join(sel.xpath("//div[@id='summary-service']").extract())
    re_match = re.search('<a href="//(.*).jd.com', supplier_info)
    if re_match:
        good.supplier = re_match.group(1)
    else:
        good.supplier = "京东"


    good.name = name
    good.price = price
    good.content = detail
    good.image_list = json.dumps(good_images)

    ggbz_btn = browser.find_element_by_xpath("//div[@id='detail']//li[contains(text(),'规格与包装')]")
    ggbz_btn.click()
    time.sleep(3)
    sel = Selector(text=browser.page_source)
    ggbz_detail = sel.xpath("//div[@id='detail']//div[@class='tab-con']/div[@style='display: block;']").extract()
    good.ggbz = ggbz_detail

    comment_btn = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
    comment_btn.click()
    time.sleep(5)
    sel = Selector(text=browser.page_source)
    tag_list = sel.xpath("//div[@class='tag-list tag-available']/span/text()").extract()
    good_rate_ratio = int(sel.xpath("//div[@class='percent-con']/text()").extract()[0])
    good.good_rate = good_rate_ratio

    summary_as = sel.xpath("//ul[@class='filter-list']/li[@data-tab='trigger']")
    for summary in summary_as:
        name = summary.xpath("./a/text()").extract()[0]
        num_str = summary.xpath("./@data-num").extract()[0]
        num = process_value(num_str)

        if name == "全部评价":
            good.comments_nums = num
        elif name == "晒图":
            good.has_image_comment_nums = num
        elif name == "视频晒单":
            good.has_video_comment_nums = num
        elif name == "追评":
            good.has_add_comment_nums = num
        elif name == "好评":
            good.well_comment_nums = num
        elif name == "中评":
            good.middle_comment_nums = num
        elif name == "差评":
            good.bad_comment_nums = num

    existed_good = Good.select().where(Good.id == good.id)
    if existed_good:
        good.save()
    else:
        good.save(force_insert=True)

    for tag in tag_list:
        re_match = re.search("(.*)\((\d+)\)", tag)
        if re_match:
            tag_name = re_match.group(1)
            nums = (re_match.group(2))

            existed_summary = GoodEvaluateSummary.select().where(GoodEvaluateSummary.good == good, GoodEvaluateSummary.tag == tag_name)
            if existed_summary:
                summary = existed_summary[0]
            else:
                summary = GoodEvaluateSummary(good=good)

            summary.tag = tag_name
            summary.num = nums
            summary.save()
    has_next_page = True
    while has_next_page:
        all_eva = sel.xpath("//div[@class='comment-item']")
        for item in all_eva:
            good_evaluate = GoodEvaluate(good=good)

            evaluate_id = item.xpath("./@data-guid").extract()[0]
            good_evaluate.id = evaluate_id
            user_head_url = "https:{}".format(item.xpath(".//div[@class='user-info']/img/@src").extract()[0])
            user_name = "".join(item.xpath(".//div[@class='user-info']/text()").extract()).strip()

            good_evaluate.user_head_url = user_head_url
            good_evaluate.user_name = user_name

            star = item.xpath("./div[@class='comment-column J-comment-column']/div[1]/@class").extract()[0]
            star = int(star[-1])
            good_evaluate.star = star
            eva_comment = "".join(item.xpath("./div[@class='comment-column J-comment-column']/p["
                                             "@class='comment-con']/text()").extract()[0]).strip()
            good_evaluate.content = eva_comment
            image_list = item.xpath("./div[@class='comment-column J-comment-column']/div[@class='pic-list "
                                    "J-pic-list']/a/img/@src").extract()
            video_list = item.xpath("./div[@class='comment-column J-comment-column']/div[@class='J-video-view-wrap "
                                    "clearfix']//video/@src").extract()
            good_evaluate.image_list = json.dumps(image_list)
            good_evaluate.video_list = json.dumps(video_list)
            comment_num = int(item.xpath(".//div[@class='comment-op']//a[3]/text()").extract()[0])
            praise_num = int(item.xpath(".//div[@class='comment-op']//a[2]/text()").extract()[0])
            good_evaluate.comment_nums = comment_num
            good_evaluate.praised_nums = praise_num
            good_info = item.xpath(".//div[@class='order-info']/span/text()").extract()
            eva_time = good_info[-1]
            good_info = good_info[:-1]
            good_info = json.dumps(good_info)
            eva_time = datetime.strptime(eva_time, "%Y-%m-%d %H:%M")
            good_evaluate.evaluate_time = eva_time
            good_evaluate.good_info = good_info

            existed_good_evaluate = GoodEvaluate.select().where(GoodEvaluate.id == good_evaluate.id)
            if existed_good_evaluate:
                good_evaluate.save()
            else:
                good_evaluate.save(force_insert=True)

        try:
            next_page_ele = browser.find_element_by_xpath("//a[@clstag='shangpin|keycount|product|pinglunfanye-nextpage']")
            next_page_ele.send_keys("\n")
            time.sleep(5)
            sel = Selector(text=browser.page_source)
        except NoSuchElementException as e:
            has_next_page = False


if __name__ == "__main__":
    parse_good(100010658548)