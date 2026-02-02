from threading import Thread
from utility import delay


class Multispider:

    def __init__(self, spiders):
        self.spiders = spiders
        self.threads = []

    def multi_crawl(self):
        self.threads = [
            Thread(target=spider.crawl)
            for spider in self.spiders
        ]

        for t in self.threads:
            delay(1, 2)
            t.start()

        for t in self.threads:
            t.join()
