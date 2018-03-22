"""class Quotes defines here"""

class Quotes():
    """This class is Quotes, which contains many quotes and a topic"""
    def __init__(self, topic=None, quotes=[]):
        """Given topic and quotes, or you can define them later"""
        self.topic = topic
        self.quotes = quotes

    def show(self):
        """Show the content of the Quotes"""
        print("-----", self.topic, "-----")
        for q in self.quotes:
            print(q)
        print("end")

    def write(self):
        """write informations to file"""
        with open("./files/" + self.topic + ".txt", mode='w', encoding='UTF-8') as f:
            for q in self.quotes:
                f.write(q + '\n')

