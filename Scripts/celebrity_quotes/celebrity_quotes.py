"""crawl Celebrity Quotes on http://www.mingyannet.com/"""
import re
from functools import reduce
import requests
import settings
from quotes import Quotes
from regex import *


def get_html(url):
    """get the url from web
    :param url: URL
    :return type: Response Object
    """

    r = requests.get(url=url, headers=settings.HEADERS)

    if r.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(r.text)
        if encodings:
            r.encoding = encodings[0]
        else:
            r.encoding = r.apparent_encoding

    if r.status_code != 200:
        print(settings.DEBUG + "Failed to get", url, ". Status code:", r.status_code)
    else:
        print(settings.DEBUG, "Get", url, "successfully!")

    return r


def get_quotes(url, topic):
    """get the quotes from the given url
    :param url: given url
    """

    r = get_html(url)
    quotes = QUOTES_REGEX.findall(r.text)

    q = Quotes(
        quotes=[reduce(REMOVE, [s] + SPECIAL_SYMBOL_REGEX.findall(s)) for s in quotes],
        topic=topic
    )

    return q


def get_topics(text):
    """get all the topics and return a list
    :param response: the response of the main page
    :return type: a tuple with two elements
    :return: the topic name and the link
    """

    return TOPIC_LINK_REGEX.findall(text)

