from unittest import TestCase
from crawling.crawlers.file_crawlers.bmp_crawler import BMPCrawler
import os


class CrawlerBMPTests(TestCase):

    PATH_PDN = "files\\bmp\\paintdotnet\\"
    PATH_GIMP = "files\\bmp\\gimp\\"

    def test_pdn_32bpp_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_32.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_32.bmp"))

    def test_pdn_24bpp_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_24.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_24.bmp"))

    def test_pdn_8bpp_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_8.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_8.bmp"))

    def test_pdn_4bpp_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_4.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_4.bmp"))

    def test_pdn_1bpp_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_1.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_1.bmp"))

    def test_gimp_R5G6B5_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R5G6B5.bmp"))

    def test_gimp_R8G8B8_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R8G8B8_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R8G8B8.bmp"))

    def test_gimp_X1R5G5B5_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP+ "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X1R5G5B5.bmp"))

    def test_gimp_X8R8G8B8_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X8R8G8B8.bmp"))


    def test_gimp_R5G6B5_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R5G6B5.bmp"))

    def test_gimp_R8G8B8_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R8G8B8_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R8G8B8.bmp"))

    def test_gimp_X1R5G5B5_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP+ "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X1R5G5B5.bmp"))

    def test_gimp_X8R8G8B8_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X8R8G8B8.bmp"))
