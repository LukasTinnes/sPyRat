from pandas import DataFrame  # Pandas Dataframe

from crawling.crawlers.file_crawlers.png_crawler import PNGCrawler


def test_png_crawler_ball():
    png_crawler = PNGCrawler()
    data_frame = png_crawler.crawl("../files/png/football_seal.png").data_frame
    target = DataFrame([[1, 50462, 50461, 0]])
    target.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
    assert target.equals(data_frame)


def test_fouroclocks():
    png_crawler = PNGCrawler()
    data_frame = png_crawler.crawl("../files/png/fouroclocks.png").data_frame
    target = DataFrame([[1, 499874, 499873, 0]])
    target.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
    assert target.equals(data_frame)


def test_fractal_tree():
    png_crawler = PNGCrawler()
    data_frame = png_crawler.crawl("../files/png/fractal_tree.png").data_frame
    target = DataFrame([[1, 8498176, 8498175, 0]])
    target.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
    assert target.equals(data_frame)
