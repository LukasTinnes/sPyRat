from crawling.crawler_data_structures.crawl_patterns_data import CrawlPatternsData


class CrawlFilesData:
    """
    A data object, that holds the results of crawling for an assortment of files.
    """

    def __init__(self):
        ...

    def data_for_file(self, file: str) -> CrawlPatternsData:
        """
        Returns the
        :param file:
        :return:
        """
        ...