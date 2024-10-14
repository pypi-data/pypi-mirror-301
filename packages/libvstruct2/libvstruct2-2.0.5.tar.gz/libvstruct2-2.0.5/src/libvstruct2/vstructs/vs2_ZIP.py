# automatically generated from ZIP.vs2

from libvstruct2 import AS, BM2, DOSDate, DOSTime, DynExpr, I1, I2, I4, I4UT, I8, NTFSTime, R, US, VStruct


ZIP_COMPRESSION = {
    # ref: https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.10.TXT
    0: 'Store',
    1: 'Shrink',
    2: 'Reduce',
    3: 'Reduce',
    4: 'Reduce',
    5: 'Reduce',
    6: 'Implode',
    7: 'Tokenize',
    8: 'Deflate',
    9: 'Enhanced-Deflate',
    12: 'BZIP2',
    14: 'LZMA',
    96: 'JPEG-Variant',
    97: 'WavPack',
    98: 'PPMd',
    99: 'AE-x-Encryption',
    }

ZIP_DEFLATE_COMPRESSION = {
    0: 'Normal',
    1: 'Maximum',
    2: 'Fast',
    3: 'Super fast',
    }

ZIP_CREATOR_HOST = {
    0: 'MS-DOS',
    1: 'Amiga',
    2: 'OpenVMS',
    3: 'UNIX',
    4: 'VM/CMS',
    5: 'Atari ST',
    6: 'OS/2 H.P.F.S.',
    7: 'Macintosh',
    8: 'Z-System',
    9: 'CP/M',
    10: 'Windows NTFS',
    11: 'MVS (OS/390 - Z/OS)',
    12: 'VSE',
    13: 'Acorn Risc',
    14: 'VFAT',
    15: 'alternate MVS',
    16: 'BeOS',
    17: 'Tandem',
    18: 'OS/400',
    19: 'OS X',
    }

ZIP_STRONG_ENCRYPTION_ALGO = {
    0x6601: 'DES',
    0x6602: 'RC2',
    0x6603: '3DES 168',
    0x6609: '3DES 112',
    0x660E: 'AES 128',
    0x660F: 'AES 192',
    0x6610: 'AES 256',
    0x6702: 'RC2',  # needs ver. >= 5.2
    0x6720: 'Blowfish',
    0x6721: 'Twofish',
    0x6801: 'RC4',
    0xFFFF: 'Unknown',
    }

ZIP_AE_X_KEY_SIZE = {
    1: '128 bits',
    2: '192 bits',
    3: '256 bits',
    }


class ZIP_DataDescriptor(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x07\x08'},
        {'name': 'CRC32', 'type': I4},
        {'name': 'CompressedSize', 'type': I4},
        {'name': 'UncompressedSize', 'type': I4},
    ]


class ZIP64_Ext_Info(VStruct):
    SFORMAT = 'QQQQ'
    SOFFSETS = [0, 8, 16, 24, 32]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'UncompressedSize', 'type': I8},
        {'name': 'CompressedSize', 'type': I8},
        {'name': 'RelHdrOffset', 'type': I8},
        {'name': 'DiskStartNum', 'type': I8},
    ]


class ZIP_Ext_StrongEncryption(VStruct):
    FIELDS = [
        {'name': 'Format', 'type': I2},
        {'name': 'AlgID', 'type': I2, 'formatter': ZIP_STRONG_ENCRYPTION_ALGO},
        {'name': 'Bitlen', 'type': I2},
        {'name': 'Flags', 'type': I2, 'bit_map': {1: 'Password', 2: 'Certificates'}},
        {'name': 'CertData', 'type': R, 'length': DynExpr('$^Size - 8')},
    ]


class ZIP_Ext_AE_X(VStruct):
    FIELDS = [
        {'name': 'VendorVer', 'type': I2},
        {'name': 'VendorID', 'type': R, 'length': 2},
        {'name': 'KeySize', 'type': I1, 'formatter': ZIP_AE_X_KEY_SIZE},
        {'name': 'CompressionMethod', 'type': I2, 'formatter': ZIP_COMPRESSION},
    ]


class ZIP_Ext_UTCTimestamps(VStruct):
    SFORMAT = 'BIII'
    SOFFSETS = [0, 1, 5, 9, 13]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'Flags', 'type': I1},
        {'name': 'MTime', 'type': I4UT},
        {'name': 'ATime', 'condition': DynExpr(' 9 <= $^Size '), 'type': I4UT},
        {'name': 'CTime', 'condition': DynExpr(' 13 <= $^Size '), 'type': I4UT},
    ]


class ZIP_Ext_InfoZip_UnixUidGid(VStruct):
    FIELDS = [
        {'name': 'Version', 'type': I1},
        {'name': 'UidSize', 'type': I1},
        {'name': 'Uid', 'type': R, 'length': DynExpr('$UidSize')},
        {'name': 'GidSize', 'type': I1},
        {'name': 'Gid', 'type': R, 'length': DynExpr('$GidSize')},
    ]


