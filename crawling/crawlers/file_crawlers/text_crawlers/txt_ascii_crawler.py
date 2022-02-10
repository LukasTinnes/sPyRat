from crawling.crawlers.file_crawler import FileCrawler
from crawling.crawlers.byte_crawler import ByteCrawler
from crawling.crawler_data_structures.crawl_data import CrawlData


class TxtAsciiCrawler(FileCrawler):
    """
    Crawls for a subset of ASCII chars. Namely all that are used in normal text and whitespace.
    """

    CHARACTERS = list(range(33, 127))  # Contains all written characters that are not whitespace
    WHITESPACE = [9, 10, 11, 13, 32]  # In sequence: HT (TAB), LF (Linebreak), VT (TAB), CR (Linebreak), SP (Space)

    def __init__(self, min_size=0, pattern="ascii.txt"):
        """
        :param min_size: The minimal size of a string to find.
        """
        self.min_size = min_size
        self.byte_crawler = ByteCrawler(self.min_size, self.CHARACTERS + self.WHITESPACE, pattern)

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find ascii char sequences at each byte.
        :param file: The file path
        :return:
        """
        return self.byte_crawler.crawl(file)
