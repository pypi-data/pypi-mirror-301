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