class ZIP_NTFS_Timestamps(VStruct):
    SFORMAT = 'QQQ'
    SOFFSETS = [0, 8, 16, 24]
    ENDIANNESS = '<'
    FIELDS = [
        {'name': 'MTime', 'type': NTFSTime},
        {'name': 'ATime', 'type': NTFSTime},
        {'name': 'CTime', 'type': NTFSTime},
    ]


class ZIP_NFTS_Tag(VStruct):
    FIELDS = [
        {'name': 'Tag', 'type': I2},
        {'name': 'Size', 'type': I2},
        {'name': 'Timestamps', 'condition': DynExpr('$Tag == 1'), 'type': ZIP_NTFS_Timestamps},
        {'name': 'Data', 'type': R, 'length': DynExpr('$Size'), 'condition': '$Tag not in (1,)'},
    ]


class ZIP_Ext_NTFS(VStruct):
    FIELDS = [
        {'name': 'Reserved', 'type': I4},
        {'name': 'Tags', 'count': DynExpr('*'), 'type': ZIP_NFTS_Tag, 'stop': '&crt_offset >= @^Magic + $^Size - 4'},
    ]


class ZIP_ExtraRecord(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 2},
        {'name': 'Size', 'type': I2},
        {'name': 'UTCTimestamps', 'flags': 2, 'condition': DynExpr("$Magic == b'UT'"), 'type': ZIP_Ext_UTCTimestamps},
        {'name': 'UnixUidGid', 'flags': 2, 'condition': DynExpr("$Magic == b'ux'"), 'type': ZIP_Ext_InfoZip_UnixUidGid},
        {'name': 'ZIP64ExtraInfo', 'flags': 2, 'condition': DynExpr("$Magic == b'\\x01\\0'"), 'type': ZIP64_Ext_Info},
        {'name': 'StrongEncryption', 'flags': 2, 'condition': DynExpr("$Magic == b'\\x17\\0'"), 'type': ZIP_Ext_StrongEncryption},
        {'name': 'AEXEncryption', 'flags': 2, 'condition': DynExpr("$Magic == b'\\x01\\x99'"), 'type': ZIP_Ext_AE_X},
        {'name': 'NTFS', 'flags': 2, 'condition': DynExpr("$Magic == b'\\x0A\\0'"), 'type': ZIP_Ext_NTFS},
        {'name': 'Data', 'type': R, 'length': DynExpr('$Size')},
    ]


