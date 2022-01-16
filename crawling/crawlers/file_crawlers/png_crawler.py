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


def end_byte_exists(end_byte):
    return end_byte != -1


def chunk_to_size(current_size_chunk):
    byte = bytearray(current_size_chunk)
    bytestring = b"", byte[0], byte[1], byte[2], byte[3]
    return int.from_bytes(bytestring, byteorder="big")


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
        df = self.define_dataframe()
        return CrawlData(df, "png")  # TODO pattern string

    def define_dataframe(self):
        df = DataFrame(self.rows)
        df.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return df

    def crawl_range(self, indices):
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
            pool.starmap(self.crawl_range, range(self.MAX_FILE_SIZE - 8))

    def add_row(self, index):
        start_byte = index
        end_byte = self.find_end_byte(index)
        if end_byte_exists(end_byte):
            size = end_byte - start_byte
            confidence = 0
            self.rows.append([start_byte, end_byte, size, confidence])

    def find_end_byte(self, index):
        current_index = index + 12
        current_size_chunk = self.bytes[current_index:current_index + 3]
        current_size = chunk_to_size(current_size_chunk)
        current_chunk_type = self.bytes[current_index + 4:current_index + 7]
        while current_chunk_type != ["I", "E", "N", "D"] and current_index < self.MAX_FILE_SIZE:
            current_index += current_size + 4
            current_size_chunk = self.bytes[current_index:current_index + 3]
            current_size = chunk_to_size(current_size_chunk)
            current_chunk_type = self.bytes[current_index + 4:current_index + 7]
        if current_index >= self.MAX_FILE_SIZE:
            return -1
        return current_index+12


if __name__ == "__main__":
    with open("C:\\Users\\Lukers\\Documents\\Zaunfreier Doggo.png", "rb") as f:
        print(f.read(32))
