"""
vstruct2: Basic field types.

Author: Vlad Topan (vtopan/gmail).
"""

from .vstruct import Field, DynExpr
from .logging import dbg

import ast
from datetime import datetime, timedelta
import inspect
import math
import re
import struct


DEFAULT_ENCODINGS = {
    1: 'utf8',
    2: 'utf16',
    4: 'utf32',
}
PY_TO_VSTRUCT = {
    'B': 'B',
    'H': 'I2',
    'I': 'I4',
    'Q': 'I8',
    'b': 'SI1',
    'h': 'SI2',
    'i': 'SI4',
    'q': 'SI8',
    }


class IntType(Field):
    IS_BASIC = True
    IS_NUMERIC = True
    ENDIANNESS = '<'


class I1(IntType):
    SFORMAT = 'B'
    ENDIANNESS = None
B = I1


class I2(IntType):
    SFORMAT = 'H'
I2L = I2
W = I2


class I4(IntType):
    SFORMAT = 'I'
I4L = I4
D = I4


class I8(IntType):
    SFORMAT = 'Q'
I8L = I8
Q = I8


class I2B(IntType):
    SFORMAT = 'H'
    ENDIANNESS = '>'


class I4B(IntType):
    SFORMAT = 'I'
    ENDIANNESS = '>'


class I8B(IntType):
    SFORMAT = 'Q'
    ENDIANNESS = '>'


class SI1(IntType):
    SFORMAT = 'b'


class SI2(IntType):
    SFORMAT = 'h'
SI2L = SI2


class SI4(IntType):
    SFORMAT = 'i'
SI4L = SI4


class SI8(IntType):
    SFORMAT = 'q'
SI8L = SI8


class SI2B(IntType):
    SFORMAT = 'h'
    ENDIANNESS = '>'


class SI4B(IntType):
    SFORMAT = 'i'
    ENDIANNESS = '>'


class SI8B(IntType):
    SFORMAT = 'q'
    ENDIANNESS = '>'


class FloatType(Field):
    IS_BASIC = True
    IS_NUMERIC = True
    ENDIANNESS = None


class F4(FloatType):
    SFORMAT = 'f'
F32 = F4


class F8(FloatType):
    SFORMAT = 'd'
F64 = F8


class BitMap(IntType):
    ENDIANNESS = '<'

    def _post_parse(self):
        for k, v in self.bit_map.items():
            first_bit_pos = int(math.log2(k & -k) + 1)
            setattr(self, v, (self.value & k) >> (first_bit_pos - 1))


class BM1(BitMap):
    SFORMAT = 'B'
    ENDIANNESS = None


class BM2(BitMap):
    SFORMAT = 'H'


class BM3(BitMap):
    """
    Yes, this exists. See Facebook's Zstandard, Block_Header in particular.
    """
    SFORMAT = 'BBB'

    def _post_parse(self):
        if self.ENDIANNESS == '<':
            self.value = self.value[0] | (self.value[1] << 8) | (self.value[2] << 16)
        else:
            self.value = self.value[2] | (self.value[1] << 8) | (self.value[0] << 16)
        super()._post_parse()


class BM4(BitMap):
    SFORMAT = 'I'


class BM8(BitMap):
    SFORMAT = 'Q'


class I4UT(I4):
    """ Unix timestamp as 4-byte LE integer. """

    def formatter(self, *args, **kwargs):
        return f"{self.value} ({datetime.fromtimestamp(self.value).strftime('%d.%m.%Y, %H:%M:%S')})"


class DOSDate(I2):
    """ MS-DOS date. """

    def _post_parse(self):
        self.value = (self.value & 0x1F, (self.value >> 5) & 0xF, (self.value >> 9) + 1980)

    def formatter(self, value):
        return '<not-parsed-yet>' if isinstance(value, int) else ('%02d.%02d.%04d' % value)


class DOSTime(I2):
    """ MS-DOS time. """

    def _post_parse(self):
        self.value = (self.value >> 11, (self.value >> 5) & 0xF, self.value & 0x1F)

    def formatter(self, value):
        return '<not-parsed-yet>' if isinstance(value, int) else ('%02d:%02d:%02d' % value)