class ZIP_FileEntry(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x03\x04'},
        {'name': 'VerRequired', 'type': I2, 'formatter': lambda x: (x // 10, x % 10)},
        {'name': 'Flags', 'type': BM2, 'bit_map': {1: 'Encrypted', 8: 'HasDataDescriptor', 32: 'CompressedPatchedData', 64: 'StrongEncryption', 2048: 'UTF8FileName', 8192: 'EncryptedCentralDirectory'}},
        {'name': 'CompressionMethod', 'type': I2, 'formatter': ZIP_COMPRESSION},
        {'name': 'DeflateCompression', 'flags': 2, 'condition': DynExpr('$CompressionMethod == 8'), 'type': I2, 'dyn_offset': '&Flags.offset', 'post_parse_value': lambda x: (x.value >> 2) & 3, 'formatter': ZIP_DEFLATE_COMPRESSION},
        {'name': 'LastModTime', 'type': DOSTime},
        {'name': 'LastModDate', 'type': DOSDate},
        {'name': 'CRC32', 'type': I4},
        {'name': 'CompressedSize', 'type': I4},
        {'name': 'UncompressedSize', 'type': I4},
        {'name': 'FileNameLen', 'type': I2},
        {'name': 'ExtraDataLen', 'type': I2},
        {'name': 'FileName', 'type': US, 'length': DynExpr('$FileNameLen')},
        {'name': 'ExtraRecords', 'count': DynExpr('*'), 'type': ZIP_ExtraRecord, 'condition': '$ExtraDataLen', 'stop': '&crt_offset >= &FileName.offset + $FileNameLen + $ExtraDataLen'},
        {'name': 'LookaheadDD', 'flags': 3, 'condition': DynExpr('$CompressedSize == 0'), 'type': ZIP_DataDescriptor, 'dyn_offset': '@/PK\\x07\\x08/f'},
        {'name': 'FileData', 'type': R, 'length': DynExpr("$CompressedSize or ($LookaheadDD.CompressedSize if hasattr(self, 'LookaheadDD') else 0)")},
        {'name': 'DataDescriptor', 'condition': DynExpr('&Flags.HasDataDescriptor'), 'type': ZIP_DataDescriptor},
        {'name': 'Trail', 'flags': 3, 'type': R, 'length': 4},
    ]


class ZIP_ArchiveExtraDataRecord(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x06\x08'},
        {'name': 'Size', 'type': I4},
        {'name': 'Data', 'type': R, 'length': DynExpr('$Size')},
    ]


class ZIP_CentralDirectoryRecord(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x01\x02'},
        {'name': 'VerCreator', 'flags': 2, 'type': I2},
        {'name': 'VerCreatorOS', 'type': I1, 'formatter': ZIP_CREATOR_HOST},
        {'name': 'VerCreatorSpec', 'type': I1, 'formatter': lambda x: (x // 10, x % 10)},
        {'name': 'VerRequired', 'type': I2},
        {'name': 'Flags', 'type': I2},
        {'name': 'CompressionMethod', 'type': I2, 'formatter': ZIP_COMPRESSION},
        {'name': 'LastModTime', 'type': I2},
        {'name': 'LastModDate', 'type': I2},
        {'name': 'CRC32', 'type': I4},
        {'name': 'CompressedSize', 'type': I4},
        {'name': 'UncompressedSize', 'type': I4},
        {'name': 'FileNameLen', 'type': I2},
        {'name': 'ExtraDataLen', 'type': I2},
        {'name': 'CommentLen', 'type': I2},
        {'name': 'StartDiskNum', 'type': I2},
        {'name': 'IntFileAttr', 'type': BM2, 'bit_map': {1: 'ASCIIFile', 2: 'RecordLenCtrlFieldPresent'}},
        {'name': 'ExtFileAttr', 'type': I4},
        {'name': 'RelOffset', 'type': I4},
        {'name': 'FileName', 'type': US, 'length': DynExpr('$FileNameLen')},
        {'name': 'ExtraRecords', 'count': DynExpr('*'), 'type': ZIP_ExtraRecord, 'condition': '$ExtraDataLen', 'stop': '&crt_offset >= &FileName.offset + $FileNameLen + $ExtraDataLen'},
        {'name': 'Comment', 'type': US, 'length': DynExpr('$CommentLen')},
        {'name': 'Trail', 'flags': 3, 'type': R, 'length': 4},
    ]


class ZIP_EndOfCentralDirectoryRecord(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x05\x06'},
        {'name': 'DiskNumber', 'type': I2},
        {'name': 'CentralDirDisk', 'type': I2},
        {'name': 'CentralDirRecOnDiskCount', 'type': I2},
        {'name': 'CentralDirRecTotalCount', 'type': I2},
        {'name': 'SizeOfCentralDir', 'type': I4},
        {'name': 'RelOffsetToCentralDir', 'type': I4},
        {'name': 'CommentLen', 'type': I2},
        {'name': 'Comment', 'type': AS, 'length': DynExpr('$CommentLen')},
    ]


class ZIP64_EndOfCentralDirectoryRecord(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x06\x06'},
        {'name': 'Size', 'type': I8},
        {'name': 'VerCreator', 'type': I2},
        {'name': 'VerRequired', 'type': I2},
        {'name': 'DiskNumber', 'type': I4},
        {'name': 'CentralDirDisk', 'type': I4},
        {'name': 'CentralDirRecOnDiskCount', 'type': I8},
        {'name': 'CentralDirRecTotalCount', 'type': I8},
        {'name': 'SizeOfCentralDir', 'type': I8},
        {'name': 'RelOffsetToCentralDir', 'type': I8},
        {'name': 'ExtSectors', 'type': R, 'length': DynExpr('$Size - 44')},
    ]


class ZIP64_EndOfCentralDirectoryLocator(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x06\x07'},
        {'name': 'EndOfCentralDirectoryRecordDiskNum', 'type': I4},
        {'name': 'EndOfCentralDirectoryRecordOffset', 'type': I8},
        {'name': 'TotalNumOfDisks', 'type': I4},
    ]


class ZIP_DigitalSignature(VStruct):
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'PK\x05\x05'},
        {'name': 'Size', 'type': I2},
        {'name': 'Data', 'type': R, 'length': DynExpr('$Size')},
    ]


class ZIP(VStruct):
    ROOT = True
    FILETYPES = ('zip',)
    FILTER = '^PK\\x03\\x04'
    FIELDS = [
        {'name': 'Entries', 'count': DynExpr('*'), 'type': ZIP_FileEntry, 'stop': "(&bytes_left == 0) or $crt_field.Trail != b'PK\\x03\\x04'"},
        {'name': 'ArchiveExtraData', 'condition': DynExpr('/PK\\x06\\x08/'), 'type': ZIP_ArchiveExtraDataRecord},
        {'name': 'CentralDirectory', 'count': DynExpr('*'), 'type': ZIP_CentralDirectoryRecord, 'stop': "$crt_field.Trail != b'PK\\x01\\x02'"},
        {'name': 'EndRecord64', 'condition': DynExpr('/PK\\x06\\x06/'), 'type': ZIP64_EndOfCentralDirectoryRecord},
        {'name': 'EndLocator64', 'condition': DynExpr('/PK\\x06\\x07/'), 'type': ZIP64_EndOfCentralDirectoryLocator},
        {'name': 'EndRecord', 'type': ZIP_EndOfCentralDirectoryRecord},
        {'name': 'Overlay', 'type': R, 'length': DynExpr('&bytes_left')},
    ]


