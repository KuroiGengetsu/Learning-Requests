#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celebrity_quotes import *


def main():
    """main function"""
    url =  'http://www.mingyannet.com/'
    r = get_html(url)
    for topic, link in get_topics(r):
        print(topic, 'http://www.mingyannet.com/' + link)
        print('-' * 25)
        topic_link = find_topic(r.text, topic)
        q = get_quotes(topic_link, topic)
        q.show()
        q.write()


if __name__ == '__main__':
    main()
