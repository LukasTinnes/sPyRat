from unittest import TestCase
from crawling.crawlers.file_crawlers.bmp_crawler import BMPCrawler


class CrawlerBMPTests(TestCase):

    def test_simple_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl("files\\4Pix.bmp")
        print(frame.get_data_frame())
