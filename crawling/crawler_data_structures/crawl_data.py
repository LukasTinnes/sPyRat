from crawling.crawler import Crawler
from pandas import DataFrame


class CrawlData:
    """
    Stores the data collected from a single crawler on a single file.
    """

    def __init__(self, data_frame: DataFrame, crawler: Crawler):
        self.data_frame: DataFrame = data_frame
        self.crawler: Crawler = crawler

    def get_data_frame(self) -> DataFrame:
        """
        Returns a data frame, with rows:
        start_byte( inclusive, starts at zero), end_byte (inclusive), size (in bytes)
        :return:
        """
        return self.data_frame

    def get_pattern(self) -> Crawler:
        """
        Returns the pattern that was crawled for
        :return:
        """
        return self.crawler
