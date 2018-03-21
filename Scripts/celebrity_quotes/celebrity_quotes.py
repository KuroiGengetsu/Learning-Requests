"""crawl Celebrity Quotes on http://www.mingyannet.com/"""
import re
from functools import reduce
import requests
import settings
from quotes import Quotes


def get_html(url):
    """get the url from web
    :param url: URL
    :return type: Response Object
    """

    r = requests.get(url=url, headers=settings.HEADERS)
    r.encoding = r.apparent_encoding

    if r.status_code != 200:
        print(settings.DEBUG + "Failed to get", url, ". Status code:", r.status_code)
    else:
        print(settings.DEBUG, "Get", url, "successfully!")

    return r


# def find_topic(text, topic):
#     """find topic from the response, and return the link
#     :response: for example, r.text
#     :topic: the topic you want to find, string.
#     """

#    link = re.search('<a title="%s".*href="(.*)".*' % topic, text)
#     if link:
#         return 'http://www.mingyannet.com/' + link.group(1)
#     else:
#         print(settings.DEBUG + "Can not find topic", topic)


REMOVE = lambda x, y: x.replace(y, "")
QUOTES_REGEX = re.compile(r'<p>(\d+、[^<]*)</p>')

def get_quotes(url, topic):
    """get the quotes from the given url
    :param url: given url
    """

    r = get_html(url)
    quotes = QUOTES_REGEX.findall(r.text)

    q = Quotes(
        quotes=[reduce(REMOVE, [s] + settings.UNWANTED) for s in quotes],
        topic=topic
    )

    return q


TOPIC_REGEX = re.compile(r'<li><a title="(\w*)" target="_blank" href="(show/\d*)">\w*</a></li>')

def get_topics(text):
    """get all the topics and return a list
    :param response: the response of the main page
    :return type: a tuple with two elements
    :return: the topic name and the link
    """

    for topic in TOPIC_REGEX.finditer(text):
        yield topic.groups()

