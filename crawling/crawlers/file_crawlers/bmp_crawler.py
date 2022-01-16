from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool
import itertools


class BMPCrawler(Crawler):
    """
    Crawls through a file to find a file pattern at each byte.
    """

    POOLS = 4

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file:
        :return:
        """
        file_size_in_bytes = os.path.getsize(file)
        with Pool(self.POOLS) as p:
            ranges = [(round(x*file_size_in_bytes/self.POOLS), round((x+1)*file_size_in_bytes/self.POOLS), file) for x in range(self.POOLS)]
            print(ranges)
            results = p.map(self.crawl_range, ranges)
            rows = itertools.chain.from_iterable(results)

        df = DataFrame(rows)
        df.rename(columns={0:"start_byte", 1:"end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, "bmp") # TODO pattern string

    @staticmethod
    def crawl_range(args):
        start = args[0]
        end = args[1]
        file = args[2]
        rows = []
        with open(file, "rb") as f:
            for i in range(start, end):
                test_bytes = f.read(2)
                try:
                    header_field_string = test_bytes.decode("ASCII")
                    if not header_field_string in ["BM", "BA", "CI", "CP", "IC", "PT"]:
                        continue
                except:
                    continue

                f.seek(i)
                header_bytes = f.read(14)
                if len(header_bytes) < 14:  # Is header long enough
                    break

                header_field_string, header_size, bytes_06, bytes_08, offset = BMPCrawler._parse_header(header_bytes)
                if not header_field_string in ["BM", "BA", "CI", "CP", "IC", "PT"]:
                    continue
                # Wikipedia says that the file size is not reliable. I exclude it from consideration.

                f.seek(i + 14)
                info_bytes = f.read(40)  # Only Version 3 for now.
                if len(info_bytes) < 40:
                    break
                BMPCrawler._parse_info_block(info_bytes)

                rows.append([i, i + header_size - 1, header_size, 0])
        return rows

    @staticmethod
    def _parse_header(header_bytes):
        header_field_bytes = header_bytes[:2]
        try:
            header_field_string = header_field_bytes.decode("ASCII")
        except:
            header_field_string = None

        header_size_bytes = header_bytes[2:6]
        header_size = int.from_bytes(header_size_bytes, "little", signed=False)

        bytes_06 = header_bytes[6:8]
        bytes_08 = header_bytes[8:10]

        offset_bytes = header_bytes[10:14]
        offset = int.from_bytes(offset_bytes, "little", signed=False)

        return header_field_string, header_size, bytes_06, bytes_08, offset

    @staticmethod
    def _parse_info_block(info_bytes):
        size_bytes = info_bytes[:4]
        size = int.from_bytes(size_bytes, "little", signed=False)

        width_bytes = info_bytes[4:8]
        width = int.from_bytes(width_bytes, "little", signed=True)

        height_bytes = info_bytes[8:12]
        height = int.from_bytes(height_bytes, "little", signed=True)

        planes_bytes = info_bytes[12:14]
        planes = int.from_bytes(planes_bytes, "little", signed=False)  # Should be 1!

        bit_count_bytes = info_bytes[14:16]
        bit_count = int.from_bytes(bit_count_bytes, "little", signed=False)

        compression_bytes = info_bytes[16:20]
        compression = int.from_bytes(compression_bytes, "little", signed=False)

        size_img_bytes = info_bytes[20:24]
        size_img = int.from_bytes(size_img_bytes, "little", signed=True)
