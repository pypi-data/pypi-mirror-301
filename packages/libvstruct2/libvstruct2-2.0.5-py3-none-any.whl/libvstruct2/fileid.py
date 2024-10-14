"""
vstruct2: File / buffer identification library.

Author: Vlad Topan (vtopan/gmail).
"""

import struct

try:
    import iogp
except ImportError:
    iogp = None


HEADER_SIZE = 8192
PARSERS = {}        # this gets filled in at runtime


def vs2_get_file_type(source):
    """
    Identify the type of a file (or `bytes` buffer).

    This is a backup implementation in case iogp.data.get_file_type() is not available.

    :param source: File handle, filename or bytes buffer.
    """
    if hasattr(source, 'read'):
        header = source.read(HEADER_SIZE)
    elif type(source) == str:
        header = open(source, 'rb').read(HEADER_SIZE)
    else:
        header = source[:HEADER_SIZE]
    if header[:2] == b'MZ':
        elfanew = struct.unpack('<L', header[0x3C:0x40])[0]
        if elfanew + 8 < len(header):
            if header[elfanew:elfanew + 4] == b'PE\0\0':
                machine = header[elfanew + 4:elfanew + 6]
                if machine == b'\x64\x86':
                    return 'pe+'
                elif machine == b'\x4c\x01':
                    return 'pe'
                else:
                    return 'coff'
        return 'mz'
    elif header[:4] == b'\x7FELF':
        return 'elf'
    elif header[:4] == b'\xD0\xCF\x11\xE0':
        return 'docfile'
    elif header[:2] == b'PK':
        if b'META-INF/MANIFEST' in header and b'.class' in header:
            return 'jar'
        return 'zip'
    elif header[:4] == b'dex\x0A':
        return 'dex'
    elif header[:4] == b'%PDF':
        return 'pdf'
    elif header[:5] == rb'{\rtf':
        return 'rtf'
    elif header[:5] == b'<html':
        return 'html'
    elif header[:2] == b'\0\0' and header[2:4] in (b'\1\0', b'\2\0'):
        return 'ico'
    elif header[:2] == b'BM':
        return 'bmp'
    elif header[:8] == b'\x89PNG\r\n\x1A\n':
        return 'png'
    elif header[:4] in (b'II*\0', b'MM\0*'):
        return 'tiff'
    elif header[:3] == b'\xFF\xD8\xFF':
        return 'jpg'
    elif header[:4] == b'r1cs':
        return 'r1cs'
    else:
        return 'unknown'


if iogp:
    from iogp.data import get_file_type
else:
    get_file_type = vs2_get_file_type
