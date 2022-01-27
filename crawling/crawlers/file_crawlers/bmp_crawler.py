from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool
import itertools


class BMPCrawler(Crawler):
    """
    Crawls through a file to find a bmp file at each byte.
    Crawls for bmp version 3.
    """

    POOLS = 4


    BITMAPCOREHEADER = 12
    OS22XBITMAPHEADER_64 = 64
    OS22XBITMAPHEADER_16 = 16
    BITMAPINFOHEADER = 40
    BITMAPV2INFOHEADER = 52
    BITMAPV3INFOHEADER = 56
    BITMAPV4INFOHEADER = 108
    BITMAPV5INFOHEADER = 124


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
            rows = list(itertools.chain.from_iterable(results))

        df = DataFrame(rows)
        df.rename(columns={0:"start_byte", 1:"end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, "bmp") # TODO pattern s tring

    @staticmethod
    def crawl_range(args):
        start = args[0]
        end = args[1]
        file = args[2]
        rows = []
        with open(file, "rb") as f:
            for i in range(start, end):
                test_bytes = f.read(2) # Entries that are not relevant need to be excluded as quickly as possible.
                try:
                    header_field_string = test_bytes.decode("ASCII")
                    if not header_field_string in ["BM"]:
                        continue
                except:
                    continue
                f.seek(i)

                index = 0

                # Deal with header block
                header_bytes = f.read(14)
                if len(header_bytes) < 14:  # Is header long enough
                    break
                index += 14

                header_field_string, header_size, bytes_06, bytes_08, offset = BMPCrawler._parse_header(header_bytes)

                # Deal with info block
                dib_header_size_bytes = f.read(4)
                if len(dib_header_size_bytes) < 4:
                    break
                index += 4
                dib_header_size = int.from_bytes(dib_header_size_bytes, "little", signed=False)
                if dib_header_size not in [BMPCrawler.BITMAPINFOHEADER, BMPCrawler.BITMAPCOREHEADER,
                                           BMPCrawler.OS22XBITMAPHEADER_16, BMPCrawler.OS22XBITMAPHEADER_64,
                                           BMPCrawler.BITMAPV2INFOHEADER, BMPCrawler.BITMAPV3INFOHEADER,
                                           BMPCrawler.BITMAPV4INFOHEADER, BMPCrawler.BITMAPV5INFOHEADER]:
                    continue

                if not dib_header_size in [BMPCrawler.BITMAPINFOHEADER, BMPCrawler.BITMAPV3INFOHEADER, BMPCrawler.BITMAPV5INFOHEADER]:
                    continue
                info_bytes = f.read(dib_header_size-4)
                index += dib_header_size - 4
                if len(info_bytes) < dib_header_size-4:
                    break

                width, height, planes, bit_count, compression, image_data_size, _, _, col_bit_count, _ = BMPCrawler._parse_info_block(info_bytes, dib_header_size)
                if not BMPCrawler._validate_info_block(planes, bit_count, compression, height):
                    continue


                # Deal with color Masks
                if dib_header_size == BMPCrawler.BITMAPINFOHEADER:
                    if compression in [3,6]:
                        mask_bytes = f.read(3*4)
                        index += 3*4
                        if len(mask_bytes) < 3*4:
                            break
                        r, g, b = BMPCrawler._parse_color_masks_rgb(mask_bytes)
                        if not BMPCrawler._validate_color_masks_rgb(r, g, b, col_bit_count):
                            continue
                if dib_header_size == BMPCrawler.BITMAPV3INFOHEADER:
                    if compression in [3,6]:
                        mask_bytes = info_bytes[-4*4:]
                        if len(mask_bytes) < 4*4:
                            break
                        r, g, b, a = BMPCrawler._parse_color_masks_rgba(mask_bytes)
                        if not BMPCrawler._validate_color_masks_rgba(r, g, b, a, col_bit_count):
                            continue
                if dib_header_size == BMPCrawler.BITMAPV5INFOHEADER:
                    remaining_bytes = info_bytes[-21*4:]
                    if compression in [3,6]:
                        mask_bytes = remaining_bytes[:4*4]
                        if len(mask_bytes) < 4*4:
                            break
                        r, g, b, a = BMPCrawler._parse_color_masks_rgba(mask_bytes)
                        if not BMPCrawler._validate_color_masks_rgba(r, g, b, a, col_bit_count):
                            continue
                    icc_profile_data = int.from_bytes(remaining_bytes[-4*3:-4*2], "little", signed=False)
                    icc_profile_size = int.from_bytes(remaining_bytes[-4*2:-4*1], "little", signed=False)


                # Deal with color table
                if ((col_bit_count == 0 and bit_count in [1,4,8]) or not col_bit_count ==0)and dib_header_size == BMPCrawler.BITMAPINFOHEADER:
                    entries = 2 ** bit_count if col_bit_count == 0 else col_bit_count
                    color_table_bytes = f.read(entries * 4)  # Every entry is 4 bytes long
                    if len(color_table_bytes) < entries * 4:
                        break
                    index += entries * 4


                # Deal with Gap1
                if not index == offset:
                    f.seek(i+offset)
                    index = offset


                # parse image data
                actual_image_data_size = 0
                if compression == 0:
                    if image_data_size == 0:
                        if compression in [0,3]:

                            row_size = int((bit_count * width + 31) / 32)*4
                            actual_image_data_size = row_size * abs(height)

                    else:
                        actual_image_data_size = image_data_size
                else:
                    actual_image_data_size = image_data_size

                image_data_bytes = f.read(actual_image_data_size)
                if len(image_data_bytes) < actual_image_data_size:
                    break
                index += actual_image_data_size

                # ICC Profile Data
                if dib_header_size == BMPCrawler.BITMAPV5INFOHEADER:
                    if icc_profile_size > 0:
                        f.seek(i+icc_profile_data)
                        icc_color_profile_bytes = f.read(icc_profile_size)
                        if len(icc_color_profile_bytes < icc_profile_size):
                            break
                        index = i + icc_profile_data + icc_profile_size

                rows.append([i, i + index, index, 0])
        return rows

    @staticmethod
    def _validate_color_table(table_bytes):
        # OK so it seems this is not a hard requirement and more of a suggestion. Thanks microsoft. So I am leaving this part out.
        for i in range(3, len(table_bytes), 4):
            if not table_bytes[i] == 0:
                return False
        return True

    @staticmethod
    def _validate_info_block(planes, bit_count, compression, height) -> bool:
        if not planes == 1:
            return False
        if not bit_count in [1, 4, 8, 16, 24, 32]:
            return False
        if not compression in [0, 1, 2, 3, 4, 5, 6, 11, 12, 13]:
            return False
        if compression == 1 and (not bit_count == 8 or not height >= 0):
            return False
        if compression == 2 and (not bit_count == 4 or not height >= 0):
            return False
        if compression == 3 and bit_count not in [16, 32]:
            return False
        return True

    @staticmethod
    def _validate_color_masks_rgb(r, g, b, col_bit_count) -> bool:
        r_arr = BMPCrawler.bytes_to_bit_list(r)
        g_arr = BMPCrawler.bytes_to_bit_list(g)
        b_arr = BMPCrawler.bytes_to_bit_list(b)

        # TODO Check if they NEED to be at least 1
        if not r_arr.count(1) > 0 or \
                not g_arr.count(1) > 0 or \
                not b_arr.count(1) > 0:
            return False

        crossings_r = BMPCrawler.bytes_crossings(r)
        crossings_g = BMPCrawler.bytes_crossings(g)
        crossings_b = BMPCrawler.bytes_crossings(b)

        if crossings_r > 2 or crossings_g > 2 or crossings_b > 2:
            return False

        return True

    @staticmethod
    def _validate_color_masks_rgba(r, g, b, a, col_bit_count) -> bool:
        r_arr = BMPCrawler.bytes_to_bit_list(r)
        g_arr = BMPCrawler.bytes_to_bit_list(g)
        b_arr = BMPCrawler.bytes_to_bit_list(b)
        a_arr = BMPCrawler.bytes_to_bit_list(a)

        # TODO Check if they NEED to be at least 1
        if not r_arr.count(1) > 0 or \
            not g_arr.count(1) > 0 or \
            not b_arr.count(1) > 0:
            return False

        crossings_r = BMPCrawler.bytes_crossings(r)
        crossings_g = BMPCrawler.bytes_crossings(g)
        crossings_b = BMPCrawler.bytes_crossings(b)
        crossings_a = BMPCrawler.bytes_crossings(a)

        if crossings_r > 2 or crossings_g > 2 or crossings_b > 2 or crossings_a > 2:
            return False

        return True


    @staticmethod
    def bytes_to_bit_list(bytes_obj):
        """
        Creates a list ob bits (1,0 integers) from bytes
        :param bytes_obj:
        :return:
        """
        bits = []
        for i in range(len(bytes_obj)):
            for j in range(8):
                bits.append((bytes_obj[i] >> j) % 2)
        return bits

    @staticmethod
    def bytes_crossings(bytes_obj):
        """
        Counts the number of 0,1 and 1,0 sequences.
        :param bytes_obj:
        :return:
        """
        crossings = 0
        last = -1
        for x in BMPCrawler.bytes_to_bit_list(bytes_obj):
            if last == -1:
                last = x
            else:
                if not x == last:
                    last = x
                    crossings += 1

        return crossings

    @staticmethod
    def _parse_color_masks_rgb(mask_bytes):
        """
        Parse the color masks of a bmp file.
        :param mask_bytes:
        :return:
        """
        r = mask_bytes[0:4]
        g = mask_bytes[4:8]
        b = mask_bytes[8:12]
        return r, g, b

    @staticmethod
    def _parse_color_masks_rgba(mask_bytes):
        """
        Parse the color masks of a bmp file.
        :param mask_bytes:
        :return:
        """
        r = mask_bytes[0:4]
        g = mask_bytes[4:8]
        b = mask_bytes[8:12]
        a = mask_bytes[12:16]
        return r, g, b, a

    @staticmethod
    def _parse_header(header_bytes):
        """
        Parse header of a bmp file
        :param header_bytes:
        :return:
        """
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
    def _parse_info_block(info_bytes, size):
        """
        Parse the info block of a bmp file
        :param info_bytes:
        :return:
        """
        width_bytes = info_bytes[0:4]
        width = int.from_bytes(width_bytes, "little", signed=True)

        height_bytes = info_bytes[4:8]
        height = int.from_bytes(height_bytes, "little", signed=True)

        planes_bytes = info_bytes[8:10]
        planes = int.from_bytes(planes_bytes, "little", signed=False)

        bit_count_bytes = info_bytes[10:12]
        bit_count = int.from_bytes(bit_count_bytes, "little", signed=False)

        compression_bytes = info_bytes[12:16]
        compression = int.from_bytes(compression_bytes, "little", signed=False)

        size_img_bytes = info_bytes[16:20]
        size_img = int.from_bytes(size_img_bytes, "little", signed=True)

        pix_per_meter_X_bytes = info_bytes[20:24]
        pix_per_meter_X = int.from_bytes(pix_per_meter_X_bytes, "little", signed=True)

        pix_per_meter_Y_bytes = info_bytes[24:28]
        pix_per_meter_Y = int.from_bytes(pix_per_meter_Y_bytes, "little", signed=True)

        col_bit_count_bytes = info_bytes[28:32]
        col_bit_count = int.from_bytes(col_bit_count_bytes, "little", signed=False)

        color_important_bytes = info_bytes[32:36]
        color_important = int.from_bytes(color_important_bytes, "little", signed=True)

        return width, height, planes, bit_count, compression, size_img, pix_per_meter_X, pix_per_meter_Y, \
               col_bit_count, color_important
