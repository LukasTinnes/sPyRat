import logging
import os
from multiprocessing import Pool

from pandas import DataFrame

from crawling.crawler_data_structures.crawl_data import CrawlData
from crawling.crawlers.file_crawler import FileCrawler

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)


def get_max_size_of_file(file):
    return os.path.getsize(file)


def signature_is_valid(signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes):
    if signature != b"PNG":
        return False
    if carriage_return != b'\r' or line_feed != b'\n' or text_close != b"\x1a" or line_feed_2 != b"\n":
        return False
    if zero_bytes != b"\x00\x00\x00":
        return False
    return True


def end_byte_exists(end_byte):
    return end_byte != -1


def png_chunk_to_size(current_size_chunk):
    return int.from_bytes(current_size_chunk, byteorder="big")


def get_pairs(file, max_file_size, pool_size):
    pairs = []
    chunk_sizes = max_file_size // pool_size
    start = 0
    end = chunk_sizes
    pairs.append((file, start, end))
    while end < max_file_size:
        start = end + 1
        end += chunk_sizes + 1
        if end >= max_file_size:
            end = max_file_size
        pairs.append((file, start, end))
    return pairs


def parse_header(file, index):
    file.seek(index)
    signature = file.read(3)
    carriage_return = file.read(1)
    line_feed = file.read(1)
    text_close = file.read(1)
    line_feed_2 = file.read(1)
    zero_bytes = file.read(3)
    return signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes


def end_not_found(next_bytes):
    return next_bytes != b"IEND"


class PNGCrawler(FileCrawler):
    POOL_SIZE = 4
    SIGNATURE_SIZE = 11
    HEADER_SIZE = 17
    END_HEADER_SIZE = 4
    END_OF_FILE_FOUND = -1
    END_HEADER_CRC = 3

    def __init__(self):
        self.MAX_FILE_SIZE = 0
        self.rows = []

    def crawl(self, file: str) -> CrawlData:
        self.MAX_FILE_SIZE = get_max_size_of_file(file)
        self.crawl_by_pools(file)
        df = self.define_dataframe()
        return CrawlData(df, "png")  # TODO pattern string

    def define_dataframe(self):
        df = DataFrame(self.rows)
        df.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return df

    def crawl_range(self, file, start, stop):
        with open(file, "rb") as f:
            for index in range(start, stop):
                if self.header_is_in_bounds(index):
                    signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes = parse_header(f,
                                                                                                              index)
                    if signature_is_valid(signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes):
                        self.add_row(file, index)

    def header_is_in_bounds(self, index):
        return index + self.SIGNATURE_SIZE < self.MAX_FILE_SIZE

    def crawl_by_pools(self, file: str):
        ranges = self.get_crawl_ranges(file)
        with Pool(self.POOL_SIZE) as pool:
            pool.starmap(self.crawl_range, ranges)

    def add_row(self, file, index):
        start_byte = index
        end_byte = self.find_end_byte(file, index)
        if end_byte_exists(end_byte):
            size = end_byte - start_byte
            confidence = 0
            self.rows.append([start_byte, end_byte, size, confidence])

    def find_end_byte(self, file, index):
        return_index = index
        with open(file, "rb") as f:
            f.seek(index)
            next_bytes = f.read(self.END_HEADER_SIZE)
            while end_not_found(next_bytes):
                if return_index >= self.MAX_FILE_SIZE:
                    return self.END_OF_FILE_FOUND
                f.seek(return_index)
                next_bytes = f.read(self.END_HEADER_SIZE)
                return_index += 1
            return return_index + self.END_HEADER_SIZE + self.END_HEADER_CRC

    def get_crawl_ranges(self, file):
        pairs = get_pairs(file, self.MAX_FILE_SIZE, self.POOL_SIZE)
        return pairs
