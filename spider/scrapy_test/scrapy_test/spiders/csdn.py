# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
from datetime import datetime
import re

from spider.csdn_spider.spider import strip_list
from spider.scrapy_test.scrapy_test.spiders.models import *
from spider.scrapy_test.scrapy_test.items import *

class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://bbs.csdn.net/forums/ios']
    domain = "https://bbs.csdn.net/forums"

    def parse(self, response):
        topic_item = TopicItem()
        all_trs = response.xpath("//table[@class='forums_tab_table']//tr")
        all_trs = all_trs[2:]
        topic_id = 0
        for tr in all_trs:
            if tr and not tr.xpath(".//td[3]/span[1]"):
                if tr.xpath(".//td[1]/span/text()").extract():
                    status = tr.xpath(".//td[1]/span/text()").extract()[0]
                    topic_item["status"] = status
                if tr.xpath(".//td[2]/em/text()").extract():
                    score = tr.xpath(".//td[2]/em/text()").extract()[0]
                    topic_item["score"] = int(score)
                if tr.xpath(".//td[3]/a/@href").extract():
                    topic_url = parse.urljoin(self.domain, tr.xpath(".//td[3]/a/@href").extract()[0])
                    topic_id = int(topic_url.split("/")[-1])
                    topic_item["id"] = topic_id
                if tr.xpath(".//td[3]//a/text()").extract():
                    topic_title = tr.xpath(".//td[3]//a/text()").extract()[0]
                    topic_item["title"] = topic_title
                if tr.xpath(".//td[4]//a/@href").extract():
                    author_url = parse.urljoin(self.domain, tr.xpath(".//td[4]//a/@href").extract()[0])
                    author_id = author_url.split("/")[-1]
                    topic_item["author"] = author_id
                if tr.xpath(".//td[4]//em/text()").extract():
                    create_time = datetime.strptime(tr.xpath(".//td[4]//em/text()").extract()[0], "%Y-%m-%d %H:%M")
                    topic_item["create_time"] = create_time
                if tr.xpath(".//td[5]//span/text()").extract():
                    answer_info = tr.xpath(".//td[5]//span/text()").extract()[0]
                    answer_nums = answer_info.split("/")[0]
                    click_nums = answer_info.split("/")[1]
                    topic_item["answer_nums"]= int(answer_nums)
                    topic_item["click_nums"] = int(click_nums)
                if tr.xpath(".//td[6]//em/text()").extract():
                    last_reply_time = tr.xpath(".//td[6]//em/text()").extract()[0]
                    last_time = datetime.strptime(last_reply_time, "%Y-%m-%d %H:%M")
                    topic_item["last_answer_time"] = last_time
                topic_item["content"] = ""
            # existed_topics = Topic.select().where(Topic.id == topic_id)
            # if not tr.xpath(".//td[3]/span[1]"):
            #     if existed_topics:
            #         topic_item.save()
            #     else:
            #         topic_item.save(force_insert=True)
                yield topic_item
                yield scrapy.http.Request(url=topic_url, callback=self.parse_topic)

                yield scrapy.http.Request(url=author_url, callback=self.parse_author)

        next_page = response.xpath("//a[@class='pageliststy next_page']/@href").extract()
        next_page_text = response.xpath("//a[@class='pageliststy next_page']/text()").extract()
        if next_page:
            next_page_url = next_page[-1]
            next_page_text = next_page_text[-1]
            if next_page_text == "下一页":
                next_url = parse.urljoin(self.domain, next_page_url)
                yield scrapy.http.Request(url=next_url, callback=self.parse)

    def parse_topic(self, response):
        topic_url = response.url
        topic_id = topic_url.split("/")[-1]
        all_divs = response.xpath("//div[starts-with(@id, 'post-')]")
        topic_item = all_divs[0]
        content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
        praised_nums = topic_item.xpath(".//label[@class='red_praise digg']//em[1]/text()").extract()[0]
        jtl_str = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
        jtl_int = re.search("(\d+)", jtl_str)
        jtl = 0
        if jtl_int:
            jtl = int(jtl_int.group(1))
        existed_topics = Topic.select().where(Topic.id == topic_id)
        if existed_topics:
            topic_chart = existed_topics[0]
            topic_chart.content = content
            topic_chart.praised_nums = praised_nums
            topic_chart.jtl = jtl
            topic_chart.save()
        for answer_item in all_divs[1:]:
            answer = Answer()
            answer.topic_id = int(topic_id)
            author_id = answer_item.xpath(".//div[@class='nick_name']/a[1]/@href").extract()[0].split("/")[-1]
            answer.author = author_id
            create_time = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
            create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
            answer.create_time = create_time
            answer_praised_nums = int(
                answer_item.xpath(".//label[@class='red_praise digg']//em[1]/text()").extract()[0])
            answer.praised_nums = answer_praised_nums
            answer_content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
            answer.content = answer_content

            answer_id = answer_item.xpath("./@id").extract()[0].split("-")[-1]
            answer.answer_id = int(answer_id)
            existed_answer = Answer.select().where(Answer.answer_id == answer_id)
            if existed_answer:
                answer.save()
            else:
                answer.save(force_insert=True)

        next_page = response.xpath("//a[@class='pageliststy next_page']/@href").extract()
        next_page_text = response.xpath("//a[@class='pageliststy next_page']/text()").extract()
        if next_page:
            next_page_url = next_page[-1]
            next_page_text = next_page_text[-1]
            if next_page_text == "下一页":
                next_url = parse.urljoin(self.domain, next_page_url)
                yield scrapy.http.Request(url=next_url, callback=self.parse_topic)


    def parse_author(self, response):  # 获取用户详情
        author_chart = Author()
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        # }
        author_url = response.url
        # res_text = requests.get(author_url, headers=headers).text
        # response = Selector(text=res_text)
        author_id = author_url.split("/")[-1]
        author_chart.id = author_id
        if response.xpath("//p[@class='lt_title']/text()").extract():
            author_name = response.xpath("//p[@class='lt_title']/text()").extract()
            author_name = strip_list(author_name)
            author_chart.name = author_name
        if response.xpath("//p[@class='lt_title']//span[1]/text()").extract():
            author_year = response.xpath("//p[@class='lt_title']//span[1]/text()").extract()
            author_year = strip_list(author_year)
            author_chart.years = int(author_year)
        if response.xpath("//p[@class='description_detail']/text()").extract():
            author_description = response.xpath("//p[@class='description_detail']/text()").extract()[0]
            author_chart.description = author_description.strip()
        detail_info = response.xpath("//ul[@class='me_chanel_list clearfix']")
        if detail_info.xpath(".//li[1]//label[1]/span[@class='count']/text()").extract():
            blog_nums = detail_info.xpath(".//li[1]//label[1]/span[@class='count']/text()").extract()[0]
            blog_nums = int(blog_nums)
            author_chart.blog_nums = int(blog_nums)
        if detail_info.xpath(".//li[2]//label[1]/span[@class='count']/text()").extract():
            resource_nums = detail_info.xpath(".//li[2]//label[1]/span[@class='count']/text()").extract()[0]
            resource_nums = int(resource_nums)
            author_chart.resource_nums = int(resource_nums)
        if detail_info.xpath(".//li[3]//label[1]/span[@class='count']/text()").extract():
            bbs_nums = detail_info.xpath(".//li[3]//label[1]/span[@class='count']/text()").extract()[0]
            bbs_nums = int(bbs_nums)
            author_chart.forum_nums = bbs_nums
        if detail_info.xpath(".//li[4]//label[1]/span[@class='count']/text()").extract():
            blink_nums = detail_info.xpath(".//li[4]//label[1]/span[@class='count']/text()").extract()[0]
            author_chart.blink_nums = int(blink_nums)
        if detail_info.xpath(".//li[7]//label[1]/span[@class='count']/text()").extract():
            col_nums = detail_info.xpath(".//li[7]//label[1]/span[@class='count']/text()").extract()[0]
            col_nums = int(col_nums)
            author_chart.column_nums = col_nums
        if response.xpath("//div[@class='fans']/a[1]/span[1]/text()").extract():
            fans_nums = response.xpath("//div[@class='fans']/a[1]/span[1]/text()").extract()
            fans_nums = strip_list(fans_nums)
            author_chart.follower_nums = fans_nums.strip()
        if response.xpath("//div[@class='att']/a[1]/span[1]/text()").extract():
            following_nums = response.xpath("//div[@class='att']/a[1]/span[1]/text()").extract()
            following_nums = strip_list(following_nums)
            author_chart.following_nums = following_nums.strip()
        existed_author = Author.select().where(Author.id == author_id)
        if existed_author:
            author_chart.save()
        else:
            author_chart.save(force_insert=True)

