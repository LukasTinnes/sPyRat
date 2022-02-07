from crawling.crawler import Crawler
from crawling.crawler_data_structures.crawl_data import CrawlData
import os
from pandas import DataFrame
from multiprocessing import Pool
import itertools
from crawling.byte_array_operations import ByteArrayOperations
from typing import Tuple
import math
from typing import BinaryIO


class BMPCrawler(Crawler):
    """
    Crawls through a file to find a bmp file at each byte.
    Crawls for bmp BITMAPINFOHEADER, BITMAPINFOHEADER3 and BITMAPINFOHEADER 5.
    """

    # DIB Header Values
    BITMAPCOREHEADER = 12
    OS22XBITMAPHEADER_64 = 64
    OS22XBITMAPHEADER_16 = 16
    BITMAPINFOHEADER = 40
    BITMAPV2INFOHEADER = 52
    BITMAPV3INFOHEADER = 56
    BITMAPV4INFOHEADER = 108
    BITMAPV5INFOHEADER = 124

    # Compression Values
    BI_RGB = 0
    BI_RLE8 = 1
    BI_RLE4 = 2
    BI_BITFIELDS = 3
    BI_JPEP = 4
    BI_PNG = 5
    BI_ALPHABITFIELDS = 6
    BI_CMYK = 11
    BI_CMYKRLE8 = 12
    BI_CMYKRLE4 = 13


    # Vaidation values
    VALID = 0
    INVALID = 1
    NO_MEMORY = 2

    # For more info on how this number is derived see the graph.
    B = 2 ** 8
    mask_a = (7**2 + 7)/2/B**4/3
    mask_rgb = (1 - 1/B**4)**3/3 * ((7**2 + 7)/2/(B**4 - 1))**3
    L = 1/B**3 * (2 * mask_rgb + mask_a)
    R = 3/(2*B)**4 * (2 * mask_rgb + mask_a)
    confidence = math.log(103.5/B**6 + 3/B**4 * (L + R), 2)

    def __init__(self, pools: int, pattern: str):
        # The number of multiprocessing pools to use.
        self.pools = pools
        self.pattern = pattern

    def crawl(self, file: str) -> CrawlData:
        """
        Crawls through a file to find a file pattern at each byte.
        :param file:
        :return:
        """
        file_size_in_bytes = os.path.getsize(file)

        # Open pools to work in parallel
        with Pool(self.pools) as p:
            # The crawling ranges are divided into approx. equal sections.
            ranges = [(round(x*file_size_in_bytes/self.pools), round((x+1)*file_size_in_bytes/self.pools), file) for x in range(self.pools)]

            results = p.map(self.crawl_range, ranges)
            # Concatenate results in list
            rows = list(itertools.chain.from_iterable(results))

        df = DataFrame(rows)
        df.rename(columns={0:"start_byte", 1:"end_byte", 2: "size", 3: "confidence"}, inplace=True)
        return CrawlData(df, self.pattern)

    @staticmethod
    def crawl_range(args):
        """
        Crawls a file for BMPs in a certain range of bytes.
        :param args: Tuple of shape (start_byte, end_byte)
        :return:
        """
        # For more information see the Markdown

        # Parse args from pool back to what they were.
        start = args[0]
        end = args[1]
        file = args[2]

        rows = []
        with open(file, "rb") as f:
            for i in range(start, end):
                # Entries that are not relevant need to be excluded as quickly as possible.
                test_bytes = f.read(2)
                try:
                    header_field_string = test_bytes.decode("ASCII")
                    if not header_field_string in ["BM"]:
                        continue
                except:
                    continue
                f.seek(i)

                # The current offset from i
                index = 0

                # Parse the BMP Header
                validation, byte_offset, header_data = BMPCrawler._parse_header(f)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += byte_offset
                header_field_string, header_size, bytes_06, bytes_08, image_offset = header_data


                # Parse the DIB Header
                validation, offset, dib_data = BMPCrawler._parse_dib_header(f)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset
                dib_header_size, width, height, planes, bit_count, compression, size_img, pix_per_meter_X, pix_per_meter_Y, \
                    col_bit_count, color_important, r, g, b, a, icc_profile_data, icc_profile_size = dib_data


                # Color table
                validation, offset, color_table_data = BMPCrawler.parse_color_table(f, col_bit_count, bit_count, dib_header_size)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset


                # Deal with Gap1
                validation, offset, gap1_data = BMPCrawler.parse_gap1(f, index, image_offset)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset


                # image data
                validation, offset, image_data = BMPCrawler.parse_image_data(f, compression, bit_count, width, height, size_img)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset


                # Deal with Gap2
                validation, offset, gap2_data = BMPCrawler.parse_gap2(f, index, icc_profile_data)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset


                # ICC Profile Data
                validation, offset, icc_profile_data_block = BMPCrawler.parse_icc_profile(f, dib_header_size, icc_profile_size, icc_profile_data)
                if validation == BMPCrawler.INVALID:
                    continue
                elif validation == BMPCrawler.NO_MEMORY:
                    break
                index += offset

                # For the reasoning behind this see the graph.
                rows.append([i, i + index, index, BMPCrawler.confidence])
        return rows

    @staticmethod
    def _validate_color_table(table_bytes: bytearray) -> (bool, float):
        """
        Validates the color table
        :param table_bytes:
        :return: (Whether its valid, the probability that it was just random)
        """
        confidence = 1
        for i in range(3, len(table_bytes), 4):
            if not table_bytes[i] == 0:
                return False, 0
            # Multiply for every zero byte.
            confidence *= 1/2**8
        return True, confidence

    @staticmethod
    def _validate_info_block(planes: int, bit_count: int, compression: int, height: int) -> bool:
        """
        Validates the dib header.
        :param planes: The color planes
        :param bit_count: The bit_count for each pixel
        :param compression: The compression method
        :param height: The height of the image as defined in the BMP header
        :return:
        """
        if not planes == 1:
            return False
        if bit_count not in [1, 4, 8, 16, 24, 32]:
            return False
        if compression not in [BMPCrawler.BI_RGB, BMPCrawler.BI_RLE8, BMPCrawler.BI_RLE4, BMPCrawler.BI_BITFIELDS,
                               BMPCrawler.BI_JPEP, BMPCrawler.BI_PNG, BMPCrawler.BI_ALPHABITFIELDS, BMPCrawler.BI_CMYK,
                               BMPCrawler.BI_CMYKRLE8, BMPCrawler.BI_CMYKRLE4]:
            return False
        if compression == BMPCrawler.BI_RLE8:
            if not bit_count == 8 or not height >= 0:
                return False
        elif compression == BMPCrawler.BI_RLE4 and (not bit_count == 4 or not height >= 0):
            return False
        elif compression == BMPCrawler.BI_BITFIELDS and bit_count not in [16, 32]:
            return False
        return True

    @staticmethod
    def _validate_color_masks_rgb(r: bytes, g: bytes, b: bytes) -> bool:
        """
        Validate the rgb color masks.
        :param r: the red mask
        :param g: the green mask
        :param b: the blue mask
        :return:
        """
        if r == 0 or g == 0 or b == 0:
            return False
        are_grouped_r = ByteArrayOperations.are_bits_grouped(r, 1)
        are_grouped_g = ByteArrayOperations.are_bits_grouped(g, 1)
        are_grouped_b = ByteArrayOperations.are_bits_grouped(b, 1)

        if not are_grouped_r or not are_grouped_g or not are_grouped_b:
            return False

        return True

    @staticmethod
    def _validate_color_masks_rgba(r: bytes, g: bytes, b: bytes, a: bytes) -> bool:
        """
        Validate the rgba mask variety
        :param r: the red mask
        :param g: the green mask
        :param b: the blue mask
        :param a: the alpha mask
        :return:
        """
        if r == 0 or g == 0 or b == 0:
            return False

        are_grouped_r = ByteArrayOperations.are_bits_grouped(r, 1)
        are_grouped_g = ByteArrayOperations.are_bits_grouped(g, 1)
        are_grouped_b = ByteArrayOperations.are_bits_grouped(b, 1)
        are_grouped_a = ByteArrayOperations.are_bits_grouped(a, 1) or int.from_bytes(a, "little") == 0

        if not are_grouped_r or not are_grouped_g or not are_grouped_b or not are_grouped_a:
            return False

        return True

    @staticmethod
    def _parse_color_masks_rgb(mask_bytes: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        Parse the color masks of a bmp file.
        :param mask_bytes: The bytes containing the masks
        :return:
        """
        # Each mask is 4 bytes
        r = mask_bytes[0:4]
        g = mask_bytes[4:8]
        b = mask_bytes[8:12]
        return r, g, b

    @staticmethod
    def _parse_color_masks_rgba(mask_bytes: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Parse the color masks of a bmp file.
        :param mask_bytes: The bytes containing the masks
        :return:
        """
        # Each mask is 4 bytes
        r = mask_bytes[0:4]
        g = mask_bytes[4:8]
        b = mask_bytes[8:12]
        a = mask_bytes[12:16]
        return r, g, b, a

    @staticmethod
    def _parse_header(f: BinaryIO) -> Tuple[int, int, tuple]:
        """
        Parse header of a bmp file
        :param f: The file stream
        :return:
        """
        header_bytes = f.read(14)
        if len(header_bytes) < 14:  # Is header long enough
            return False, -1, ()

        header_field_bytes = header_bytes[0x0:0x2]
        try:
            header_field_string = header_field_bytes.decode("ASCII")
        except:
            return BMPCrawler.INVALID, -1, ()

        header_size_bytes = header_bytes[0x2:0x6]
        header_size = int.from_bytes(header_size_bytes, "little", signed=False)

        bytes_06 = header_bytes[0x6:0x8]
        bytes_08 = header_bytes[0x8:0xA]

        offset_bytes = header_bytes[0xA:0xD]
        offset = int.from_bytes(offset_bytes, "little", signed=False)

        return BMPCrawler.VALID, 14, (header_field_string, header_size, bytes_06, bytes_08, offset)

    @staticmethod
    def _parse_dib_header(f: BinaryIO) -> Tuple[int, int, tuple]:
        """
        Parse the info block of a bmp file
        :param f: The file stream
        :return:
        """
        # Deal with dib header
        dib_header_size_bytes = f.read(4)
        if len(dib_header_size_bytes) < 4:
            return BMPCrawler.NO_MEMORY, -1, ()

        dib_header_size = int.from_bytes(dib_header_size_bytes, "little", signed=False)
        if dib_header_size not in [BMPCrawler.BITMAPINFOHEADER, BMPCrawler.BITMAPCOREHEADER,
                                   BMPCrawler.OS22XBITMAPHEADER_16, BMPCrawler.OS22XBITMAPHEADER_64,
                                   BMPCrawler.BITMAPV2INFOHEADER, BMPCrawler.BITMAPV3INFOHEADER,
                                   BMPCrawler.BITMAPV4INFOHEADER, BMPCrawler.BITMAPV5INFOHEADER]:
            return BMPCrawler.INVALID, -1, ()

        if dib_header_size not in [BMPCrawler.BITMAPINFOHEADER, BMPCrawler.BITMAPV3INFOHEADER,
                                   BMPCrawler.BITMAPV5INFOHEADER]:
            print(f"WARNING! Found Unsupported BMP Type: {dib_header_size}")
            return BMPCrawler.INVALID, -1, ()
        # Not setting confidence here since this is just a class limitation.

        # Mandatory fields

        info_bytes = f.read(dib_header_size - 4)
        if len(info_bytes) < dib_header_size - 4:
            return BMPCrawler.NO_MEMORY, -1, ()

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

        valid = BMPCrawler._validate_info_block(planes, bit_count, compression, height)
        if not valid:
            return BMPCrawler.INVALID, -1, ()
        offset = dib_header_size

        # Optional fields

        r, g, b, a = None, None, None, None
        icc_profile_data, icc_profile_size = None, None

        # Deal with color Masks
        if dib_header_size == BMPCrawler.BITMAPINFOHEADER:
            if compression in [BMPCrawler.BI_BITFIELDS, BMPCrawler.BI_ALPHABITFIELDS]:
                mask_bytes = f.read(3 * 4)
                offset += 3*4
                if len(mask_bytes) < 3 * 4:
                    return BMPCrawler.NO_MEMORY, -1, ()
                r, g, b = BMPCrawler._parse_color_masks_rgb(mask_bytes)
                valid = BMPCrawler._validate_color_masks_rgb(r, g, b)
                if not valid:
                    return BMPCrawler.INVALID, -1, ()
        if dib_header_size == BMPCrawler.BITMAPV3INFOHEADER:
            if compression in [BMPCrawler.BI_BITFIELDS, BMPCrawler.BI_ALPHABITFIELDS]:
                mask_bytes = info_bytes[-4 * 4:]
                if len(mask_bytes) < 4 * 4:
                    return BMPCrawler.NO_MEMORY, -1, ()
                r, g, b, a = BMPCrawler._parse_color_masks_rgba(mask_bytes)
                valid = BMPCrawler._validate_color_masks_rgba(r, g, b, a)
                if not valid:
                    return BMPCrawler.INVALID, -1, ()
        if dib_header_size == BMPCrawler.BITMAPV5INFOHEADER:
            remaining_bytes = info_bytes[-21 * 4:]
            if compression in [BMPCrawler.BI_BITFIELDS, BMPCrawler.BI_ALPHABITFIELDS]:
                mask_bytes = remaining_bytes[:4 * 4]
                if len(mask_bytes) < 4 * 4:
                    return BMPCrawler.NO_MEMORY, -1, ()
                r, g, b, a = BMPCrawler._parse_color_masks_rgba(mask_bytes)
                valid = BMPCrawler._validate_color_masks_rgba(r, g, b, a)
                if not valid:
                    return BMPCrawler.INVALID, -1, ()

            # Parse ICC Profile
            icc_profile_data = int.from_bytes(remaining_bytes[-4 * 3:-4 * 2], "little", signed=False)
            icc_profile_size = int.from_bytes(remaining_bytes[-4 * 2:-4 * 1], "little", signed=False)

        return BMPCrawler.VALID, offset, (dib_header_size, width, height, planes, bit_count, compression, size_img,
                                          pix_per_meter_X, pix_per_meter_Y, col_bit_count, color_important,
                                          r, g, b, a, icc_profile_data, icc_profile_size)

    @staticmethod
    def parse_color_table(f: BinaryIO, col_bit_count: int, bit_count: int, dib_header_size: int) -> Tuple[int, int, tuple]:
        """
        Parses the color table.
        :param f: The file stream
        :param col_bit_count: The bitcount ´per color
        :param bit_count: The
        :param dib_header_size:
        :return:
        """
        if ((col_bit_count == 0 and bit_count in [1, 4,
                                                  8]) or not col_bit_count == 0) and dib_header_size == BMPCrawler.BITMAPINFOHEADER:
            entries = 2 ** bit_count if col_bit_count == 0 else col_bit_count
            color_table_bytes = f.read(entries * 4)  # Every entry is 4 bytes long
            if len(color_table_bytes) < entries * 4:
                return BMPCrawler.NO_MEMORY, -1, ()
            return BMPCrawler.VALID, entries*4, ()
        return BMPCrawler.VALID, 0, ()

    @staticmethod
    def parse_gap1(f: BinaryIO, current_offset: int, needed_offset: int) -> Tuple[int, int, tuple]:
        """
        Parses the first gap.
        :param f: The filestream
        :param current_offset: The offset in the file stream currently given.
        :param needed_offset:The One that it should be at, at the end of the gap.
        :return:
        """
        if not current_offset == needed_offset:
            if needed_offset < current_offset:
                return BMPCrawler.INVALID, -1, ()
            gap_bytes = f.read(needed_offset - current_offset)
            return BMPCrawler.VALID, needed_offset - current_offset, (gap_bytes,)
        return BMPCrawler.VALID, 0, (None,)

    @staticmethod
    def parse_gap2(f: BinaryIO, current_offset: int, needed_offset: int) -> Tuple[int, int, tuple]:
        """
        Parses the Seond Gap in the file.
        :param f: The filestream
        :param current_offset: The offset in the file stream currently given.
        :param needed_offset:The One that it should be at, at the end of the gap.
        :return:
        """
        if not current_offset == needed_offset and needed_offset is not None and not needed_offset == 0:
            if needed_offset < current_offset:
                return BMPCrawler.INVALID, -1, ()
            gap_bytes = f.read(needed_offset - current_offset)
            return BMPCrawler.VALID, needed_offset - current_offset, (gap_bytes,)
        return BMPCrawler.VALID, 0, (None,)

    @staticmethod
    def parse_image_data(f: BinaryIO, compression: int, bit_count: int, width: int, height: int,
                         image_data_size: int) -> Tuple[int, int, tuple]:
        """
        Parses the image data
        :param f: The filestream
        :param compression: The compression method
        :param bit_count: The bit count defined in BMP Header
        :param width: The width in pixels
        :param height: The height in rows
        :param image_data_size: The total size of the image in bytes
        :return:
        """
        actual_image_data_size = 0
        if compression == 0:
            if image_data_size == 0:
                if compression in [BMPCrawler.BI_RGB, BMPCrawler.BI_BITFIELDS]:
                    # Alright this looks strange but is the actual formula to compute how long a row is,
                    # since we need the padding.
                    row_size = int((bit_count * width + 31) / 32) * 4
                    actual_image_data_size = row_size * abs(height)

            else:
                actual_image_data_size = image_data_size
        else:
            actual_image_data_size = image_data_size

        image_data_bytes = f.read(actual_image_data_size)
        if len(image_data_bytes) < actual_image_data_size:
            return BMPCrawler.NO_MEMORY, -1, ()

        # You may notice that I am not checking if zeros are actually present as the padding.
        # I decided to omit it here because I don't think it's a hard requirement.
        return BMPCrawler.VALID, actual_image_data_size, (image_data_bytes,)

    @staticmethod
    def parse_icc_profile(f: BinaryIO, dib_header_size: int, icc_profile_size: int, icc_profile_data: int) \
            -> Tuple[int, int, tuple]:
        """
        Parses the ICC Profile
        :param f:  The files stream
        :param dib_header_size: The DIB Header size. (Just the version of BMP)
        :param icc_profile_size: The size of the icc profile in bytes
        :param icc_profile_data: The offset to the start of the ICC Profile
        :return:
        """
        if dib_header_size == BMPCrawler.BITMAPV5INFOHEADER:
            if icc_profile_size > 0:
                icc_color_profile_bytes = f.read(icc_profile_size)
                if len(icc_color_profile_bytes) < icc_profile_size:
                    return BMPCrawler.NO_MEMORY, -1, ()
                return BMPCrawler.VALID, icc_profile_data + icc_profile_size, (icc_color_profile_bytes,)
        return BMPCrawler.VALID, 0, (None,)
