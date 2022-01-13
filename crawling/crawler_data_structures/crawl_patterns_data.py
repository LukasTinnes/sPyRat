from crawling.crawler_data_structures.crawl_data import CrawlData
from typing import List
from pandas import DataFrame


class CrawlPatternsData:
    """
    Basically just a collection of Crawler Data objects.
    """

    def __init__(self, crawl_data: List[CrawlData]):
        ...

    def get_dataframe_for_pattern(self, pattern: str) -> DataFrame:
        """
        Returns the data frame, for a pattern, given a CrawlerConfig.
        :param pattern:
        :return:
        """
        ...

    def compile_dataframe_for_all(self) -> DataFrame:
        """
        Returns a data frame that concatenates ALL the frames that it holds.
        start_byte( inclusive, starts at zero), end_byte (inclusive), size (in bytes), confidence, pattern
        :return:
        """
        ...
