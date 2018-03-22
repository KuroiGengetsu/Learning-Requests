"""
从 http://www.mingyannet.com/ 爬取名人名言
"""
import re
from functools import reduce
import requests
import settings
from quotes import Quotes


def get_html(url):
    """
    从给定 url 发出请求, 并返回响应
    :param url: str
        给定的 URL
    :rtype: Response Object
        Response 对象
    """

    # 通过给定 url 发出请求, headers 将爬虫伪装成浏览器
    r = requests.get(url, headers=settings.HEADERS)

    # 判断 响应的编码是否是 ISO-8859-1
    if r.encoding == 'ISO-8859-1':
        # 从响应的内容中获得编码
        encodings = requests.utils.get_encodings_from_content(r.text)
        # 如果成功
        if encodings:
            r.encoding = encodings[0]
        # 否则用另一种方法
        else:
            r.encoding = r.apparent_encoding

    # 判断响应是否成功
    if not r.ok:
        print(settings.DEBUG + "Failed to get", url, ". Status code:", r.status_code)
    else:
        print(settings.DEBUG, "Get", url, "successfully!")

    return r


TOPIC_LINK_REGEX = re.compile(r'<a title="(.*?)".*?href="(show/\w+)">')

def get_topics(text):
    """
    获得所有的话题与对应的链接
    :param text: str, 即 r.text
    :rtype: 二元元组, 迭代器
    :return: (topic, link)  iterator
    """

    for topic in TOPIC_LINK_REGEX.finditer(text):
        yield topic.groups()


# 匿名函数, lambda 表达式, 给定两个参数 x, y, 将 y 从 x 中除去
REMOVE = lambda x, y: x.replace(y, "")

# 匹配名言
QUOTES_REGEX = re.compile(r'<p>(\d+、[^<]*)</p>')

# 匹配一些不想要的特殊符号例如 &nbsp;
SPECIAL_SYMBOL_REGEX = re.compile(r'&\w+;')


def get_quotes(url, topic):
    """
    从给定的 url 以及 话题中获得名言信息, 返回 Quotes 对象
    :param url: str
        给定的 url
    :param topic: str
        话题
    :rtype: Quotes 对象
    """

    # 请求
    r = get_html(url)
    # 匹配所有的名言
    quotes = QUOTES_REGEX.findall(r.text)

    # 创建 Quotes 对象, 将不想要的符号剔除
    q = Quotes(
        quotes=[reduce(REMOVE, [s] + SPECIAL_SYMBOL_REGEX.findall(s)) for s in quotes],
        topic=topic
    )

    return q

