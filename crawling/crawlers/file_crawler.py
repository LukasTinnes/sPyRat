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
