from crawling.crawler_data_structures.crawl_data import CrawlData
from typing import Dict
from pandas import DataFrame
import pandas


class CrawlPatternsData:
    """
    Basically just a collection of Crawler Data objects.
    """

    def __init__(self, crawl_data: Dict[str, CrawlData]):
        self.crawl_data = crawl_data

    def get_dataframe_for_pattern(self, pattern: str) -> DataFrame:
        """
        Returns the data frame, for a pattern, given a CrawlerConfig.
        :param pattern:
        :return:
        """
        crawl_data = self.crawl_data[pattern]
        df = crawl_data.get_data_frame()
        df["file_type"] = crawl_data.get_pattern()
        return self.crawl_data[pattern].get_data_frame()

    def compile_dataframe_for_all(self) -> DataFrame:
        """
        Returns a data frame that concatenates ALL the frames that it holds.
        start_byte( inclusive, starts at zero), end_byte (inclusive), size (in bytes), confidence, pattern
        :return:
        """
        frames = []
        for k, v in self.crawl_data:
            data = self.crawl_data[k]
            df = data.get_data_frame()
            df["file_type"] = v
            frames.append(df)
        concat_df = pandas.concat(frames)
        return concat_df
