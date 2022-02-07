from pandas import DataFrame # Pandas Dataframe

from crawling.crawlers.file_crawlers.png_crawler import PNGCrawler


def test_png_crawler_ball():
    png_crawler = PNGCrawler()
    data_frame = png_crawler.crawl("../files/png/football_seal.png")
    target = DataFrame([])
    target.rename(columns={0: "start_byte", 1: "end_byte", 2: "size", 3: "confidence"}, inplace=True)
    assert target.equals(data_frame)
