"""定义了一个 Quotes 类"""

class Quotes():
    """class Quotes , 用来存放 一个 topic 以及众多 quotes"""

    def __init__(self, topic=None, quotes=[]):
        """
        创建对象的时候给定两个参数, 话题 topic 和 名言 quotes
        
        Parameters
        ----------
        :param topic: str
            话题 topic, 例如 "创业励志名言大全"
        :param quotes: list
            名言
        """

        self.topic = topic
        self.quotes = quotes

    def show(self):
        """
        展示一个 Quotes 类的内容
        
        Parameters
        ----------
        :rtype: None
        """

        print("-----", self.topic, "-----")
        for q in self.quotes:
            print(q)
        print("end")

    def write(self):
        """
        将一个 Quotes 类的信息写入文件, 为了方便起见, 以 txt 为例子
        :rtype: None
        """

        with open("./files/" + self.topic + ".txt", mode='w', encoding='UTF-8') as f:
            for q in self.quotes:
                f.write(q + '\n')           

