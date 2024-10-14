# automatically generated from definition files

from .vs2_BMP import BMP
from .vs2_GIF import GIF
from .vs2_ICO import ICO
from .vs2_JPG import JPG
from .vs2_MBR import MBR
from .vs2_PDF import PDF
from .vs2_PE import PE
from .vs2_PNG import PNG
from .vs2_R1CS import R1CS
from .vs2_TIFF import TIFF
from .vs2_ZIP import ZIP
from .vs2_bios import E820, MultiBoot
from .vs2_socks import SOCKS5, SOCKS5Client, SOCKS5Server
from .vs2_zstd import Zstandard

ROOT_PARSERS = [BMP, E820, GIF, ICO, JPG, MBR, MultiBoot, PDF, PE, PNG, R1CS, SOCKS5, SOCKS5Client, SOCKS5Server, TIFF, ZIP, Zstandard]

FT_MAP = {
    'bmp': ('vs2_BMP', BMP),
    'coff': ('vs2_PE', PE),
    'cur': ('vs2_ICO', ICO),
    'gif': ('vs2_GIF', GIF),
    'ico': ('vs2_ICO', ICO),
    'jpg': ('vs2_JPG', JPG),
    'mbr': ('vs2_MBR', MBR),
    'mz': ('vs2_PE', PE),
    'pdf': ('vs2_PDF', PDF),
    'pe': ('vs2_PE', PE),
    'pe+': ('vs2_PE', PE),
    'png': ('vs2_PNG', PNG),
    'r1cs': ('vs2_R1CS', R1CS),
    'socks5': ('vs2_socks', SOCKS5),
    'socks5client': ('vs2_socks', SOCKS5Client),
    'socks5server': ('vs2_socks', SOCKS5Server),
    'tiff': ('vs2_TIFF', TIFF),
    'zip': ('vs2_ZIP', ZIP),
    'zst': ('vs2_zstd', Zstandard),
    }

