from . import logging, vstruct, defparser, fileid
from .vstruct import *
from .basefields import *
from .defparser import DefLoader
from .fileid import get_file_type, PARSERS
from .logging import log, err, warn, dbg
from .vstructs import *

__ver__ = '2.0.5'

VStruct.map = {}
for e in VStruct.__subclasses__():
    VStruct.map[e.__name__] = e
