from crawling.crawler import Crawler
from typing import List


class CrawlerConfig:
    """
    Since we can hardly export the actual classes used in Crawling we need to define enums that correspond to them.
    This is the class for that.
    It contains a simple collection of pointers from string to Crawler.
    """

    def get_id_for_class(self, crawler_class:Crawler) -> str:
        """
        Returns the string representation of the given crawler.
        :param crawler_class:
        :return:
        """
        ...

    def get_class_for_id(self, pattern:str) -> Crawler:
        """
        Returns the class of the string representation
        :param pattern:
        :return:
        """
        ...

    def register_crawler_type(self, abbreviation:str, CrawlerClass: Crawler):
        """
        Register a new representation given the string and the class it is supposed to represent
        :param abbreviation:
        :param CrawlerClass:
        :return:
        """
        ...

    def register_crawler_types(self, abbreviations:List[str], CrawlerClass: List[Crawler]):
        """
        Register multiple representations.
        :param abbreviations:
        :param CrawlerClass:
        :return:
        """
        ...

    def save(self, file):
        """
        Save the configuration to a file.
        :param file:
        :return:
        """
        ...

    @staticmethod
    def load(file) -> CrawlerConfig:
        """
        Load the configuration from a file.
        :param file:
        :return:
        """
        ...

