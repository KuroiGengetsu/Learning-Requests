 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celebrity_quotes import *


def main():
    """
    主函数
    """

    url =  'http://www.mingyannet.com/'

    # 请求
    r = get_html(url)

    for topic, link in get_topics(r.text):
        q = get_quotes(url + link, topic)
        q.show()
        q.write()


if __name__ == '__main__':
    main()

