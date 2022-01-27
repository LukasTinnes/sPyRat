from crawling.crawler import Crawler
from typing import List
import pickle


class CrawlerConfig:
    """
    Since we can hardly export the actual classes used in Crawling we need to define enums that correspond to them.
    This is the class for that.
    It contains a simple collection of pointers from string to Crawler.
    """

    def __init__(self):
        self.crawl_dict = {}

    def get_id_for_class(self, crawler_class:Crawler) -> str: # TODO Force bijektion
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
        return self.crawl_dict[pattern]

    def register_crawler_type(self, abbreviation:str, CrawlerClass: Crawler):
        """
        Register a new representation given the string and the class it is supposed to represent
        :param abbreviation:
        :param CrawlerClass:
        :return:
        """
        self.crawl_dict[abbreviation] = CrawlerClass

    def register_crawler_types(self, abbreviations:List[str], CrawlerClass: List[Crawler]):
        """
        Register multiple representations.
        :param abbreviations:
        :param CrawlerClass:
        :return:
        """
        for pattern, crawler in zip(abbreviations, CrawlerClass):
            self.register_crawler_type(pattern, crawler)

    def save(self, file):
        """
        Save the configuration to a file.
        :param file:
        :return:
        """
        with open(file, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file) -> CrawlerConfig:
        """
        Load the configuration from a file.
        :param file:
        :return:
        """
        with open(file, "rb") as file:
            return pickle.load(file)
