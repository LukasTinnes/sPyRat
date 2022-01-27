from typing import List
from crawling.crawler_data_structures.crawl_patterns_data import CrawlPatternsData
from crawling.crawler_config import CrawlerConfig


class CrawlerController:
    """
    The Crawler Controller is responsible for managing the crawlers given a crawler Config.
    """

    def __init__(self, crawler_config):
        self.crawler_config: CrawlerConfig = crawler_config

    def crawl_for_patterns(self, file: str, patterns: List[str]) -> CrawlPatternsData:
        """
        Crawls through a list of files and attempts to find the patterns given.
        The patterns are translated by using the previously defined CrawlerConfig.
        :param files: List of absolute file paths
        :param patterns: List of crawler shorthands
        :return:
        """
        data = {}
        for pattern in patterns:
            data[pattern] = self.crawler_config.get_class_for_id(pattern).crawl(file)
        patterns_data = CrawlPatternsData(data)
        return patterns_data


