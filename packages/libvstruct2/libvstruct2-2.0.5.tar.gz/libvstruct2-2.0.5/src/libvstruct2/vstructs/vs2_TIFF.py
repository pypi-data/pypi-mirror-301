# automatically generated from TIFF.vs2

from libvstruct2 import AS, DynExpr, Eval, I1, I2, I2B, I4, I4B, R, SI1, SI2, SI4, VStruct


TIFF_FIELDS_BY_SIZE = {
    # maps field size (in bytes) to list of field types
    1: (1, 2, 6, 7,),
    2: (3, 8,),
    4: (4, 9, 11,),
    8: (5, 10, 12,)
    }

# maps field type to field size
TIFF_FIELD_SIZE = {e:k for k, v in TIFF_FIELDS_BY_SIZE.items() for e in v}

IFD_TAGS = {
    0x010e: 'ImageDescription',
    0x010f: 'Make',
    0x0110: 'Model',
    0x0112: 'Orientation',
    0x011a: 'XResolution',
    0x011b: 'YResolution',
    0x0128: 'ResolutionUnit',
    0x0131: 'Software',
    0x0132: 'DateTime',
    0x013e: 'WhitePoint',
    0x013f: 'PrimaryChromaticities',
    0x0211: 'YCbCrCoefficients',
    0x0213: 'YCbCrPositioning',
    0x0214: 'ReferenceBlackWhite',
    0x8298: 'Copyright',
    0x8769: 'ExifOffset',
    0x829a: 'ExposureTime',
    0x829d: 'FNumber',
    0x8822: 'ExposureProgram',
    0x8827: 'ISOSpeedRatings',
    0x9000: 'ExifVersion',
    0x9003: 'DateTimeOriginal',
    0x9004: 'DateTimeDigitized',
    0x9101: 'ComponentConfiguration',
    0x9102: 'CompressedBitsPerPixel',
    0x9201: 'ShutterSpeedValue',
    0x9202: 'ApertureValue',
    0x9203: 'BrightnessValue',
    0x9204: 'ExposureBiasValue',
    0x9205: 'MaxApertureValue',
    0x9206: 'SubjectDistance',
    0x9207: 'MeteringMode',
    0x9208: 'LightSource',
    0x9209: 'Flash',
    0x920a: 'FocalLength',
    0x927c: 'MakerNote',
    0x9286: 'UserComment',
    0xa000: 'FlashPixVersion',
    0xa001: 'ColorSpace',
    0xa002: 'ExifImageWidth',
    0xa003: 'ExifImageHeight',
    0xa004: 'RelatedSoundFile',
    0xa005: 'ExifInteroperabilityOffset',
    0xa20e: 'FocalPlaneXResolution',
    0xa20f: 'FocalPlaneYResolution',
    0xa210: 'FocalPlaneResolutionUnit',
    0xa217: 'SensingMethod',
    0xa300: 'FileSource',
    0xa301: 'SceneType',
    0x0100: 'ImageWidth',
    0x0101: 'ImageLength',
    0x0102: 'BitsPerSample',
    0x0103: 'Compression',
    0x0106: 'PhotometricInterpretation',
    0x0111: 'StripOffsets',
    0x0115: 'SamplesPerPixel',
    0x0116: 'RowsPerStrip',
    0x0117: 'StripByteConunts',
    0x011a: 'XResolution',
    0x011b: 'YResolution',
    0x011c: 'PlanarConfiguration',
    0x0128: 'ResolutionUnit',
    0x0201: 'JpegIFOffset',
    0x0202: 'JpegIFByteCount',
    0x0211: 'YCbCrCoefficients',
    0x0212: 'YCbCrSubSampling',
    0x0213: 'YCbCrPositioning',
    0x0214: 'ReferenceBlackWhite',
    0x00fe: 'NewSubfileType',
    0x00ff: 'SubfileType',
    0x012d: 'TransferFunction',
    0x013b: 'Artist',
    0x013d: 'Predictor',
    0x0142: 'TileWidth',
    0x0143: 'TileLength',
    0x0144: 'TileOffsets',
    0x0145: 'TileByteCounts',
    0x014a: 'SubIFDs',
    0x015b: 'JPEGTables',
    0x828d: 'CFARepeatPatternDim',
    0x828e: 'CFAPattern',
    0x828f: 'BatteryLevel',
    0x83bb: 'IPTC/NAA',
    0x8773: 'InterColorProfile',
    0x8824: 'SpectralSensitivity',
    0x8825: 'GPSInfo',
    0x8828: 'OECF',
    0x8829: 'Interlace',
    0x882a: 'TimeZoneOffset',
    0x882b: 'SelfTimerMode',
    0x920b: 'FlashEnergy',
    0x920c: 'SpatialFrequencyResponse',
    0x920d: 'Noise',
    0x9211: 'ImageNumber',
    0x9212: 'SecurityClassification',
    0x9213: 'ImageHistory',
    0x9214: 'SubjectLocation',
    0x9215: 'ExposureIndex',
    0x9216: 'TIFF/EPStandardID',
    0x9290: 'SubSecTime',
    0x9291: 'SubSecTimeOriginal',
    0x9292: 'SubSecTimeDigitized',
    0xa20b: 'FlashEnergy',
    0xa20c: 'SpatialFrequencyResponse',
    0xa214: 'SubjectLocation',
    0xa215: 'ExposureIndex',
    0xa302: 'CFAPattern',
    }


