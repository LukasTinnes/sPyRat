from crawling.crawlers.byte_crawler import ByteCrawler


PATH = "files\\bytes\\"


def test_alphabet():
    crawler = ByteCrawler(0, elements = [0,1,2,3,4,5,6,7,8,9,10,11])
    crawl_data = crawler.crawl(PATH + "10.b")
    frame = crawl_data.get_data_frame()
    assert frame.shape[0] == 1


def test_alphabet_broken():
    crawler = ByteCrawler(0, elements = [0,9])
    crawl_data = crawler.crawl(PATH + "10.b")
    frame = crawl_data.get_data_frame()
    assert frame.shape[0] == 2

