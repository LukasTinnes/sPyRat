from crawling.crawlers.file_crawler import FileCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool


def get_max_size_of_file(file):
    return os.path.getsize(file)


def signature_is_valid(signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes):
    if signature != "PNG":
        return False
    if carriage_return != b'\r' or line_feed == b'\n':
        return False



class JPGCrawler(FileCrawler):

    POOL_SIZE = 4
    HEADER_SIZE = 11

    def __init__(self):
        self.MAX_FILE_SIZE = 0
        self.bytes = []
        self.rows = []

    def crawl(self, file: str) -> CrawlData:
        self.MAX_FILE_SIZE = get_max_size_of_file(file)
        self.read_byte_stream(file)
        self.crawl_by_pools()

    def check_bytes(self, indices):
        for index in indices:
            if self.header_is_in_bounds(index):
                signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes = self.parse_header(index)
                if signature_is_valid(signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes):
                    self.add_row(index)

    def header_is_in_bounds(self, index):
        return index + self.HEADER_SIZE < self.MAX_FILE_SIZE

    def parse_header(self, index):
        # header = self.bytes[]
        pass

    def read_byte_stream(self, file):
        with open(file, "rb") as file_stream:
            self.bytes = bytes(file_stream.read())

    def crawl_by_pools(self):
        with Pool(self.POOL_SIZE) as pool:
            pool.starmap(self.check_bytes, range(self.MAX_FILE_SIZE - 8))


if __name__ == "__main__":
    with open("C:\\Users\\Lukers\\Documents\\Zaunfreier Doggo.png", "rb") as f:
        for x in range(11):
            print(f.read(1))
