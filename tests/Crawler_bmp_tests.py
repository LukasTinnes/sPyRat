from unittest import TestCase
from crawling.crawlers.file_crawlers.bmp_crawler import BMPCrawler
import time

class CrawlerBMPTests(TestCase):

    def test_simple_bmp(self):
        crawler = BMPCrawler()
        t = time.time()
        frame = crawler.crawl("files\\synth spiral.bmp")
        print(time.time()-t)
        print(frame.get_data_frame())
