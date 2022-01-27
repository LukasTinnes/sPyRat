from unittest import TestCase
from crawling.crawlers.file_crawlers.bmp_crawler import BMPCrawler
import os


class CrawlerBMPTests(TestCase):

    PATH_PDN = "files\\bmp\\paintdotnet\\"
    PATH_PAINT = "files\\bmp\\paint\\"
    PATH_GIMP = "files\\bmp\\gimp\\"
    PATH_WIKI = "files\\bmp\\wiki\\"

    ### PAINT.NET tests

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
        """
        Ok so this is complicated.
        For some reason Paint.NET gives two bits per pixel when you select 1.
        Is there a good reason for this?
        :return:
        """
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PDN + "4Pix_1.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_PDN + "4Pix_1.bmp"))


    # GIMP TESTS

    def test_gimp_R5G6B5_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R5G6B5.bmp"))

    def test_gimp_R8G8B8_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R8G8B8.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R8G8B8.bmp"))

    def test_gimp_X1R5G5B5_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP+ "4Pix_X1R5G5B5.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X1R5G5B5.bmp"))

    def test_gimp_X8R8G8B8_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_X8R8G8B8.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X8R8G8B8.bmp"))

    # "Farbraum nicht mit schreiben" was selected for these.

    def test_gimp_R5G6B5_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R5G6B5_no_color.bmp"))

    def test_gimp_R8G8B8_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_R8G8B8_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_R8G8B8_no_color.bmp"))

    def test_gimp_X1R5G5B5_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP+ "4Pix_X1R5G5B5_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X1R5G5B5_no_color.bmp"))

    def test_gimp_X8R8G8B8_no_color_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_GIMP + "4Pix_X8R8G8B8_no_color.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0], os.path.getsize(self.PATH_GIMP + "4Pix_X8R8G8B8_no_color.bmp"))

    # PAINT TESTS

    def test_paint_1_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PAINT + "4Pix_1.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0],
                          os.path.getsize(self.PATH_PAINT + "4Pix_1.bmp"))

    def test_paint_16_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PAINT + "4Pix_16.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0],
                          os.path.getsize(self.PATH_PAINT + "4Pix_16.bmp"))

    def test_paint_24_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PAINT + "4Pix_24.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0],
                          os.path.getsize(self.PATH_PAINT + "4Pix_24.bmp"))

    def test_paint_256_depth_bmp(self):
        """
        Ok so for some reason there is apparently a difference between saving in 24 bit and 256 color depth
        even though that should be the exact same thing????????? IT HAS A KLIOBYTE OF DATA ?????????????
        :return:
        """
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_PAINT + "4Pix_256.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0],
                          os.path.getsize(self.PATH_PAINT + "4Pix_256.bmp"))

    # Wikipedia Tests

    def test_wiki_ex1_bmp(self):
        crawler = BMPCrawler()
        frame = crawler.crawl(self.PATH_WIKI + "wiki_1.bmp")
        self.assertEquals(frame.get_data_frame().shape[0], 1)
        self.assertEquals((frame.get_data_frame()["size"]).iloc[0],
                          os.path.getsize(self.PATH_WIKI + "wiki_1.bmp"))
