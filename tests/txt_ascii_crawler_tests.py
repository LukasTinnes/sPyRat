from unittest import TestCase
from crawling.crawlers.txt_ascii_crawler import TxtAsciiCrawler


class TxtAsciiCrawlerTests(TestCase):

    PATH = "files\\txt\\"

    def test_alphabet(self):
        crawler = TxtAsciiCrawler(0)
        crawl_data = crawler.crawl(self.PATH + "Alphabet_ascii.txt")
        frame = crawl_data.get_data_frame()
        print(frame["confidence"])
        self.assertGreater(frame.shape[0], 0)

    def test(self):
        crawler = TxtAsciiCrawler(5)
        crawl_data = crawler.crawl("files\\machina.mfx")
        frame = crawl_data.get_data_frame()
        frame.to_csv("yee.csv")
        self.assertGreater(frame.shape[0], 0)
