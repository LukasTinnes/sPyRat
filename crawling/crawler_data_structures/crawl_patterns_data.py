from crawling.crawler_data_structures.crawl_data import CrawlData
from crawling.crawler_config import CrawlerConfig
from typing import List
from pandas import DataFrame


class CrawlPatternsData:
    """
    Basically just a collection of Crawler Data objects.
    """

    def __init__(self, crawl_data: List[CrawlData]):
        ...

    def get_frame_for_pattern(self, pattern: str, config: CrawlerConfig) -> DataFrame:
        """
        Returns the data frame, for a pattern, given a CrawlerConfig.
        :param pattern:
        :return:
        """
        ...

    def compile_frame_for_all(self) -> DataFrame:
        """
        Returns a data frame that concatenates ALL the frames that it holds.
        :return:
        """
        ...
