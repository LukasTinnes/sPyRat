from .file_crawler import FileCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import itertools
from pandas import DataFrame
from multiprocessing.pool import Pool
import os
import math

class TxtAsciiCrawler(FileCrawler):

    def __init__(self, min_size=0):
        self.min_size = min_size

    POOLS = 4

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file:
        :return:
        """
        file_size_in_bytes = os.path.getsize(file)
        rows = self.crawl_range((0, file_size_in_bytes, file))

        df = DataFrame(rows)
        df.rename(columns={0:"start_byte", 1:"end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, "ascii.txt") # TODO pattern s tring

    def crawl_range(self, args):
        start = args[0]
        end = args[1]
        file = args[2]

        rows = []
        read_state = False
        read_byte = -1

        with open(file, "rb") as f:
            for i in range(start, end):
                textbyte = f.read(1)
                val = int.from_bytes(textbyte, "little", signed=False)
                if val in range(32, 127) or val in [9, 10, 11, 13]:
                    if not read_state:
                        read_byte = i
                        read_state = True
                else:
                    if read_state and i-read_byte > self.min_size:
                        rows.append([read_byte, i, i-read_byte, ((127-32+4)/256)**(i-read_byte)])
                        read_state = False
            if read_state:
                rows.append([read_byte, end-1, end-1 - read_byte, math.log(((127 - 32 + 4) / 256) ** (end-1 - read_byte),2)])
        return rows
