from abc import abstractmethod
from crawling.crawler_data_structures.crawl_data import CrawlData


class Crawler:
    """
    An abstract class for other Crawlers to inherit from.
    A Crawler should open a given file and attempt to find an associated file pattern at every byte in the given file.
    """

    @abstractmethod
    def crawl(self, file: str) -> CrawlData:
        """
        Crawls a file to find a certain file pattern at every byte.
        :param file: The file path
        :return:
        """
        ...

    @abstractmethod
    def crawl_in_range(self, file: str, start_byte: int, end_byte: int) -> CrawlData:
        """
        Crawls the file for a file pattern between the start byte (inclusive) and the end_byte (exclusive).
        :param file: Tjhe file path
        :param start_byte: The byte to start crawling at.
        :param end_byte: The byte to end crawling at.
        :return:
        """
        ...

    @abstractmethod
    def crawl_at_byte(self, file:str, start_byte: int = 0) -> CrawlData:
        """
        Crawls for a file pattern at the specific byte given.
        :param file: The filepath.
        :param start_byte: The byte to start crawling at.
        :return:
        """
        ...
