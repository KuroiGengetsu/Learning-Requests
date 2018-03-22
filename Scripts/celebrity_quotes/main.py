#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Pool
from celebrity_quotes import *


URL =  'http://www.mingyannet.com/'


def main(topic_link):
    """main function"""
    q = get_quotes(URL + topic_link[1], topic_link[0])
    q.write()


if __name__ == '__main__':
    r = get_html(URL)
    with Pool(5) as p:
        p.map(main, get_topics(r.text))