class TIFF_IFDEntry(VStruct):
    FIELDS = [
        {'name': 'Tag', 'type': I2, 'formatter': IFD_TAGS},
        {'name': 'Type', 'type': I2},
        {'name': 'Count', 'type': I4},
        {'name': 'ValueOrOffset', 'type': I4},
        {'name': 'Size', 'flags': 2, 'expression': '$Count * TIFF_FIELD_SIZE[$Type]', 'type': Eval},
        {'name': 'Value', 'flags': 2, 'type': R, 'length': DynExpr('$Size'), 'dyn_offset': '@^^ + $ValueOrOffset', 'condition': '$Size > 4'},
        {'name': 'Value', 'flags': 2, 'expression': '$ValueOrOffset', 'type': Eval, 'condition': '$Size <= 4'},
        {'name': 'String', 'flags': 2, 'type': AS, 'length': DynExpr('$Count'), 'dyn_offset': '@Value', 'condition': '$Type == 2'},
    ]


class XXX(VStruct):
    FIELDS = [
        {'name': 'UByte', 'flags': 2, 'count': DynExpr('$Count'), 'type': I1, 'dyn_offset': '@Value', 'condition': '$Type in (1, 7)'},
        {'name': 'SByte', 'flags': 2, 'count': DynExpr('$Count'), 'type': SI1, 'dyn_offset': '@Value', 'condition': '$Type == 6'},
        {'name': 'UShort', 'flags': 2, 'count': DynExpr('$Count'), 'type': I2, 'dyn_offset': '@Value', 'condition': '$Type == 3'},
        {'name': 'SShort', 'flags': 2, 'count': DynExpr('$Count'), 'type': SI2, 'dyn_offset': '@Value', 'condition': '$Type == 8'},
        {'name': 'ULong', 'flags': 2, 'count': DynExpr('$Count'), 'type': I4, 'dyn_offset': '@Value', 'condition': '$Type == 4'},
        {'name': 'SLong', 'flags': 2, 'count': DynExpr('$Count'), 'type': SI4, 'dyn_offset': '@Value', 'condition': '$Type == 9'},
    ]


class TIFF_IFD(VStruct):
    FIELDS = [
        {'name': 'Count', 'type': I2B},
        {'name': 'Entries', 'count': DynExpr('$Count'), 'type': TIFF_IFDEntry},
        {'name': 'NextIFDOffset', 'type': I4B},
    ]


class TIFF(VStruct):
    ROOT = True
    FILETYPES = ('tiff',)
    FILTER = '^(II*\\0|MM\\0*)'
    FIELDS = [
        {'name': 'ByteOrder', 'type': R, 'length': 4, 'validator': [b'II*\x00', b'MM\x00*']},
        {'name': 'Endianness', 'flags': 2, 'expression': "'<' if $ByteOrder == b'II*\\0' else '>'", 'type': Eval},
        {'name': 'IFD0Offset', 'type': I4, 'endianness': DynExpr('$Endianness')},
        {'name': 'IFDs', 'flags': 2, 'count': True, 'type': TIFF_IFD, 'dyn_offset': '(@ByteOrder + $crt_field.NextIFDOffset) if &field_index else (@ByteOrder + $IFD0Offset)', 'stop': '$crt_field.NextIFDOffset == 0', 'endianness': DynExpr('$Endianness')},
    ]


