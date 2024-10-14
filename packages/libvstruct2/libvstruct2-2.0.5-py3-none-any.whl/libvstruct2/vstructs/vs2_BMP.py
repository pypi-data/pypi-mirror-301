# automatically generated from BMP.vs2

from libvstruct2 import B, DynExpr, F4, I2, I4, R, SI4, VStruct


BMP_COMPRESSION = {
    0:'BI_RGB',
    1:'BI_RLE8',
    2:'BI_RLE4',
    3:'BI_BITFIELDS',
    4:'BI_JPEG',
    5:'BI_PNG',
    6:'BI_ALPHABITFIELDS',
    }


class BITMAPFILEHEADER(VStruct):
    FIELDS = [
        {'name': 'bfType', 'type': R, 'length': 2, 'validator': b'BM'},
        {'name': 'bfSize', 'type': I4},
        {'name': 'bfReserved1', 'type': I2, 'should_be': 0},
        {'name': 'bfReserved2', 'type': I2, 'should_be': 0},
        {'name': 'bfOffBits', 'type': I4},
    ]


class BITMAPCOREHEADER(VStruct):
    SFORMAT = 'IHHHH'
    SOFFSETS = [0, 4, 6, 8, 10, 12]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'bcSize', 'type': I4},
        {'name': 'bcWidth', 'type': I2},
        {'name': 'bcHeight', 'type': I2},
        {'name': 'bcPlanes', 'type': I2},
        {'name': 'bcBitCount', 'type': I2},
    ]


class RGBTRIPLE(VStruct):
    SFORMAT = 'BBB'
    SOFFSETS = [0, 1, 2, 3]
    FIELDS = [
        {'name': 'rgbtBlue', 'type': B},
        {'name': 'rgbtGreen', 'type': B},
        {'name': 'rgbtRed', 'type': B},
    ]


class BITMAPCOREINFO(VStruct):
    FIELDS = [
        {'name': 'bmciHeader', 'type': BITMAPCOREHEADER},
        {'name': 'bmciColors', 'count': DynExpr('(1 << $bmciHeader.bcBitCount) if $bmciHeader.bcBitCount < 16 else 0'), 'type': RGBTRIPLE},
    ]


class BITMAPINFOHEADER(VStruct):
    SFORMAT = 'IiiHHIIiiII'
    SOFFSETS = [0, 4, 8, 12, 14, 16, 20, 24, 28, 32, 36, 40]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'biSize', 'type': I4},
        {'name': 'biWidth', 'type': SI4},
        {'name': 'biHeight', 'type': SI4},
        {'name': 'biPlanes', 'type': I2},
        {'name': 'biBitCount', 'type': I2},
        {'name': 'biCompression', 'type': I4, 'formatter': BMP_COMPRESSION},
        {'name': 'biSizeImage', 'type': I4},
        {'name': 'biXPelsPerMeter', 'type': SI4},
        {'name': 'biYPelsPerMeter', 'type': SI4},
        {'name': 'biClrUsed', 'type': I4},
        {'name': 'biClrImportant', 'type': I4},
    ]


class RGBQUAD(VStruct):
    SFORMAT = 'BBBB'
    SOFFSETS = [0, 1, 2, 3, 4]
    FIELDS = [
        {'name': 'rgbBlue', 'type': B},
        {'name': 'rgbGreen', 'type': B},
        {'name': 'rgbRed', 'type': B},
        {'name': 'rgbReserved', 'type': B},
    ]


class BITMAPINFO(VStruct):
    FIELDS = [
        {'name': 'bmiHeader', 'type': BITMAPINFOHEADER},
        {'name': 'bmiColors', 'count': DynExpr('(1 << $bmiHeader.biBitCount) if $bmiHeader.biBitCount < 16 else 0'), 'type': RGBQUAD},
    ]


class CIEXYZ(VStruct):
    SFORMAT = 'fff'
    SOFFSETS = [0, 4, 8, 12]
    FIELDS = [
        {'name': 'ciexyzX', 'type': F4},
        {'name': 'ciexyzY', 'type': F4},
        {'name': 'ciexyzZ', 'type': F4},
    ]


class CIEXYZTRIPLE(VStruct):
    FIELDS = [
        {'name': 'ciexyzRed', 'type': CIEXYZ},
        {'name': 'ciexyzGreen', 'type': CIEXYZ},
        {'name': 'ciexyzBlue', 'type': CIEXYZ},
    ]


