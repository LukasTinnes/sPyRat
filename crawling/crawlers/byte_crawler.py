from .file_crawler import FileCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import itertools
from pandas import DataFrame
from multiprocessing.pool import Pool
import os
import math


class ByteCrawler(FileCrawler):
    """
    Crawls through a file to find sequences containing specific bytes.
    """

    def __init__(self, min_size=0, elements=None, pattern="byte"):
        self.min_size = min_size
        self.elements = [] if elements is None else elements
        self.pattern = pattern

    POOLS = 4

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file: The file path
        :return:
        """
        return self.crawl_in_range(file, 0, os.path.getsize(file))

    def _fix_overlap(self, results: list) -> list:
        """
        Concatenates strings together that overlap over multiple buckets.
        :param results: The results given by the crawling.
        :return:
        """
        # The last bin can be excluded
        for x in range(len(results) - 1):

            # Get the two bins to search for strings in.
            first = results[x]
            second = results[x + 1]

            # If either of the bins are emtpy, we don't care.
            if len(first) == 0 or len(second) == 0:
                continue

            # We only need to care about the resluts that may be directly adjacent.
            first_last = first[-1]
            second_first = second[0]

            # Check if the second string starts exactly where the first ends.
            if first_last[1] == second_first[0] - 1:
                # Create a new string combing the original ones.
                new_element = [first_last[0], second_first[1], second_first[1] - first_last[0],
                               first_last[3] + second_first[3]]

                # Remove old string, add new string.
                first = first[:-1]
                second = [new_element] + second[1:]
                results[x] = first
                results[x + 1] = second
        return results

    def crawl_range(self, args):
        """
        Crawls through a range of bytes to find the byte sequences.
        :param args: The arguments given by the pools. (start_byte, end_byte, file path)
        :return:
        """
        start = args[0]
        end = args[1]
        file = args[2]

        rows = []
        read_state = False
        read_byte = -1

        with open(file, "rb") as f:
            f.seek(start)
            for i in range(start, end):
                textbyte = f.read(1)
                val = int.from_bytes(textbyte, "little", signed=False)

                if val in self.elements:
                    if not read_state:
                        read_byte = i
                        read_state = True
                else:
                    if read_state and i-read_byte > self.min_size:
                        rows.append([read_byte, i, i-read_byte, ((127-32+4)/256)**(i-read_byte)])
                        read_state = False
            if read_state:
                confidence = math.log((len(self.elements) / 256) ** (end-1 - read_byte), 2)
                rows.append([read_byte, end-1, end-1 - read_byte, confidence])
        return rows

    def crawl_in_range(self, file: str, start_byte: int, end_byte: int) -> CrawlData:
        """
        Crawls the file for the bytes between the start byte (inclusive) and the end_byte (exclusive).
        :param file: The file path
        :param start_byte: The byte to start crawling at.
        :param end_byte: The byte to end crawling at.
        :return:
        """
        size= end_byte - start_byte

        with Pool(self.POOLS) as p:
            # The crawling ranges are divided into approx. equal sections.
            ranges = [(start_byte + round(x*size/self.POOLS), start_byte + round((x+1)*size/self.POOLS), file) for x in range(self.POOLS)]

            results = p.map(self.crawl_range, ranges)
            results = self._fix_overlap(results)

            # Concatenate results in list
            rows = list(itertools.chain.from_iterable(results))

        df = DataFrame(rows)
        df.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, self.pattern)

    def crawl_at_byte(self, file: str, start_byte: int = 0) -> CrawlData:
        """
        Crawls for a bytes at the specific byte given.
        :param file: The file path.
        :param start_byte: The byte to crawl at.
        :return:
        """
        return self.crawl_in_range(file, start_byte, start_byte+1)
