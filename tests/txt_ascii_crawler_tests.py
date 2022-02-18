from crawling.crawlers.file_crawlers.text_crawlers.txt_ascii_crawler import TxtAsciiCrawler


PATH = "files\\txt\\"


def test_alphabet():
    crawler = TxtAsciiCrawler(0)
    crawl_data = crawler.crawl(PATH + "Alphabet_ascii.txt")
    frame = crawl_data.get_data_frame()
    assert frame.shape[0] == 1


def test_alphabet_broken():
    crawler = TxtAsciiCrawler(0)
    crawl_data = crawler.crawl(PATH + "Alphabet_broken_ascii.txt")
    frame = crawl_data.get_data_frame()
    assert frame.shape[0] == 2


def test_alphabet_range():
    crawler = TxtAsciiCrawler(0)
    crawl_data = crawler.crawl_in_range(PATH + "Alphabet_ascii.txt", 0, 4)
    frame = crawl_data.get_data_frame()
    assert frame.shape[0] == 1
    assert 4 == frame.iloc[0]["size"]

