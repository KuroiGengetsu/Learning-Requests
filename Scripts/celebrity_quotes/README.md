# 爬取名人名言

本文主要是从 [名人名言网站](http://www.mingyannet.com/) 爬取名人名言， 旨在练习 `python` 的 `requests` 库 与 *built-in* 的 `re` 模块

可以先通过 [requests英文官网](http://docs.python-requests.org/en/master/) 或 [requests中文官网](http://cn.python-requests.org/zh_CN/latest/) 学习一下 requests 库

然后从 [python官方教程 howto-regex](https://docs.python.org/3/howto/regex.html) 以及 [library 中的 re](https://docs.python.org/3/library/re.html) 学习正则表达式

## 简易教程

偶然发现这个网站, 比较适合拿来练手, 意图很简单, 那就是先从主页获得各种各样的话题, 接着访问这些话题的连接, 然后将这些名人名言保存到本地, 这是一种最简单的爬虫模式.

### Overview

这个小项目一共有四个文件:

  * `main.py`: 主函数定义在这里, 每次只需要执行这个文件就可以
	
  * `celebrity_quotes.py`: 一些主要的函数, 可以说它是整个项目的核心部分
	
  * `quotes.py`: 定义了一个类 `Quotes`, 用来存放爬下来的 **某个话题** 的名言
	
  * `settings.py`: 存放一些全局变量, 毕竟是小项目, 所以变量很少.

> `files` 文件夹下存放爬下来的名言, 可以先预览下

### 分析

一上来肯定是先要分析一波, 第一次点开这个网站就知道这个网站很容易拿来练习

首页上放了一堆 **话题**, 并且都是**链接**的形式, 他们的格式都是类似的, 出入不大, 具体情况到时候可以通过分析源代码来了解

随便点开一个链接, 里面的名言格式也比较工整, 猜测多数都可以通过一个表达式来获得, 当然现在只是分析, 写代码以及测试都是后边的事情, 现在不用关心, 只需要决定主要流程即可

拉到网页的最下面, 有 **第二页**, **第三页**, 点击之后, 发现与第一页并不是同一个话题, 回到主页发现有相同的话题, 而且内容都一样, 因此, **这是一个假的页数**, 所以这下就省劲了, 不用写翻页的代码了, 如果要写的话, 不小心就会陷入无尽的循环(如果不定义 **链接池** 的话, 也就是不判断是否爬取过相同的网页, 很容易就死循环)

所以经过上面的分析, 需要做的任务就是:

1. 通过 **主页** 获得 **话题** 与 **对应的链接**

2. 访问这些链接并爬取 **名言**
	
3. 将爬取到的名言通过 **话题** 归类(或许可以和上一步合为一步)
	
4. 处理这些数据

每次在写代码之前先规划好, 可以节省很多的时间, 这其实就是所谓的 **TODO**, 如果你有听说过 `org-mode`, 那么自然就懂.

接下来针对每一步进行更详细的规划

### 获取话题与链接

#### 发出请求并处理响应

爬虫的作用就是模仿人的动作去与网页打交道, 所以可以用来完成大量的、重复性的工作, 这其中最重要的一个协议就是 **HTTP 协议**, 了解 HTTP 可以增加对爬虫的理解(详见 **图解HTTP** 一书)

这一小结首先要了解的就是 HTTP 的 **GET 方法**, 以及 **HTTP 状态消息**(通常上来说就是状态码 status code)

首先为了获得 [名言网](http://www.mingyannet.com/ "名言网") [http://www.mingyannet.com/](http://www.mingyannet.com/) 的源代码, 也就是页面信息, 使用的是 *requests* 模块的 `get` 方法(对应 HTTP 的 GET 方法), 首先在终端里面进入 python 的解释器, 然后进行测试(Windows 上可以用 cmd 或者 powershell 或 编辑器集成的终端 或 python 自带的 shell, 输入 `python <ENTER>` 即可):

``` python
>>> import requests                     # 导入 requests 模块
>>> url = "http://www.mingyannet.com/"  # 将要访问的 URL
>>> r = requests.get(url)               # 使用 requests.get 方法发出请求(Requests)
>>> r.status_code                       # 查看 响应 Response
200                                     # 200 说明请求成功
>>> print(r.text)                       # 打印页面信息
<!DOCTYPE html ...

>>> r.encoding                          # 查看网页的原编码
'ISO-8859-1'
```

首先导入 `requests` 模块, 接着声明一个 url 变量, 然后使用 `requests.get()` 方法, 其第一个参数是 url, 它返回一个 **请求对象(Response object)**, 该对象拥有很多的属性, 比如 *headers* , *cookies* 等等, 可以通过 `dir(r)` 来查看.

``` python
>>> help(requests.get)
Help on function get in module requests.api:

get(url, params=None, **kwargs)
    Sends a GET request.
    
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

>>> dir(r)
[ ..., 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
```

目前我们需要的就是 `status_code` 属性, 也就是状态码, 如果它是 200, 就说明请求成功了, 如果是其它, 就说明请求失败, 想要详细了解所有的状态码, 去看 **图解HTTP** 这本书, 粗略地看一下就去 [w3cschool.com](http://www.w3school.com.cn/tags/html_ref_httpmessages.asp)

接下来处理 **编码**, 要用到的是 `r.encoding`, 相关的是 `r.apparent_encoding`, 他们之间是有区别的, `r.encoding` 是从 **HTTP请求头** 中获得的编码, 一般来说, 只要别是 *ISO-8859-1* 都没有太大问题, 这个问题指的就是 **让人头痛的乱码问题**. 所以遇到 *ISO-8859-1* 就需要做一些处理:

1. 你可以亲自去翻网页的源代码找 `charset` 属性, 然后将 `r.encoding` 赋值成对应的编码
  
2. 也可以利用 `requests.utils.get_encodings_from_content(r.text)`, 它返回的结果是一个列表, 包含了匹配到的所有编码, 通常就一个
  
3. 利用 `r.apparent_encoding`, 根据页面内容推测编码, 如果你懒的话确实可以直接将 `r.encoding = r.apparent_encoding` 赋值, 但是 `apparent_encoding` 比较慢, 花的时间长
  
所以如果遇到了 *ISO-8859-1*, 通常用的是第二种方法

由于现在是测试, 所以可以看看他们的结果分别是什么

采用第一种方法, 就是去看源代码中的 `<head>` 标签中的信息:

``` html
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
```

于是就能知道该页面的编码是 *gb2312*

第二种方法:

``` python
>>> requests.utils.get_encodings_from_content(r.text)
['gb2312']
```

与第一种方法吻合, 没问题

第三种方法:

``` python
>>> r.apparent_encoding
'GB2312'
```

同样吻合

具体关于第二种方法和第三种方法的区别, 直接看 `requests` 库的源代码就能知道:

  * [get_encodings_from_content](http://docs.python-requests.org/en/master/_modules/requests/utils/#get_encodings_from_content)
  
  * [Response](http://docs.python-requests.org/en/master/_modules/requests/models/#Response) 从链接中找到 `apparent_encoding`

于是我们需要做的就是将 编码的字符串赋值给 `r.encoding`:

``` python
>>> r.encoding = 'GB2312'
```

`r.text` 使用到属性会调用 `r.encoding`, 所以如果不处理好编码的问题, 会对信息提取造成很大的干扰

#### 使用正则表达式匹配话题和链接

**正则表达式(regular expression, regex, re)** 对于提取信息有很大的帮助, 虽然 python 提供了很多解析 HTML 的库, 但是学习正则表达式依然是基础中的基础, 就比如说 `BeautifulSoup` 这个解析库, 它的内部就是由正则表达式实现的, 当然了, 并不是叫你以后一直使用正则表达式, 这里只是对它进行简单使用罢了

在使用之前, 有必要了解它的好处与弊端. python 的 **re** 模块提供了正则表达式的 API, 它是用 **C语言** 实现的, 可以通过阅读 [python 的官方文档](https://docs.python.org/3/howto/regex.html) 中的 `howto-regex` 这一篇文章来基础学习, 你也可以把整个 python 官方文档的压缩包下载到本地, 然后找到 `howto-regex.pdf` 进行阅读, 当然配套的就是 python 内建库, 即 `library.pdf` 中对 re 模块 API 的教程, 这两个都属于 python 官方文档, 你要是想很好地掌握最新版本的 python, **官方文档永远是最好的选择**

当然正则表达式几乎是所有语言通用的, 区别会有, 但是不大, 它的基础语法是基本不会变的

正则表达式通过 *patterns* 来匹配(我并不知道该叫什么好, 于是就叫 *pattern*), 通俗的说就是表达式, 比如上一小节中使用到了 `get_encodings_from_content` 这个方法, 源代码中 `<meta.*?charset=["\']*(.+?)["\'>]` 就是用来匹配 html 文档中的 *charset* 属性, 它就叫一个 *pattern*

回到正题, 我们需要匹配的是 话题 和 链接, 下面是我们需要匹配的部分(为了方便, 省略了大部分):

``` html
<ul>
    <li>
	    <a title="创业励志名言大全" target="_blank" href="show/7511113240940">创业励志名言大全</a>
	</li>
	<li>
	    <a title="树立志向的格言警句" target="_blank" href="show/8852217160902">树立志向的格言警句</a>
	</li>
	<li>
	    <a title="先失败后成功的名言" target="_blank" href="show/9793016160957">先失败后成功的名言</a>
	</li>
	<li>
...
```

可以看到, 我们需要的 话题 以及 链接 都在 a 标签里面, 并且话题在 *title* 属性 和 主要内容里, 由于一样, 所以我们选一个匹配就好, 而链接在 `href` 属性里面, 接下来可以开始构造表达式了(回到终端中):

``` python
>>> # 别忘了 r.encoding = 'GB2312' 或使用上一节任意方法赋值, 注意是字符串

>>> import re                        # 导入 re 模块
>>> regex = re.compile(r'<a title="(.*?)".*?href="(show/\w+)">')
>>> topic_link = []
>>> for topic, link in regex.findall(r.text):
...     print(topic, url + link)                 # 不要忘记缩进, GitHub 可能显示有问题
...     topic_link.append((topic, url + link))

创业励志名言大全 http://www.mingyannet.com/show/7511113240940
树立志向的格言警句 http://www.mingyannet.com/show/8852217160902
先失败后成功的名言 http://www.mingyannet.com/show/9793016160957
关于狼性的励志名言 http://www.mingyannet.com/show/9102316160939
职场励志名言大全 http://www.mingyannet.com/show/4852615020709
...
```

好了, 我们的目标达成了



`r''` 在 python 中是 **raw 字符串**, 也就是原生字符串, 也就是 **所见即所得, 不会转义**, 转义字符多了去了, `\n`, `\t` 等等由反斜杠加一个或多个字符组成的来表示某些特殊意义的字符就叫做转义字符, 而在字符串之前加上 前缀 `r`, 这个字符串就变成了原生字符串, 也就是说, `r'\n'` 就是 `'\\n'` 的意思, **不要把转义字符与正则表达式中的 metacharacter 搞混!**

正则表达式中也有 `\w`, `\s`, `*` 等等字符, 他们与转义字符是不同的, 叫做 *metacharacter*, 具有特殊含义, 总之记住, 使用正则表达式的时候, 给它加上 `r` 前缀就不会错, 下面是一些 metacharacters 的示例:

| metacharacter | 说明 |
| :--: | :-- |
| `.` | 代表任意字符, 默认是除了 换行符 `'\n` 以外的所有字符 |
| `^` | 一行中匹配字符串的开始, 简单来说就是跳过 **前面** 的空白 |
| `$` | 匹配一行的结尾 |
| `*` | 重复前面一个字符 0 或 无穷次, 例如 `a*` 可以匹配 `""`, `"a"`, `"aaaaa"` 等等, 默认是 **贪婪模式 Greedy**, 也就是能匹配无穷次不匹配1次 这个道理 |
| `+` | 重复前面一个字符 1 或无穷次, 例如 `a+` 可以匹配 `"a"`, `"aa"`, `"aaaaa"` 等等 默认 **贪婪模式**|
| `?` | 匹配前面一个字符 0 或 1 次, 例如 `a?` 可以匹配 `""` 和 `"a"` |
| `{m,n}` | 至少匹配前面的字符 m 次, 最多 n 次, m 或 n 可以省略其中的一个, `{m}` 表示至少 m 次, `{,n}` 表示至多 n 次. 默认 **贪婪模式**, 注意逗号后面没有空格 |
| `[]` | 匹配方括号中的 **任意一个**, 也就是说, `[abc]` 可以匹配 `"a"`, `"b"`, `"c"` 中的一个, 这只是一种写法, 可以把字母都列出来, 还有一种就是用 `-` 连接起来表示范围, 如 `[a-z]` 表示 a 到 z 中任意一个字符, 也可以是 **Unicode编码**, 如 `[\u30a0-\u30ff]` |
| `[^]` | 与上边类似, 只是这个与上边相反, 这个是 **不匹配**, 比如 `[^abc]` **不会** 匹配 `"a"` `"b"` `"c"` 中的任何一个 |
| `\` | 用来将 metacharacter 变成普通的字符, 例如 `\*` 就表示 `*` 这个符号, 没有了上边的特殊含义 |
| `|` | 逻辑或, 比如 `hello|world` 会匹配 `hello` 或 `world` |
| `()` | 这个就是所谓的 *group*, 比如 `aaaaaaa123------444` 这个字符串, 使用 `a+([0-9]+)-+(4+)` 就会匹配到 `(123, 444)`, python 中是以 **元组** 的形式返回的 |
| `\d` | 数字, 等同于 `[0-9]` |
| `\D` | 非数字, 等同于 `[^0-9]` |
| `\s` | 匹配空白, 比如空格, 换行, 制表符 |
| `\S` | 匹配除了空白以外的所有字符 |
| `\w` | 数字字母, 相当于 `[0-9a-zA-Z]` |
| `\W` | 除了数字字母以外的字符, 相当于 `[^0-9a-zA-Z]` |

> 注: 消除贪婪模式的方法很简单, 就是在 `*` 后边加一个 `?`, 所以 `.*?` 就变得不贪婪了, 所以 要是用 `<.*>` 来匹配 `<123456>abcdef<>` 的话, 能匹配到 `<123456>abcdef<>`, 而用 `<.*?>` 的话, 会匹配到 `<123456>`

有了以上的基础, 就入门了, 当然 `howto-regex` 比这里描述的要详细的多而且深入

讲一下刚刚写的 pattern: `r'<a title="(.*?)".*?href="(show/\w+)">'`

`<a title="先失败后成功的名言" target="_blank" href="show/9793016160957">先失败后成功的名言</a>`

为了对比, 我把要匹配的也写在上面, 前面的 `<a title=` 是固定的, `"(.*?)"` 匹配话题, 而且是非贪婪模式, 紧跟着的 `.*?` 是为了匹配 `target` 属性直到 href 前面, `"(show/\w+)"` 就是来匹配链接的, 当然这里只是相对路径, 绝对路径好要加上网站的完整网址

再来解释以下 `re.compile(pattern)` 这个函数, 从名字就知道, 它是用来 **编译 compile** 表达式的, 当然这里可以理解为加载到内存, 如果要多次用到这个匹配式, 最好将它单独放在一个模块里或者放在全局变量, 而不是放到函数中, 这样可以避免每次都重新加载它而浪费时间, 为了方便, 我这里只是将他们放到了全局变量中, 以后的话最好还是单独放到一个模块中, 可以去搜索 `.pyc` 相关的内容

`findall` 函数就简单啦, 就是从给定的字符串中找到所有的匹配项, 并以列表的形式返回, 如果有 *group* , 列表中的元素就是 **元组 tuple** 了, 元组中的元素还是字符串, 我们这里就是返回了一个 **二元元组**, 它的第一个元素是 *topic*, 第二个是 *link*

Ok, 可以进行下一步了

### 从每一个话题的链接中爬取名言

