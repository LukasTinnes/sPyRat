from typing import List
from crawling.crawler_data_structures.crawl_files_data import CrawlFilesData


class CrawlerController:
    """
    The Crawler Controller is responsible for managing the crawlers given a crawler Config.
    """

    def __init__(self, crawler_config):
        self.crawler_config = crawler_config

    def crawl_for_patterns(self, files: List[str], patterns:List[str]) -> CrawlFilesData:
        """
        Crawls through a list of files and attempts to find the patterns given.
        The patterns are translated by using the previously defined CrawlerConfig.
        :param files:
        :param patterns:
        :return:
        """
        ...

    def crawl_specialized(self, files: List[str], patterns:List[List[str]]) -> CrawlFilesData:
        """
        Crawls through a list of files, finding an indivual assortment of oatterns for each file.
        :param files:
        :param patterns:
        :return:
        """
        ...
