# automatically generated from bios.vs2

from libvstruct2 import BM4, DynExpr, I4, I4L, I8L, VStruct


E820_MEM_TYPE = {
    0x0001: 'Available',
    0x0002: 'Reserved',
    0x0003: 'ACPI-reclaimable',
    0x0004: 'ACPI-NVS',
    0x0005: 'Unusable',
    0x0006: 'Disabled',
    }


class MultiBoot(VStruct):
    ROOT = True
    SFORMAT = 'IIIIIIIIIIII'
    SOFFSETS = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'Magic', 'type': I4, 'validator': 464367618},
        {'name': 'Flags', 'type': BM4, 'bit_map': {1: 'Align4K', 2: 'ReqMemInfo', 4: 'ReqVidModeInfo', 65536: 'ValidAddrs'}},
        {'name': 'Checksum', 'type': I4, 'should_be': DynExpr('($_ + $Magic + $Flags) & 0xFFFFFFFF == 0')},
        {'name': 'HeaderAddr', 'type': I4, 'description': 'Only valid if Flags.ValidAddrs is set'},
        {'name': 'LoadAddr', 'type': I4, 'description': 'Only valid if Flags.ValidAddrs is set'},
        {'name': 'LoadEndAddr', 'type': I4, 'description': 'Only valid if Flags.ValidAddrs is set'},
        {'name': 'BSSEndAddr', 'type': I4, 'description': 'Only valid if Flags.ValidAddrs is set'},
        {'name': 'EntryAddr', 'type': I4, 'description': 'Only valid if Flags.ValidAddrs is set'},
        {'name': 'ModeType', 'type': I4, 'description': 'Only valid if Flags.ReqVidModeInfo is set'},
        {'name': 'Width', 'type': I4, 'description': 'Only valid if Flags.ReqVidModeInfo is set'},
        {'name': 'Height', 'type': I4, 'description': 'Only valid if Flags.ReqVidModeInfo is set'},
        {'name': 'Depth', 'type': I4, 'description': 'Only valid if Flags.ReqVidModeInfo is set'},
    ]


class E820Entry(VStruct):
    SFORMAT = 'QQII'
    SOFFSETS = [0, 8, 16, 20, 24]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'BaseAddr', 'type': I8L},
        {'name': 'Length', 'type': I8L},
        {'name': 'Type', 'type': I4L, 'formatter': E820_MEM_TYPE},
        {'name': 'ExtAttr', 'type': I4L},
    ]


class E820(VStruct):
    ROOT = True
    FIELDS = [
        {'name': 'Entries', 'count': DynExpr('*'), 'type': E820Entry},
    ]


