from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame


class BMPCrawler(Crawler):
    """
    Crawls through a file to find a file pattern at each byte.
    """

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file:
        :return:
        """
        file_size_in_bytes = os.path.getsize(file)
        rows = []
        with open(file, "rb") as f:
            for i in range(file_size_in_bytes):
                f.seek(i)
                header_bytes = f.read(14)
                if len(header_bytes) < 14:  # Is header long enough
                    continue

                header_field_string, header_size, bytes_06, bytes_08, offset = self._parse_header(header_bytes)
                if not header_field_string in ["BM", "BA", "CI", "CP", "IC", "PT"]:
                    continue
                if i+header_size > file_size_in_bytes:
                    continue
                rows.append([i, i + header_size-1, header_size, 0])

        df = DataFrame(rows)
        df.rename(columns={0:"start_byte", 1:"end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, "bmp") # TODO pattern string


    def _parse_header(self, header_bytes):
        header_field_bytes = header_bytes[:2]
        try:
            header_field_string = header_field_bytes.decode("ASCII")
        except:
            header_field_string = None

        header_size_bytes = header_bytes[2:6]
        header_size = int.from_bytes(header_size_bytes, "little")

        bytes_06 = header_bytes[6:8]
        bytes_08 = header_bytes[8:10]

        offset_bytes = header_bytes[10:14]
        offset = int.from_bytes(offset_bytes, "little")

        return header_field_string, header_size, bytes_06, bytes_08, offset

