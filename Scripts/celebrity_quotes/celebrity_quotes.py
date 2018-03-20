"""crawl Celebrity Quotes on http://www.mingyannet.com/"""
import re
from functools import reduce
import requests
from quotes import Quotes

def get_html(url):
    """get the url from web
    :param url: the URL
    :return: Response Object
    """

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;',
        'accept-language': 'zh_CN,zh;q=0.8',
        'user-agent': 'Chrome/61.0.3293.100 Mozilla/5.0(Windows NT 6.3) AppleWebKit/537.87(KHTML,like Gecko) Safari/537.65'
    }
    r = requests.get(url=url, headers=headers)
    r.encoding = r.apparent_encoding
    print('get url', url, 'status code:', r.status_code)
    r.raise_for_status()
    return r


def find_topic(text, topic):
    """find topic from the response, and return the link
    :response: for example, r.text
    :topic: the topic you want to find, string.
    """
    link = re.search('<a title="%s".*href="(.*)".*' % topic, text)
    if link:
        return 'http://www.mingyannet.com/' + link.group(1)
    else:
        raise ValueError("Can't find any topic links!")


def get_quotes(url, topic):
    """get the quotes from the given url
    :param url: given url
    """
    r = get_html(url)
    quotes = re.findall(r'<p>(\d.*)</p>', r.text)
    no_need = ["&mdash;", "&middot;"]
    remove = lambda x, y: x.replace(y, "")
    q = Quotes(quotes=[reduce(remove, [s] +  no_need) for s in quotes], topic=topic)
    return q

def get_topics(response):
    """get all the topics and return a list
    :param response: the response of the main page
    :return: list
    """
    regex = re.compile(r'<li><a title="(\w*)" target="_blank" href="(show/\d*)">\w*</a></li>')
    for topic in regex.finditer(response.text):
        yield topic.groups()
