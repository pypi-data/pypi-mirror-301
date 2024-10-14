# automatically generated from PNG.vs2

from libvstruct2 import AS, DynExpr, Eval, I1, I4B, R, VStruct


import zlib

from .vs2_JPG import EXIF


class PNG_IHDR(VStruct):
    SFORMAT = 'IIBBBBB'
    SOFFSETS = [0, 4, 8, 9, 10, 11, 12, 13]
    ENDIANNESS = '>'
    FIELDS = [
        {'name': 'Width', 'type': I4B},
        {'name': 'Height', 'type': I4B},
        {'name': 'BitDepth', 'type': I1},
        {'name': 'ColorType', 'type': I1},
        {'name': 'CompressionMethod', 'type': I1},
        {'name': 'FilterMethod', 'type': I1},
        {'name': 'InterlaceMethod', 'type': I1},
    ]


class PNG_tEXt(VStruct):
    FIELDS = [
        {'name': 'Keyword', 'type': AS, 'maxlen': 80},
        {'name': 'Text', 'type': AS, 'length': DynExpr('$^Length - :Keyword')},
    ]


class PNG_iTXt(VStruct):
    FIELDS = [
        {'name': 'Keyword', 'type': AS, 'maxlen': 80},
        {'name': 'CompressionFlag', 'type': I1},
        {'name': 'CompressionMethod', 'type': I1},
        {'name': 'LanguageTag', 'type': AS},
        {'name': 'TranslatedKeyword', 'type': AS},
        {'name': 'Text', 'type': AS, 'length': DynExpr('$^Length - :Keyword')},
    ]


class PNG_iCCP(VStruct):
    FIELDS = [
        {'name': 'ProfileName', 'type': AS, 'maxlen': 80},
        {'name': 'CompressionMethod', 'type': I1},
        {'name': 'CompressedProfile', 'type': R, 'length': DynExpr('$^Length - :CompressionMethod - 1')},
        {'name': 'DecompressedProfile', 'flags': 2, 'expression': 'zlib.decompress($CompressedProfile)', 'type': Eval},
    ]


class PNG_pHYs(VStruct):
    SFORMAT = 'IIB'
    SOFFSETS = [0, 4, 8, 9]
    ENDIANNESS = '>'
    FIELDS = [
        {'name': 'PixelsPerUnitX', 'type': I4B},
        {'name': 'PixelsPerUnitY', 'type': I4B},
        {'name': 'UnitSpecifier', 'type': I1},
    ]


class PNG_gAMA(VStruct):
    FIELDS = [
        {'name': 'GammaX100000', 'type': I4B},
        {'name': 'Gamma', 'flags': 2, 'expression': '$GammaX100000 / 100000', 'type': Eval},
    ]


class PNGChunk(VStruct):
    FIELDS = [
        {'name': 'Length', 'type': I4B},
        {'name': 'ChunkType', 'type': R, 'length': 4},
        {'name': 'ChunkData', 'type': R, 'length': DynExpr('$Length')},
        {'name': 'Header', 'flags': 2, 'type': PNG_IHDR, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'IHDR'", 'validator': DynExpr('$^Length == 13')},
        {'name': 'Text', 'flags': 2, 'type': PNG_tEXt, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'tEXt'"},
        {'name': 'Text', 'flags': 2, 'type': PNG_iTXt, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'iTXt'"},
        {'name': 'ICCProfile', 'flags': 2, 'type': PNG_iCCP, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'iCCP'"},
        {'name': 'Exif', 'flags': 2, 'type': EXIF, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'eXIf'"},
        {'name': 'PhysPixelDimenstions', 'flags': 2, 'type': PNG_pHYs, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'pHYs'", 'validator': DynExpr('$^Length == 9')},
        {'name': 'Gamma', 'flags': 2, 'type': PNG_gAMA, 'dyn_offset': '@ChunkData', 'condition': "$ChunkType == b'gAMA'"},
        {'name': 'CRC', 'type': I4B},
    ]


class PNG(VStruct):
    ROOT = True
    FILETYPES = ('png',)
    FILTER = '^\\x89PNG\\r\\n\\x1A\\n'
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 8},
        {'name': 'Chunks', 'count': DynExpr('&data_available'), 'type': PNGChunk, 'stop': "$crt_field.ChunkType == b'IEND'"},
    ]


