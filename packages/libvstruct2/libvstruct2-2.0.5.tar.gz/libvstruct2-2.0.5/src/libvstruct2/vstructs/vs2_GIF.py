# automatically generated from GIF.vs2

from libvstruct2 import BM1, DynExpr, Eval, I1, I2, R, VStruct


class RGB(VStruct):
    FIELDS = [
        {'name': 'RGB', 'type': R, 'length': 3},
    ]


class GIF_CT(VStruct):
    FIELDS = [
        {'name': 'Colors', 'count': DynExpr('2 ** (&^Fields.SizeOfCT + 1)'), 'type': RGB},
    ]


class GIF_SubBlockChunk(VStruct):
    FIELDS = [
        {'name': 'Size', 'type': I1},
        {'name': 'Data', 'type': R, 'length': DynExpr('$Size')},
    ]


class GIF_SubBlock(VStruct):
    FIELDS = [
        {'name': 'Chunks', 'flags': 1, 'count': DynExpr('*'), 'type': GIF_SubBlockChunk, 'stop': '$crt_field.Size == 0'},
        {'name': 'Data', 'flags': 2, 'expression': "b''.join(e.Data.value for e in &Chunks)", 'type': Eval},
    ]


class GIF_ImageData(VStruct):
    FIELDS = [
        {'name': 'LZWMinCodeSize', 'type': I1},
        {'name': 'ImageData', 'type': GIF_SubBlock},
    ]


class GIF_ImageDescriptor(VStruct):
    FIELDS = [
        {'name': 'Left', 'type': I2},
        {'name': 'Top', 'type': I2},
        {'name': 'Width', 'type': I2},
        {'name': 'Height', 'type': I2},
        {'name': 'Fields', 'type': BM1, 'bit_map': {128: 'HasLCT', 64: 'Interlaced', 32: 'CTIsSorted', 24: 'Reserved', 7: 'SizeOfCT'}},
        {'name': 'ImageData', 'type': GIF_ImageData},
    ]


class GIF_GraphicControlExt(VStruct):
    SFORMAT = 'BBHBB'
    SOFFSETS = [0, 1, 2, 4, 5, 6]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'BlockSize', 'type': I1},
        {'name': 'Fields', 'type': BM1, 'bit_map': {224: 'Reserved', 28: 'DisposalMethod', 2: 'UserInputFlag', 1: 'TransparentColFlg'}},
        {'name': 'DelayTime', 'type': I2},
        {'name': 'TransparentColIdx', 'type': I1},
        {'name': 'BlockTerm', 'type': I1, 'validator': 0},
    ]


class GIF_CommentExt(VStruct):
    FIELDS = [
        {'name': 'Comment', 'type': GIF_SubBlock},
    ]


class GIF_PlainTextExt(VStruct):
    FIELDS = [
        {'name': 'Size', 'type': I1},
        {'name': 'Left', 'type': I2},
        {'name': 'Top', 'type': I2},
        {'name': 'Width', 'type': I2},
        {'name': 'Height', 'type': I2},
        {'name': 'ChrCellWidth', 'type': I1},
        {'name': 'ChrCellHeight', 'type': I1},
        {'name': 'TxtFgColIdx', 'type': I1},
        {'name': 'TxtBgColIdx', 'type': I1},
        {'name': 'Text', 'type': GIF_SubBlock},
    ]


class GIF_ApplicationExt(VStruct):
    FIELDS = [
        {'name': 'Size', 'type': I1},
        {'name': 'AppId', 'type': R, 'length': 8},
        {'name': 'AppAuthCode', 'type': R, 'length': 3},
        {'name': 'AppData', 'type': GIF_SubBlock},
    ]


class GIF_Block(VStruct):
    FIELDS = [
        {'name': 'Separator', 'type': R, 'length': 1},
        {'name': 'GCLabel', 'condition': DynExpr(" $Separator == b'!' "), 'type': I1},
        {'name': 'GraphicControl', 'condition': DynExpr(" $Separator == b'!' and $GCLabel == 0xF9 "), 'type': GIF_GraphicControlExt},
        {'name': 'Comment', 'condition': DynExpr(" $Separator == b'!' and $GCLabel == 0xFE "), 'type': GIF_CommentExt},
        {'name': 'PlainText', 'condition': DynExpr(" $Separator == b'!' and $GCLabel == 0x01 "), 'type': GIF_PlainTextExt},
        {'name': 'Application', 'condition': DynExpr(" $Separator == b'!' and $GCLabel == 0xFF "), 'type': GIF_ApplicationExt},
        {'name': 'ImageDescriptor', 'condition': DynExpr(" $Separator == b',' "), 'type': GIF_ImageDescriptor},
    ]


class GIF_Header(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 3, 'validator': b'GIF'},
        {'name': 'Version', 'type': R, 'length': 3, 'validator': (b'87a', b'89a')},
        {'name': 'Width', 'type': I2},
        {'name': 'Height', 'type': I2},
        {'name': 'Fields', 'type': BM1, 'bit_map': {128: 'HasGCT', 112: 'ColorRes', 8: 'CTIsSorted', 7: 'SizeOfCT'}},
        {'name': 'BgColor', 'type': I1},
        {'name': 'PxAspectRatio', 'type': I1},
        {'name': 'GCT', 'type': GIF_CT},
    ]


class GIF(VStruct):
    ROOT = True
    FILETYPES = ('gif',)
    FILTER = '^GIF8[79]'
    FIELDS = [
        {'name': 'Header', 'type': GIF_Header},
        {'name': 'Blocks', 'count': DynExpr('*'), 'type': GIF_Block, 'stop': "&crt_field.Separator == b';'"},
        {'name': 'Trailer', 'type': R, 'length': 1, 'should_be': b';'},
    ]