class BITMAPV4HEADER(VStruct):
    FIELDS = [
        {'name': 'bV4Size', 'type': I4},
        {'name': 'bV4Width', 'type': SI4},
        {'name': 'bV4Height', 'type': SI4},
        {'name': 'bV4Planes', 'type': I2},
        {'name': 'bV4BitCount', 'type': I2},
        {'name': 'bV4V4Compression', 'type': I4, 'formatter': BMP_COMPRESSION},
        {'name': 'bV4SizeImage', 'type': I4},
        {'name': 'bV4XPelsPerMeter', 'type': SI4},
        {'name': 'bV4YPelsPerMeter', 'type': SI4},
        {'name': 'bV4ClrUsed', 'type': I4},
        {'name': 'bV4ClrImportant', 'type': I4},
        {'name': 'bV4RedMask', 'type': I4},
        {'name': 'bV4GreenMask', 'type': I4},
        {'name': 'bV4BlueMask', 'type': I4},
        {'name': 'bV4AlphaMask', 'type': I4},
        {'name': 'bV4CSType', 'type': I4},
        {'name': 'bV4Endpoints', 'type': CIEXYZTRIPLE},
        {'name': 'bV4GammaRed', 'type': I4},
        {'name': 'bV4GammaGreen', 'type': I4},
        {'name': 'bV4GammaBlue', 'type': I4},
    ]


class BITMAPV4INFO(VStruct):
    FIELDS = [
        {'name': 'bmiHeader', 'type': BITMAPV4HEADER},
        {'name': 'bmiColors', 'count': DynExpr('(1 << $bmiHeader.bV4BitCount) if $bmiHeader.bV4BitCount < 16 else 0'), 'type': RGBQUAD},
    ]


class BITMAPV5HEADER(VStruct):
    FIELDS = [
        {'name': 'bV5Size', 'type': I4},
        {'name': 'bV5Width', 'type': SI4},
        {'name': 'bV5Height', 'type': SI4},
        {'name': 'bV5Planes', 'type': I2},
        {'name': 'bV5BitCount', 'type': I2},
        {'name': 'bV5Compression', 'type': I4, 'formatter': BMP_COMPRESSION},
        {'name': 'bV5SizeImage', 'type': I4},
        {'name': 'bV5XPelsPerMeter', 'type': SI4},
        {'name': 'bV5YPelsPerMeter', 'type': SI4},
        {'name': 'bV5ClrUsed', 'type': I4},
        {'name': 'bV5ClrImportant', 'type': I4},
        {'name': 'bV5RedMask', 'type': I4},
        {'name': 'bV5GreenMask', 'type': I4},
        {'name': 'bV5BlueMask', 'type': I4},
        {'name': 'bV5AlphaMask', 'type': I4},
        {'name': 'bV5CSType', 'type': I4},
        {'name': 'bV5Endpoints', 'type': CIEXYZTRIPLE},
        {'name': 'bV5GammaRed', 'type': I4},
        {'name': 'bV5GammaGreen', 'type': I4},
        {'name': 'bV5GammaBlue', 'type': I4},
        {'name': 'bV5Intent', 'type': I4},
        {'name': 'bV5ProfileData', 'type': I4},
        {'name': 'bV5ProfileSize', 'type': I4},
        {'name': 'bV5Reserved', 'type': I4},
    ]


class BITMAPV5INFO(VStruct):
    FIELDS = [
        {'name': 'bmiHeader', 'type': BITMAPV5HEADER},
        {'name': 'bmiColors', 'count': DynExpr('(1 << $bmiHeader.bV5BitCount) if $bmiHeader.bV5BitCount < 16 else 0'), 'type': RGBQUAD},
    ]


class BMP_DIB_Header(VStruct):
    FIELDS = [
        {'name': 'next_hdr', 'flags': 3, 'type': I4, 'validator': (12, 40, 108, 124)},
        {'name': 'bminfoV2', 'condition': DynExpr('$next_hdr == 12'), 'type': BITMAPCOREINFO, 'alias': 'bminfo'},
        {'name': 'bminfoV3', 'condition': DynExpr('$next_hdr == 40'), 'type': BITMAPINFO, 'alias': 'bminfo'},
        {'name': 'bminfoV4', 'condition': DynExpr('$next_hdr == 108'), 'type': BITMAPV4INFO, 'alias': 'bminfo'},
        {'name': 'bminfoV5', 'condition': DynExpr('$next_hdr == 124'), 'type': BITMAPV5INFO, 'alias': 'bminfo'},
    ]


class BMP(VStruct):
    ROOT = True
    FILETYPES = ('bmp',)
    FILTER = '^BM'
    FIELDS = [
        {'name': 'fileheader', 'type': BITMAPFILEHEADER},
        {'name': 'DIB', 'type': BMP_DIB_Header},
        {'name': 'imagedata', 'flags': 2, 'type': R, 'length': DynExpr('&bytes_left'), 'dyn_offset': '$fileheader.bfOffBits'},
    ]


