import numpy as np
import logging
from crawling.crawlers.file_crawler import FileCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool

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
    byte = bytearray(current_size_chunk)
    bytestring = b"", byte[0], byte[1], byte[2], byte[3]
    return int.from_bytes(bytestring, byteorder="big")


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
    logging.debug(("Signature: ", str(signature), " Index: ", str(index), " lf: ", str(line_feed), " carriage: ",
                   str(carriage_return), " lf2: ", str(line_feed_2), " textc: ", str(text_close), "zeroes: ",
                   str(zero_bytes)))
    return signature, carriage_return, line_feed, text_close, line_feed_2, zero_bytes


class PNGCrawler(FileCrawler):
    POOL_SIZE = 4
    HEADER_SIZE = 11

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
        return index + self.HEADER_SIZE < self.MAX_FILE_SIZE

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
        with open(file, "rb") as f:
            current_index = index + 12
            f.seek(current_index)
            current_size_chunk = f.read(4)
            current_size = png_chunk_to_size(current_size_chunk)
            current_chunk_type = f.read(4)
            while current_chunk_type != b"IEND" and current_index < self.MAX_FILE_SIZE:
                current_index += current_size + 4
                f.seek(current_index)
                current_size_chunk = f.read(4)
                current_size = png_chunk_to_size(current_size_chunk)
                current_chunk_type = f.read(4)
            if current_index >= self.MAX_FILE_SIZE:
                return -1
            return current_index + 12

    def get_crawl_ranges(self, file):
        pairs = get_pairs(file, self.MAX_FILE_SIZE, self.POOL_SIZE)
        return pairs


if __name__ == "__main__":
    test = PNGCrawler()
    test.crawl("C:\\Users\\Lukers\\Documents\\fouroclocks.png")
