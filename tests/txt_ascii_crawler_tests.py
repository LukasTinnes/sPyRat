from unittest import TestCase
from crawling.crawlers.file_crawlers.text_crawlers.txt_ascii_crawler import TxtAsciiCrawler


class TxtAsciiCrawlerTests(TestCase):

    PATH = "files\\txt\\"

    def test_alphabet(self):
        crawler = TxtAsciiCrawler(0)
        crawl_data = crawler.crawl(self.PATH + "Alphabet_ascii.txt")
        frame = crawl_data.get_data_frame()
        self.assertGreater(frame.shape[0], 0)
