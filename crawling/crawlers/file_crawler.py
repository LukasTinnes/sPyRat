from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
from abc import abstractmethod
import os


class FileCrawler(Crawler):
    """
    Crawls through a file to find a file pattern at each byte.
    """

    @abstractmethod
    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file:
        :return:
        """
        file_size_in_bytes = os.path.getsize(file)
        with open(file, "rb") as f:
            for i in range(file_size_in_bytes):
                f.seek(i)
                header_bytes = f.read(2)
                header_field_string = header_bytes.decode("ASCII")
                if header_field_string in ["BM", "BA", "CI", "CP", "IC", "PT"]:
                    self._crawl_at_byte(file, i, header_field_string)

    def _crawl_at_byte(self, file, index, header_field_string):
        ...
