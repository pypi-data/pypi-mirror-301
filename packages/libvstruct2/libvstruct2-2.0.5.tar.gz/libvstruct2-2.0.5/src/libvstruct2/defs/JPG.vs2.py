from .vs2_TIFF import TIFF
from ..basefields import Field


JPG_MARKERS = {
    0xFF01: 'TEM',
    0xFFC0: 'SOF0',
    0xFFC1: 'SOF1',
    0xFFC2: 'SOF2',
    0xFFC3: 'SOF3',
    0xFFC4: 'DHT',
    0xFFC5: 'SOF5',
    0xFFC6: 'SOF6',
    0xFFC7: 'SOF7',
    0xFFC8: 'JPG',
    0xFFC9: 'SOF9',
    0xFFCA: 'SOF10',
    0xFFCB: 'SOF11',
    0xFFCC: 'DAC',
    0xFFCD: 'SOF13',
    0xFFCE: 'SOF14',
    0xFFCF: 'SOF15',
    0xFFD0: 'RST0',
    0xFFD1: 'RST1',
    0xFFD2: 'RST2',
    0xFFD3: 'RST3',
    0xFFD4: 'RST4',
    0xFFD5: 'RST5',
    0xFFD6: 'RST6',
    0xFFD7: 'RST7',
    0xFFD8: 'SOI',
    0xFFD9: 'EOI',
    0xFFDA: 'SOS',
    0xFFDB: 'DQT',
    0xFFDC: 'DNL',
    0xFFDD: 'DRI',
    0xFFDE: 'DHP',
    0xFFDF: 'EXP',
    0xFFE0: 'APP0',
    0xFFE1: 'APP1',
    0xFFE2: 'APP2',
    0xFFE3: 'APP3',
    0xFFE4: 'APP4',
    0xFFE5: 'APP5',
    0xFFE6: 'APP6',
    0xFFE7: 'APP7',
    0xFFE8: 'APP8',
    0xFFE9: 'APP9',
    0xFFEA: 'APP10',
    0xFFEB: 'APP11',
    0xFFEC: 'APP12',
    0xFFED: 'APP13',
    0xFFEE: 'APP14',
    0xFFEF: 'APP15',
    0xFFF0: 'JPG0',
    0xFFFD: 'JPG13',
    0xFFFE: 'COM',
    }

JPG_MARKERS_W_CONTENT = set(range(0xFFE0, 0xFFF0)) | {0xFFDB, 0xFFC0, 0xFFC4, 0xFFDA}


class ICC_DateTime(Field):
    SFORMAT = 'HHHHHH'
    ENDIANNESS = '>'

    def formatted_value(self):
        return '%02d:%02d:%02d, %02d.%02d.%04d' % (value[3:6] + value[2:0:-1])
