from pandas import DataFrame


class CrawlData:
    """
    Stores the data collected from a single crawler on a single file.
    """

    def __init__(self, data_frame: DataFrame, pattern: str):
        self.data_frame: DataFrame = data_frame
        self.pattern = pattern

    def get_data_frame(self) -> DataFrame:
        """
        Returns a data frame, with rows:
        start_byte( inclusive, starts at zero), end_byte (inclusive), size (in bytes), confidence
        :return:
        """
        return self.data_frame

    def get_pattern(self) -> str:
        """
        Returns the pattern that was crawled for
        :return:
        """
        return self.pattern
