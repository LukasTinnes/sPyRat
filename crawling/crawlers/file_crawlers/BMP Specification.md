#BMP Specification

Note this specification is about validation. It will only instruct on interpretation as much as necessary.
BMPs can be divided into the following sections.

Index:
1. BMP Header
2. DIB Header
3. Color Table
4. GAP1
5. Image Data
6. GAP2
7. ICC Color Profile

## BMP Header

| Offset | Size | Name | Description |
|--------|------|------|-------------|
| 0x00 | 2 | Signature | Needs to be exactly "BM"|
| 0x02 | 4 | File Size | Is unreliable can be ignored |
| 0x06 | 2 | Reserved1 | variable |
| 0x08 | 2 | Reserved2 | variable |
| 0x0A | 4 | Files Offset to PixelArray | Offset to Image Data |

## DIB Header

| Offset | Size | Name | Description | Optionality |
|--------|------|------|-------------|-------------|
| 0x00 | 4 | DIB Header Size | Determines the Version of the BMP | Not Optional |
| 0x04 | 4 | Image width | Number of pixels in a row | Not Optional |
| 0x08 | 4 | Image Height | Number of rows | Not Optional |
| 0x0C | 2 | Planes | Must be 1 | Not Optional |
| 0x0E | 2 | Bits Per Pixel | As it says | Not Optional |
| 0x10 | 4 | Compression | | Not Optional |
| 0x14 | 4 | Image Size | | Not Optional |
| 0x18 | 4 | X Pixels Per Meter | | Not Optional |
| 0x22 | 4 | Y Pixels Per Meter | | Not Optional |
| 0x26 | 4 | Colors in Color Table | | Not Optional |
| 0x2A | 4 | Important Color Count | | Not Optional |
| 0x2E | 4 | Red channel bitmasl | | Optional |
| 0x32 | 4 | Green channel bitmasl | | Optional |
| 0x36 | 4 | Blue channel bitmasl | | Optional |
| 0x3A | 4 | Alpha channel bitmasl | | Optional |
| 0x3E | 4 | Color Space Type | | Optional |
| 0x42 | 4 | Color Space Endpoints | | Optional |
| 0x46 | 4 | Gamma for Red channel | | Optional |
| 0x4A | 4 | Gamma for Green channel | | Optional |
| 0x4E | 4 | Gamma for Blue channel | | Optional |
| 0x52 | 4 | Intent | | Optional |
| 0x56 | 4 | ICC Profile Data | | Optional |
| 0x5A | 4 | ICC Profile Size | | Optional |
| 0x5E | 4 | Reserved | Rserved, not important| Optional |

## Color Table

## GAP1
The Gap between color table and image data. 
Determined by the given image data offset in the header.


## Image Data
You would think that image data is just bit count * width * height but no,
rows NEED to be padded to be a multiple of a DWORD.
The Formula for row size is then given as row size = round down((bit_count * width + 31) / 32) * 4

## GAP2
The Gap between image data and ICC Color Profile. 
Determined by the given image data offset in the DIB Header.

## ICC Color Profile


