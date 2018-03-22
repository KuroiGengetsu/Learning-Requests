# 爬取名人名言

本文主要是从 [名人名言网站](http://www.mingyannet.com/) 爬取名人名言， 旨在练习 `python` 的 `requests` 库 与 *built-in* 的 `re` 模块

可以先通过 [requests英文官网](http://docs.python-requests.org/en/master/) 或 [requests中文官网](http://cn.python-requests.org/zh_CN/latest/) 学习一下 requests 库

然后从 [python官方教程 howto-regex](https://docs.python.org/3/howto/regex.html) 以及 [library 中的 re](https://docs.python.org/3/library/re.html) 学习正则表达式

## 简易教程

偶然发现这个网站, 比较适合拿来练手, 意图很简单, 那就是先从主页获得各种各样的话题, 接着访问这些话题的连接, 然后将这些名人名言保存到本地, 这是一种最简单的爬虫模式.

### Overview

这个小项目一共有五个文件:

* `main.py`: 主函数定义在这里, 每次只需要执行这个文件就可以
	
* `celebrity_quotes.py`: 一些主要的函数, 可以说它是整个项目的核心部分
	
* `quotes.py`: 定义了一个类 `Quotes`, 用来存放爬下来的 **某个话题** 的名言
	
* `settings.py`: 存放一些全局变量, 毕竟是小项目, 所以变量很少.

* `regex.py`: 主要存放正则表达式

> `files` 文件夹下存放爬下来的名言, 可以先预览下

**multiprocess 线** 与 **master 线** 的不同:
 
* 采用多进程, 能够在 **一秒左右** 爬完全部内容
>
* 更改一些代码组织方式

> The crazy multiprocess Pool!!!

