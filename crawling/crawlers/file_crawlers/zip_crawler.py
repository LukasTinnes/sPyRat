from crawling.crawler_data_structures.crawl_data import CrawlData
from crawling.crawlers.file_crawler import FileCrawler


class ZIPCrawler(FileCrawler):

    def __init__(self, pattern: str):
        self.pattern = pattern

    def crawl(self, file: str) -> CrawlData:
        rows = self.crawl_range([0, 100, file])
        return rows

    def crawl_range(self, args):
        start_byte = args[0]
        end_byte = args[1]
        file = args[2]
        with open(file) as f:
            for i in range(start_byte, end_byte):
                f.seek(i)
                local_file_header_bytes = f.read(4)
                local_file_header = int.from_bytes(local_file_header_bytes, "little")
                if not local_file_header == 0x04034b50:
                    continue
                f.seek(i)
                if not self.crawl_zip(f):
                    continue

    def crawl_zip(self, f):
        local_file_header_bytes = f.read(4)
        local_file_header = int.from_bytes(local_file_header_bytes, "little")
        if local_file_header == 0x04034b50:
            self.crawl_local_file_header(f)

    def crawl_local_file_header(self, f):
        local_file_header_bytes = f.read(30)

        version_bytes = local_file_header_bytes[4:6]

        bit_flag_bytes = local_file_header_bytes[6:8]

        compression_bytes = local_file_header_bytes[8:10]

        last_mod_time_bytes = local_file_header_bytes[10:12]

        last_mod_date_bytes = local_file_header_bytes[12:14]

        crc_32_bytes = local_file_header_bytes[14:18]

        compressed_size_bytes = local_file_header_bytes[18:22]

        uncompressed_size_bytes = local_file_header_bytes[22:26]

        file_name_length_bytes = local_file_header_bytes[26:28]

        extra_name_length_bytes = local_file_header_bytes[28:30]