class NTFSTime(I8):
    """ NTFS FILETIME structure. """

    def formatter(self, value):
        dt = datetime(1601, 1, 1, 0, 0, 0) + timedelta(seconds=value / 1e7)
        return f"{value} ({dt.strftime('%d.%m.%Y, %H:%M:%S')})"


class StringType(Field):
    ENDIANNESS = None
    BPC = 1
    ENCODING = None
    NULLTERM = True
    IS_BASIC = True
    IS_NUMERIC = False

    def _parse(self):
        self._parsing = True
        cls = self.__class__
        if getattr(self, 'length', None):
            length = self.parent.eval(self.length) if isinstance(self.length, DynExpr) else self.length
        else:
            maxlen = getattr(self, 'maxlen', None)
            if isinstance(maxlen, DynExpr):
                maxlen = self.parent.eval(maxlen)
            if cls.NULLTERM:
                end = self.dataview.find(b'\0' * cls.BPC, self.offset)
                if end < 0:
                    end = len(self.dataview) - 1
                else:
                    end += 1    # include terminating NULL
                length = (end - self.offset) // cls.BPC
            else:
                length = maxlen
            if maxlen and length > maxlen:
                length = maxlen
        buffer = self.dataview[self.offset:self.offset + length * cls.BPC]
        self._size = len(buffer)
        if cls.ENCODING:
            buffer = buffer.decode(getattr(self, 'encoding', cls.ENCODING or DEFAULT_ENCODINGS[cls.BPC]), errors='replace')
            if cls.NULLTERM:
                buffer = buffer.rstrip('\0')
        self.raw_value = buffer
        self.value = buffer
        self._parsing = False
        return self._size


class Raw(StringType):
    NULLTERM = False
R = Raw


class AS(StringType):
    """
    ASCII (actually UTF-8) NULL-terminated string.
    """
    BPC = 1
    ENCODING = 'utf8'
ASCII = AS
US = AS


class WS(StringType):
    """
    WCHAR (UTF-16) NULL-terminated string.
    """
    BPC = 2
    ENCODING = 'utf16'
WCHAR = WS


class BigInt(StringType):
    """
    Big endian variable-sized unsigned int.
    """

    def _post_parse(self):
        self.value = int.from_bytes(self.value, byteorder='big')


class Eval(Field):
    """
    Dynamic expression.
    """

    def parse(self):
        self.value = self.parent.eval(self.expression)
        self._size = 0
        return 0


class RegEx(Field):
    """
    Field matching a RegEx.
    """

    def parse(self):
        self.parse_regex()
        if self._present:
            dbg(f'{self.depth * "  "}Extracted regex {self.full_name} @ 0x{self.offset:X} = {self.value}', 2)
        return self._size

RX = RegEx


class StringRegEx(RegEx):
    """
    RegEx matching an UTF-8 string regex.
    """

    def parse(self):
        super().parse()
        if self.present:
            self.value = self.value.decode('utf8') if type(self.value) is bytes else [e.decode('utf8') for e in self.value]
        return self._size

SRX = StringRegEx


class IS(RegEx):
    """
    Integer as ASCII string.
    """

    REGEX = re.compile(rb'^(0x[a-f0-9]+|-?\d+)', flags=re.I)

    def parse(self):
        if not getattr(self, 'maxlen', None):
            self.maxlen = 32
        super().parse()
        if self.present:
            self.value = ast.literal_eval(self.value.decode('ascii'))
        return self._size


class Token(RegEx):
    """
    ASCII-string token from a predefined list, skips whitespace (space, tab, CR, LF).
    """

    def parse(self):
        super().parse()
        if self.present:
            self._value = self._value.decode('ascii')
        return self._size

T = Token


BASE_TYPES = {k for k, v in globals().items() if inspect.isclass(v) and issubclass(v, Field)}
BASE_STRING_TYPES = {k for k, v in globals().items() if inspect.isclass(v) and issubclass(v, StringType)}
BASE_REGEX_TYPES = {k for k, v in globals().items() if inspect.isclass(v) and issubclass(v, RegEx)}
