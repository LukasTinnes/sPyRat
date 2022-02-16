from crawling.crawlers.file_crawlers.bmp.bmp_crawler import BMPCrawler
import os
import pytest


PATH_PDN = "files\\bmp\\paintdotnet\\"
PATH_PAINT = "files\\bmp\\paint\\"
PATH_GIMP = "files\\bmp\\gimp\\"
PATH_WIKI = "files\\bmp\\wiki\\"
PATH_EXTRA = "files\\bmp\\extra\\"

POOLS = 4
PATTERN = "bmp"

### PAINT.NET tests

def test_pdn_32bpp_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PDN + "4Pix_32.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PDN + "4Pix_32.bmp")


def test_pdn_24bpp_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PDN + "4Pix_24.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PDN + "4Pix_24.bmp")


def test_pdn_8bpp_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PDN + "4Pix_8.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PDN + "4Pix_8.bmp")


def test_pdn_4bpp_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PDN + "4Pix_4.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PDN + "4Pix_4.bmp")


def test_pdn_1bpp_bmp():
    """
    Ok so this is complicated.
    For some reason Paint.NET gives two bits per pixel when you select 1.
    Is there a good reason for this?
    :return:
    """
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PDN + "4Pix_1.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PDN + "4Pix_1.bmp")


# GIMP TESTS

def test_gimp_R5G6B5_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_R5G6B5.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_R5G6B5.bmp")


def test_gimp_R8G8B8_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_R8G8B8.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_R8G8B8.bmp")


def test_gimp_X1R5G5B5_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP+ "4Pix_X1R5G5B5.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_X1R5G5B5.bmp")


def test_gimp_X8R8G8B8_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_X8R8G8B8.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_X8R8G8B8.bmp")

# "Farbraum nicht mit schreiben" was selected for these.

def test_gimp_R5G6B5_no_color_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_R5G6B5_no_color.bmp")


def test_gimp_R8G8B8_no_color_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_R8G8B8_no_color.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_R8G8B8_no_color.bmp")


def test_gimp_X1R5G5B5_no_color_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP+ "4Pix_X1R5G5B5_no_color.bmp")
    assert  frame.get_data_frame().shape[0] == 1
    assert  (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_X1R5G5B5_no_color.bmp")


def test_gimp_X8R8G8B8_no_color_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_GIMP + "4Pix_X8R8G8B8_no_color.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_GIMP + "4Pix_X8R8G8B8_no_color.bmp")

# PAINT TESTS

def test_paint_1_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PAINT + "4Pix_1.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PAINT + "4Pix_1.bmp")


def test_paint_16_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PAINT + "4Pix_16.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PAINT + "4Pix_16.bmp")


def test_paint_24_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PAINT + "4Pix_24.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert frame.get_data_frame()["size"].iloc[0] == os.path.getsize(PATH_PAINT + "4Pix_24.bmp")


def test_paint_256_depth_bmp():
    """
    Ok so for some reason there is apparently a difference between saving in 24 bit and 256 color depth
    even though that should be the exact same thing????????? IT HAS A KLIOBYTE OF DATA ?????????????
    :return:
    """
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_PAINT + "4Pix_256.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_PAINT + "4Pix_256.bmp")

# Wikipedia Tests

def test_wiki_ex1_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_WIKI + "wiki_1.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_WIKI + "wiki_1.bmp")

# Misc functions test.

def test_wiki_ex1_bmp_0():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl_at_byte(PATH_WIKI + "wiki_1.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_WIKI + "wiki_1.bmp")

def test_wiki_ex1_bmp_1():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl_at_byte(PATH_WIKI + "wiki_1.bmp", 1)
    assert frame.get_data_frame().shape[0] == 0

# Slow tests


@pytest.mark.slow
def test_hd_bmp():
    crawler = BMPCrawler(POOLS, PATTERN)
    frame = crawler.crawl(PATH_EXTRA + "synth spiral.bmp")
    assert frame.get_data_frame().shape[0] == 1
    assert (frame.get_data_frame()["size"]).iloc[0] == os.path.getsize(PATH_EXTRA + "synth spiral.bmp")
