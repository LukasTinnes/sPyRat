from abc import abstractmethod
from pandas import DataFrame
from crawling.crawler_data_structures.crawl_data import CrawlData


class Crawler:
    """
    An abstract class for other Crawlers to inherit from.
    A Crawler should open a given file and attempt to find an associated file pattern at every byte in the given file.
    """

    @abstractmethod
    def crawl(self, file: str) -> CrawlData:
        """
        Crawls a file to find a certain file pattern at every byte.
        :param file:
        :return:
        """
        ...

    @abstractmethod
    def export(self, data: DataFrame, file: str):
        """
        Export all files given in the data frame into the given file.
        :param data:
        :param file:
        :return:
        """
        ...
