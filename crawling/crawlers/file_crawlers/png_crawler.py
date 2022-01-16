from crawling.crawlers.file_crawler import FileCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool


class JPGCrawler(FileCrawler):

    HEADER_SIZE = 11

    def __init__(self):
        self.MAX_FILE_SIZE = 0
        self.bytes = []

    def crawl(self, file: str) -> CrawlData:
        self.MAX_FILE_SIZE = os.path.getsize(file)
        with open(file, "rb") as f:
            self.bytes = f.read()
        with Pool(4) as pool:
            pool.starmap(self.check_byte, range(self.MAX_FILE_SIZE - 8))

    def check_byte(self, index):
        if index + self.HEADER_SIZE < self.MAX_FILE_SIZE:
            byte_01, file_signature, carriage_return, line_feed, byte_07, parity, zero_bytes = self.parse_header(index)

    def parse_header(self, index):
        # header = self.bytes[]
        pass

if __name__ == "__main__":
    with open("C:\\Users\\Lukers\\Documents\\fouroclocks.png", "rb") as f:
        data = f.read()
        print(data)
