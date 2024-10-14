# automatically generated from zstd.vs2

from libvstruct2 import BM1, BM3, DynExpr, I4, R, VStruct


class ZST_Header(VStruct):
    FIELDS = [
        {'name': 'Magic_Number', 'type': R, 'length': 4, 'validator': b'(\xb5/\xfd'},
        {'name': 'Frame_Header_Descriptor', 'type': BM1, 'bit_map': {3: 'Dictionary_ID_flag', 4: 'Content_Checksum_flag', 32: 'Single_Segment_flag', 192: 'Frame_Content_Size_flag'}},
        {'name': 'Window_Descriptor', 'condition': DynExpr(' not &Frame_Header_Descriptor.Single_Segment_flag '), 'type': BM1, 'bit_map': {7: 'Mantissa', 248: 'Exponent'}},
        {'name': 'Dictionary_ID', 'type': R, 'length': DynExpr(' &Frame_Header_Descriptor.Dictionary_ID_flag if (&Frame_Header_Descriptor.Dictionary_ID_flag < 3) else 4')},
        {'name': 'Frame_Content_Size', 'type': R, 'length': DynExpr(' &Frame_Header_Descriptor.Single_Segment_flag or ((2 ** &Frame_Header_Descriptor.Frame_Content_Size_flag) if &Frame_Header_Descriptor.Frame_Content_Size_flag else 0)')},
    ]


class ZST_Data_Block(VStruct):
    FIELDS = [
        {'name': 'Block_Header', 'type': BM3, 'bit_map': {1: 'Last_Block', 6: 'Block_Type', 16777208: 'Block_Size'}},
        {'name': 'Block_Content', 'type': R, 'length': DynExpr(' {0: &Block_Header.Block_Size, 1: 1, 2: &Block_Header.Block_Size}[&Block_Header.Block_Type] ')},
    ]


class Zstandard(VStruct):
    ROOT = True
    FILETYPES = ('zst',)
    FILTER = '^\\x28\\xB5\\x2F\\xFD'
    FIELDS = [
        {'name': 'Header', 'type': ZST_Header},
        {'name': 'Blocks', 'count': DynExpr('*'), 'type': ZST_Data_Block, 'stop': '&crt_field.Block_Header.Last_Block'},
        {'name': 'Content_Checksum', 'condition': DynExpr(' &Header.Frame_Header_Descriptor.Content_Checksum_flag '), 'type': I4},
        {'name': 'Overlay', 'type': R, 'length': DynExpr('&bytes_left')},
    ]


