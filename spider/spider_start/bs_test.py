from bs4 import BeautifulSoup
import re
html = """
<!DOCTYPE html_test>
<html_test lang="en">
<head>
    <meta charset="UTF-8">
    <title>bobby基本信息</title>
    <script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
    <!--<script>-->
        <!--$(document).ready(function () {-->
            <!--console.log($("#info")[0].nodeName)-->
            <!--// console.log($("#info").text())-->
            <!--// console.log($("#info").html_test())-->
            <!--// console.log($(".teacher_info").html_test())-->
            <!--// console.log($("#info").children().first().text())-->
            <!--// console.log($(".name").siblings().first().text())-->
            <!--$(".name").addClass("bobby")-->
            <!--console.log($(".name").attr("class"))-->
            <!--$(".age").attr("data", "30")-->
            <!--$(".age").remove()-->
        <!--})-->
    <!--</script>-->
</head>
<body>
    <div id="info">
        <p style="color: blue">讲师信息</p>
        <div class="teacher_info info">
            python全栈工程师，7年工作经验，喜欢钻研python技术，对爬虫、
            web开发以及机器学习有浓厚的兴趣，关注前沿技术以及发展趋势。
            <p class="age">年龄: 29</p>
            <p class="name">姓名: bobby</p>
            <p class="work_years">工作年限: 7年</p>
            <p class="position">职位: python开发工程师</p>
        </div>
        <p style="color: aquamarine">课程信息</p>
        <table class="courses">
          <tr>
            <th>课程名</th>
            <th>讲师</th>
            <th>地址</th>
          </tr>
          <tr>
            <td>django打造在线教育</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/78.html">访问</a></td>
          </tr>
          <tr>
            <td>python高级编程</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/200.html">访问</a></td>
          </tr>
          <tr>
            <td>scrapy分布式爬虫</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/92.html">访问</a></td>
          </tr>
          <tr>
            <td>django rest framework打造生鲜电商</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/131.html">访问</a></td>
          </tr>
          <tr>
            <td>tornado从入门到精通</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/290.html">访问</a></td>
          </tr>
        </table>
    </div>

</body>
</html_test>

"""
bs = BeautifulSoup(html, "html.parser")
# title_tag = bs.title
# print(title_tag.string)
# div_tag = bs.div
# print(div_tag.string)
# div_tags = bs.find_all("div")
# for tag in div_tags:
#     print(tag.string)
# target = bs.find("div", id = re.compile("info-\d+"))
# children = target.descendants
# # for child in children:
# #     if child.name != None:
# #         print(child.name)
# # print(children)
# for next_tag in next_tags:
#     print(next_tag.string)
# next_tag = bs.find("p", {"class":"name"})
# print(next_tag.get("class"))

from scrapy import Selector

sel = Selector(text=html)
tag = sel.xpath("//div[1]/div[1]/p[1]/text()").extract()[0];
pass

