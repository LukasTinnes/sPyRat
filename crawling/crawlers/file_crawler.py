from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
from abc import abstractmethod


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
        pass

    @abstractmethod
    def crawl_in_range(self, file: str, start_byte: int, end_byte: int) -> CrawlData:
        """
        Crawls the file for a file pattern between the start byte (inclusive) and the end_byte (exclusive).
        :param file: The file path
        :param start_byte: The byte to start crawling at.
        :param end_byte: The byte to end crawling at.
        :return:
        """
        ...

    @abstractmethod
    def crawl_at_byte(self, file:str, start_byte: int = 0) -> CrawlData:
        """
        Crawls for a file pattern at the specific byte given.
        :param file: The file path.
        :param start_byte: The byte to crawl at.
        :return:
        """
        ...
