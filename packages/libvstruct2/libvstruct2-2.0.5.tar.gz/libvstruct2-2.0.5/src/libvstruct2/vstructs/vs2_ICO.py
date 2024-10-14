# automatically generated from ICO.vs2

from libvstruct2 import B, D, DynExpr, I2, R, VStruct, W


from .vs2_BMP import BMP_DIB_Header
from .vs2_PNG import PNG


ICO_TYPE = {
    1:'ICO',
    2:'CUR',
    }


class ICO_Entry(VStruct):
    FIELDS = [
        {'name': 'Width', 'type': B, 'description': 'Cursor width (16, 32 or 64)'},
        {'name': 'Height', 'type': B, 'description': 'Cursor height (16, 32 or 64)'},
        {'name': 'ColorCount', 'type': B, 'description': 'Number of colors (2,16, 0=256)'},
        {'name': 'Reserved', 'type': B},
        {'name': 'Planes', 'type': W},
        {'name': 'BitCount', 'type': W, 'description': 'Bits per pixel (1, 4, 8)'},
        {'name': 'SizeInBytes', 'type': D, 'description': 'Size of (InfoHeader + ANDbitmap + XORbitmap)'},
        {'name': 'FileOffset', 'type': D, 'description': 'FilePos, where InfoHeader starts'},
        {'name': 'DataFormat', 'flags': 3, 'type': R, 'length': 4, 'dyn_offset': '$FileOffset'},
        {'name': 'Data', 'flags': 2, 'type': R, 'length': DynExpr('$SizeInBytes'), 'dyn_offset': '$FileOffset'},
        {'name': 'BMPImage', 'flags': 2, 'condition': DynExpr("$DataFormat != b'\\x89PNG'"), 'type': BMP_DIB_Header, 'dyn_offset': '$FileOffset'},
        {'name': 'PNGImage', 'flags': 2, 'condition': DynExpr("$DataFormat == b'\\x89PNG'"), 'type': PNG, 'dyn_offset': '$FileOffset'},
    ]


class ICO(VStruct):
    ROOT = True
    FILETYPES = ('ico', 'cur')
    FILTER = '^\\0\\0[\\x01\\x02]\\0'
    FIELDS = [
        {'name': 'Reserve', 'type': I2},
        {'name': 'Type', 'type': I2, 'formatter': ICO_TYPE, 'validator': [1, 2]},
        {'name': 'Count', 'type': I2, 'description': 'Number of Icons in this file'},
        {'name': 'Entries', 'count': DynExpr('$Count'), 'type': ICO_Entry, 'description': 'List of icons'},
        {'name': 'Overlay', 'type': R, 'length': True},
    ]


