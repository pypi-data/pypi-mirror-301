# automatically generated from PDF.vs2

from libvstruct2 import DynExpr, IS, R, RX, SRX, T, VStruct


import re
class PDF_List(VStruct):
    FIELDS = [
        {'name': 'Start', 'flags': 1, 'type': T, 'regex': re.compile(b'\\s*(\\[)\\s*')},
        {'name': 'Values', 'count': True, 'type': 'PDF_Value', 'stop': '/\\]/'},
        {'name': 'End', 'flags': 1, 'type': T, 'regex': re.compile(b'\\s*(\\])\\s*')},
    ]


class PDF_Value(VStruct):
    FIELDS = [
        {'name': 'String', 'type': SRX, 'regex': re.compile(b'^\\s*/(\\w+)\\s*')},
        {'name': 'Object', 'condition': DynExpr('/^<</'), 'type': 'PDF_Object'},
        {'name': 'Reference', 'type': SRX, 'post_parse_value': (int, int), 'regex': re.compile(b'^(\\d+)\\s+(\\d+)\\s+R\\s*')},
        {'name': 'Number', 'type': IS},
        {'name': 'List', 'condition': DynExpr('/^\\[\\s+/'), 'type': PDF_List},
    ]


class PDF_Attribute(VStruct):
    FIELDS = [
        {'name': 'Name', 'type': SRX, 'regex': re.compile(b'/(\\w+)\\s+')},
        {'name': 'Value', 'type': PDF_Value},
    ]


class PDF_Object(VStruct):
    FIELDS = [
        {'name': 'Marker1', 'flags': 4, 'type': T, 'regex': re.compile(b'\\s*(<<)\\s*')},
        {'name': 'Attribute', 'count': DynExpr('/^\\s*/\\w/'), 'type': PDF_Attribute},
        {'name': 'Marker2', 'flags': 4, 'type': T, 'regex': re.compile(b'\\s*(>>)\\s*')},
    ]


class PDF_Trailer(VStruct):
    FIELDS = [
        {'name': 'Marker', 'type': T, 'regex': re.compile(b'\\s*(trailer)\\s*')},
        {'name': 'Object', 'type': PDF_Object},
    ]


class PDF_Stream(VStruct):
    FIELDS = [
        {'name': 'Start', 'type': SRX, 'regex': re.compile(b'^\\s*stream[\\r\\n]+')},
        {'name': 'Data', 'type': R, 'maxlen': DynExpr('@/endstream/f - &crt_offset')},
        {'name': 'End', 'type': T, 'maxlen': -1, 'regex': re.compile(b'\\s*(endstream)\\s*')},
    ]


class PDF_HeaderObject(VStruct):
    FIELDS = [
        {'name': 'Header', 'type': RX, 'post_parse_value': (int, int), 'regex': re.compile(b'(\\d+)[ \\t]+(\\d+)[ \\t]+obj\\s*')},
        {'name': 'Object', 'condition': DynExpr('/^<</'), 'type': PDF_Object},
        {'name': 'List', 'condition': DynExpr('/^\\[/'), 'type': PDF_List},
        {'name': 'Stream', 'condition': DynExpr('/^stream/'), 'type': PDF_Stream},
        {'name': 'Footer', 'type': T, 'regex': re.compile(b'\\s*(endobj)\\s*')},
    ]


class PDF(VStruct):
    ROOT = True
    FILETYPES = ('pdf',)
    FILTER = '%PDF-1\\.'
    FIELDS = [
        {'name': 'Magic', 'type': RX, 'regex': re.compile(b'%PDF-1\\.\\d+[\\r\\n]*')},
        {'name': 'Version', 'flags': 2, 'type': IS, 'dyn_offset': '@Magic + 7'},
        {'name': 'Nodes', 'flags': 10, 'count': True, 'type': PDF_HeaderObject, 'dyn_offset': '@/(\\d+)[ \\t]+(\\d+)[ \\t]+obj\\s/'},
        {'name': 'xref', 'type': RX, 'regex': re.compile(b'xref\\s+(\\d+)\\s+(\\d+)\\s+((?:\\d+\\s+\\d+[fn]\\s+)+)')},
        {'name': 'trailer', 'condition': DynExpr('/trailer\\s*<</'), 'type': PDF_Trailer},
        {'name': 'eof', 'type': RX, 'regex': re.compile(b'%%EOF')},
    ]


