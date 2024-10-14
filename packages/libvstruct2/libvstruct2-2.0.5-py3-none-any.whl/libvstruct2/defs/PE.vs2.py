import struct

from libvstruct2 import dbg


IMAGE_DIRECTORY_ENTRY_ARCHITECTURE = 7                       # Architecture Specific Data
IMAGE_DIRECTORY_ENTRY_BASERELOC = 5                          # Base Relocation Table
IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT = 11                      # Bound Import Directory in headers
IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR = 14                    # COM Runtime descriptor
IMAGE_DIRECTORY_ENTRY_DEBUG = 6                              # Debug Directory
IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT = 13                      # Delay Load Import Descriptors
IMAGE_DIRECTORY_ENTRY_EXCEPTION = 3                          # Exception Directory
IMAGE_DIRECTORY_ENTRY_EXPORT = 0                             # Export Directory
IMAGE_DIRECTORY_ENTRY_GLOBALPTR = 8                          # RVA of GP
IMAGE_DIRECTORY_ENTRY_IAT = 12                               # Import Address Table
IMAGE_DIRECTORY_ENTRY_IMPORT = 1                             # Import Directory
IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG = 10                       # Load Configuration Directory
IMAGE_DIRECTORY_ENTRY_RESOURCE = 2                           # Resource Directory
IMAGE_DIRECTORY_ENTRY_SECURITY = 4                           # Security Directory
IMAGE_DIRECTORY_ENTRY_TLS = 9                                # TLS Directory
IMAGE_DLLCHARACTERISTICS_APPCONTAINER = 0x1000               # Image should execute in an AppContainer
IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE = 0x0040               # DLL can move.
IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY = 0x0080            # Code Integrity Image
IMAGE_DLLCHARACTERISTICS_GUARD_CF = 0x4000                   # Image supports Control Flow Guard.
IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA = 0x0020            # Image can handle a high entropy 64-bit virtual address space.
IMAGE_DLLCHARACTERISTICS_NO_BIND = 0x0800                    # Do not bind this image.
IMAGE_DLLCHARACTERISTICS_NO_ISOLATION = 0x0200               # Image understands isolation and doesn't want it
IMAGE_DLLCHARACTERISTICS_NO_SEH = 0x0400                     # Image does not use SEH.  No SE handler may reside in this image
IMAGE_DLLCHARACTERISTICS_NX_COMPAT = 0x0100                  # Image is NX compatible
IMAGE_DLLCHARACTERISTICS_TERMINAL_SERVER_AWARE = 0x8000
IMAGE_DLLCHARACTERISTICS_WDM_DRIVER = 0x2000                 # Driver uses WDM model
IMAGE_DOS_SIGNATURE = 0x5A4D                                 # MZ
IMAGE_FILE_32BIT_MACHINE = 0x0100                            # 32 bit word machine.
IMAGE_FILE_AGGRESIVE_WS_TRIM = 0x0010                        # Aggressively trim working set
IMAGE_FILE_BYTES_REVERSED_HI = 0x8000                        # Bytes of machine word are reversed.
IMAGE_FILE_BYTES_REVERSED_LO = 0x0080                        # Bytes of machine word are reversed.
IMAGE_FILE_DEBUG_STRIPPED = 0x0200                           # Debugging info stripped from file in .DBG file
IMAGE_FILE_DLL = 0x2000                                      # File is a DLL.
IMAGE_FILE_EXECUTABLE_IMAGE = 0x0002                         # File is executable  (i.e. no unresolved external references).
IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020                      # App can handle >2gb addresses
IMAGE_FILE_LINE_NUMS_STRIPPED = 0x0004                       # Line nunbers stripped from file.
IMAGE_FILE_LOCAL_SYMS_STRIPPED = 0x0008                      # Local symbols stripped from file.
IMAGE_FILE_MACHINE_ALPHA = 0x0184                            # Alpha_AXP
IMAGE_FILE_MACHINE_ALPHA64 = 0x0284                          # ALPHA64
IMAGE_FILE_MACHINE_AM33 = 0x01d3
IMAGE_FILE_MACHINE_AMD64 = 0x8664                            # AMD64 (K8)
IMAGE_FILE_MACHINE_ARM = 0x01c0                              # ARM Little-Endian
IMAGE_FILE_MACHINE_ARM64 = 0xAA64                            # ARM64 Little-Endian
IMAGE_FILE_MACHINE_ARMNT = 0x01c4                            # ARM Thumb-2 Little-Endian
IMAGE_FILE_MACHINE_AXP64 = IMAGE_FILE_MACHINE_ALPHA64
IMAGE_FILE_MACHINE_CEE = 0xC0EE
IMAGE_FILE_MACHINE_CEF = 0x0CEF
IMAGE_FILE_MACHINE_CHPE_X86 = 0x3A64
IMAGE_FILE_MACHINE_EBC = 0x0EBC                              # EFI Byte Code
IMAGE_FILE_MACHINE_I386 = 0x014c                             # Intel 386.
IMAGE_FILE_MACHINE_IA64 = 0x0200                             # Intel 64
IMAGE_FILE_MACHINE_M32R = 0x9041                             # M32R little-endian
IMAGE_FILE_MACHINE_MIPS16 = 0x0266                           # MIPS
IMAGE_FILE_MACHINE_MIPSFPU = 0x0366                          # MIPS
IMAGE_FILE_MACHINE_MIPSFPU16 = 0x0466                        # MIPS
IMAGE_FILE_MACHINE_POWERPC = 0x01F0                          # IBM PowerPC Little-Endian
IMAGE_FILE_MACHINE_POWERPCFP = 0x01f1
IMAGE_FILE_MACHINE_R10000 = 0x0168                           # MIPS little-endian
IMAGE_FILE_MACHINE_R3000 = 0x0162                            # MIPS little-endian, 0x160 big-endian
IMAGE_FILE_MACHINE_R4000 = 0x0166                            # MIPS little-endian
IMAGE_FILE_MACHINE_SH3 = 0x01a2                              # SH3 little-endian
IMAGE_FILE_MACHINE_SH3DSP = 0x01a3
IMAGE_FILE_MACHINE_SH3E = 0x01a4                             # SH3E little-endian
IMAGE_FILE_MACHINE_SH4 = 0x01a6                              # SH4 little-endian
IMAGE_FILE_MACHINE_SH5 = 0x01a8                              # SH5
IMAGE_FILE_MACHINE_TARGET_HOST = 0x0001                      # Useful for indicating we want to interact with the host and not a WoW guest.
IMAGE_FILE_MACHINE_THUMB = 0x01c2                            # ARM Thumb/Thumb-2 Little-Endian
IMAGE_FILE_MACHINE_TRICORE = 0x0520                          # Infineon
IMAGE_FILE_MACHINE_UNKNOWN = 0
IMAGE_FILE_MACHINE_WCEMIPSV2 = 0x0169                        # MIPS little-endian WCE v2
IMAGE_FILE_NET_RUN_FROM_SWAP = 0x0800                        # If Image is on Net, copy and run from the swap file.
IMAGE_FILE_RELOCS_STRIPPED = 0x0001                          # Relocation info stripped from file.
IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP = 0x0400                  # If Image is on removable media, copy and run from the swap file.
IMAGE_FILE_SYSTEM = 0x1000                                   # System File.
IMAGE_FILE_UP_SYSTEM_ONLY = 0x4000                           # File should only be run on a UP machine
IMAGE_LOADER_FLAGS_COMPLUS = 0x00000001                      # COM+ image
IMAGE_LOADER_FLAGS_SYSTEM_GLOBAL = 0x01000000                # Global subsections apply across TS sessions.
IMAGE_NT_OPTIONAL_HDR32_MAGIC = 0x10b
IMAGE_NT_OPTIONAL_HDR64_MAGIC = 0x20b
IMAGE_NT_SIGNATURE = 0x00004550                              # PE00
IMAGE_NUMBEROF_DIRECTORY_ENTRIES = 16
IMAGE_OS2_SIGNATURE = 0x454E                                 # NE
IMAGE_OS2_SIGNATURE_LE = 0x454C                              # LE
IMAGE_ROM_OPTIONAL_HDR_MAGIC = 0x107
IMAGE_SCN_ALIGN_1024BYTES = 0x00B00000
IMAGE_SCN_ALIGN_128BYTES = 0x00800000
IMAGE_SCN_ALIGN_16BYTES = 0x00500000                         # Default alignment if no others are specified.
IMAGE_SCN_ALIGN_1BYTES = 0x00100000
IMAGE_SCN_ALIGN_2048BYTES = 0x00C00000
IMAGE_SCN_ALIGN_256BYTES = 0x00900000
IMAGE_SCN_ALIGN_2BYTES = 0x00200000
IMAGE_SCN_ALIGN_32BYTES = 0x00600000
IMAGE_SCN_ALIGN_4096BYTES = 0x00D00000
IMAGE_SCN_ALIGN_4BYTES = 0x00300000
IMAGE_SCN_ALIGN_512BYTES = 0x00A00000
IMAGE_SCN_ALIGN_64BYTES = 0x00700000
IMAGE_SCN_ALIGN_8192BYTES = 0x00E00000
IMAGE_SCN_ALIGN_8BYTES = 0x00400000
IMAGE_SCN_ALIGN_MASK = 0x00F00000
IMAGE_SCN_CNT_CODE = 0x00000020                              # Section contains code.
IMAGE_SCN_CNT_INITIALIZED_DATA = 0x00000040                  # Section contains initialized data.
IMAGE_SCN_CNT_UNINITIALIZED_DATA = 0x00000080                # Section contains uninitialized data.
IMAGE_SCN_GPREL = 0x00008000                                 # Section content can be accessed relative to GP
IMAGE_SCN_LNK_COMDAT = 0x00001000                            # Section contents comdat.
IMAGE_SCN_LNK_INFO = 0x00000200                              # Section contains comments or some other type of information.
IMAGE_SCN_LNK_NRELOC_OVFL = 0x01000000                       # Section contains extended relocations.
IMAGE_SCN_LNK_OTHER = 0x00000100                             # Reserved.
IMAGE_SCN_LNK_REMOVE = 0x00000800                            # Section contents will not become part of image.
IMAGE_SCN_MEM_16BIT = 0x00020000
IMAGE_SCN_MEM_DISCARDABLE = 0x02000000                       # Section can be discarded.
IMAGE_SCN_MEM_EXECUTE = 0x20000000                           # Section is executable.
IMAGE_SCN_MEM_FARDATA = 0x00008000
IMAGE_SCN_MEM_LOCKED = 0x00040000
IMAGE_SCN_MEM_NOT_CACHED = 0x04000000                        # Section is not cachable.
IMAGE_SCN_MEM_NOT_PAGED = 0x08000000                         # Section is not pageable.
IMAGE_SCN_MEM_PRELOAD = 0x00080000
IMAGE_SCN_MEM_PURGEABLE = 0x00020000
IMAGE_SCN_MEM_READ = 0x40000000                              # Section is readable.
IMAGE_SCN_MEM_SHARED = 0x10000000                            # Section is shareable.
IMAGE_SCN_MEM_WRITE = 0x80000000                             # Section is writeable.
IMAGE_SCN_NO_DEFER_SPEC_EXC = 0x00004000                     # Reset speculative exceptions handling bits in the TLB entries for this section.
IMAGE_SCN_SCALE_INDEX = 0x00000001                           # Tls index is scaled
IMAGE_SIZEOF_FILE_HEADER = 20
IMAGE_SIZEOF_SECTION_HEADER = 40
IMAGE_SIZEOF_SHORT_NAME = 8
IMAGE_SUBSYSTEM_EFI_APPLICATION = 10
IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER = 11
IMAGE_SUBSYSTEM_EFI_ROM = 13
IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER = 12
IMAGE_SUBSYSTEM_NATIVE = 1                                   # Image doesn't require a subsystem.
IMAGE_SUBSYSTEM_NATIVE_WINDOWS = 8                           # image is a native Win9x driver.
IMAGE_SUBSYSTEM_OS2_CUI = 5                                  # image runs in the OS/2 character subsystem.
IMAGE_SUBSYSTEM_POSIX_CUI = 7                                # image runs in the Posix character subsystem.
IMAGE_SUBSYSTEM_UNKNOWN = 0                                  # Unknown subsystem.
IMAGE_SUBSYSTEM_WINDOWS_BOOT_APPLICATION = 16
IMAGE_SUBSYSTEM_WINDOWS_CE_GUI = 9                           # Image runs in the Windows CE subsystem.
IMAGE_SUBSYSTEM_WINDOWS_CUI = 3                              # Image runs in the Windows character subsystem.
IMAGE_SUBSYSTEM_WINDOWS_GUI = 2                              # Image runs in the Windows GUI subsystem.
IMAGE_SUBSYSTEM_XBOX = 14
IMAGE_SUBSYSTEM_XBOX_CODE_CATALOG = 17
IMAGE_SYM_ABSOLUTE = -1                                      # Symbol is an absolute value.
IMAGE_SYM_CLASS_ARGUMENT = 0x0009
IMAGE_SYM_CLASS_AUTOMATIC = 0x0001
IMAGE_SYM_CLASS_BIT_FIELD = 0x0012
IMAGE_SYM_CLASS_BLOCK = 0x0064
IMAGE_SYM_CLASS_CLR_TOKEN = 0x006B
IMAGE_SYM_CLASS_END_OF_FUNCTION = -1
IMAGE_SYM_CLASS_END_OF_STRUCT = 0x0066
IMAGE_SYM_CLASS_ENUM_TAG = 0x000F
IMAGE_SYM_CLASS_EXTERNAL = 0x0002
IMAGE_SYM_CLASS_EXTERNAL_DEF = 0x0005
IMAGE_SYM_CLASS_FAR_EXTERNAL = 0x0044
IMAGE_SYM_CLASS_FILE = 0x0067
IMAGE_SYM_CLASS_FUNCTION = 0x0065
IMAGE_SYM_CLASS_LABEL = 0x0006
IMAGE_SYM_CLASS_MEMBER_OF_ENUM = 0x0010
IMAGE_SYM_CLASS_MEMBER_OF_STRUCT = 0x0008
IMAGE_SYM_CLASS_MEMBER_OF_UNION = 0x000B
IMAGE_SYM_CLASS_NULL = 0x0000
IMAGE_SYM_CLASS_REGISTER = 0x0004
IMAGE_SYM_CLASS_REGISTER_PARAM = 0x0011
IMAGE_SYM_CLASS_SECTION = 0x0068
IMAGE_SYM_CLASS_STATIC = 0x0003
IMAGE_SYM_CLASS_STRUCT_TAG = 0x000A
IMAGE_SYM_CLASS_TYPE_DEFINITION = 0x000D
IMAGE_SYM_CLASS_UNDEFINED_LABEL = 0x0007
IMAGE_SYM_CLASS_UNDEFINED_STATIC = 0x000E
IMAGE_SYM_CLASS_UNION_TAG = 0x000C
IMAGE_SYM_CLASS_WEAK_EXTERNAL = 0x0069
IMAGE_SYM_DEBUG = -2                                         # Symbol is a special debug item.
IMAGE_SYM_DTYPE_ARRAY = 3                                    # array.
IMAGE_SYM_DTYPE_FUNCTION = 2                                 # function.
IMAGE_SYM_DTYPE_NULL = 0                                     # no derived type.
IMAGE_SYM_DTYPE_POINTER = 1                                  # pointer.
IMAGE_SYM_SECTION_MAX = 0xFEFF                               # Values 0xFF00-0xFFFF are special
IMAGE_SYM_SECTION_MAX_EX = 0xFFFFFFFF
IMAGE_SYM_TYPE_CHAR = 0x0002                                 # type character.
IMAGE_SYM_TYPE_DOUBLE = 0x0007
IMAGE_SYM_TYPE_ENUM = 0x000A                                 # enumeration.
IMAGE_SYM_TYPE_FLOAT = 0x0006
IMAGE_SYM_TYPE_INT = 0x0004
IMAGE_SYM_TYPE_LONG = 0x0005
IMAGE_SYM_TYPE_MOE = 0x000B                                  # member of enumeration.
IMAGE_SYM_TYPE_NULL = 0x0000                                 # no type.
IMAGE_SYM_TYPE_PCODE = 0x8000
IMAGE_SYM_TYPE_SHORT = 0x0003                                # type short integer.
IMAGE_SYM_TYPE_STRUCT = 0x0008
IMAGE_SYM_TYPE_UCHAR = 0x000C
IMAGE_SYM_TYPE_UINT = 0x000E
IMAGE_SYM_TYPE_ULONG = 0x000F
IMAGE_SYM_TYPE_UNION = 0x0009
IMAGE_SYM_TYPE_USHORT = 0x000D
IMAGE_SYM_TYPE_VOID = 0x0001
IMAGE_SYM_UNDEFINED = 0                                      # Symbol is undefined or is common.
IMAGE_VXD_SIGNATURE = 0x454C                                 # LE

RT_CURSOR = 1
RT_BITMAP = 2
RT_ICON = 3
RT_MENU = 4
RT_DIALOG = 5
RT_STRING = 6
RT_FONTDIR = 7
RT_FONT = 8
RT_ACCELERATOR = 9
RT_RCDATA = 10
RT_MESSAGETABLE = 11
RT_VERSION = 16
RT_DLGINCLUDE = 17
RT_PLUGPLAY = 19
RT_VXD = 20
RT_ANICURSOR = 21
RT_ANIICON = 22
RT_HTML = 23
RT_MANIFEST = 24
RT_GROUP_CURSOR = RT_CURSOR + 11
RT_GROUP_ICON = RT_ICON + 12

RESOURCE_TYPE = {
    RT_CURSOR: 'CURSOR',
    RT_BITMAP: 'BITMAP',
    RT_ICON: 'ICON',
    RT_MENU: 'MENU',
    RT_DIALOG: 'DIALOG',
    RT_STRING: 'STRING',
    RT_FONTDIR: 'FONTDIR',
    RT_FONT: 'FONT',
    RT_ACCELERATOR: 'ACCELERATOR',
    RT_RCDATA: 'RCDATA',
    RT_MESSAGETABLE: 'MESSAGETABLE',
    RT_VERSION: 'VERSION',
    RT_DLGINCLUDE: 'DLGINCLUDE',
    RT_PLUGPLAY: 'PLUGPLAY',
    RT_VXD: 'VXD',
    RT_ANICURSOR: 'ANICURSOR',
    RT_ANIICON: 'ANIICON',
    RT_HTML: 'HTML',
    RT_MANIFEST: 'MANIFEST',
    RT_GROUP_CURSOR: 'GROUP_CURSOR',
    RT_GROUP_ICON: 'GROUP_ICON',
    }


def init_rva2offs(self):
    """
    Post-parse for each SectionHeader entry.
    """
    pe = self.parent.parent
    if not hasattr(pe, '_r2o_sections'):
        pe._r2o_sections = []
        pe.last_va_offset = 0
    s = (self.PointerToRawData.value, self.SizeOfRawData.value, self.VirtualAddress.value, self.VirtualSize.value)
    pe._r2o_sections.append(s)
    pe.last_va_offset = max(s[0] + s[1], pe.last_va_offset)


def rva2offs(self, rva):
    """
    Convert an RVA to an offset.

    Note: this will be attached as a method to PE objects.
    """
    if not hasattr(self, '_r2o_sections'):
        raise ValueError('rva2offs is only available after PE.NTHeader.SectionHeaders have been parsed!')
    if hasattr(rva, 'value'):
        rva = rva.value
    for s in self._r2o_sections:
        if s[2] <= rva < s[2] + s[3]:
            res = rva - s[2] + s[0]
            dbg(f'RVA: 0x{rva:X} => offset 0x{res:X}', 3)
            return res
    dbg(f'RVA: 0x{rva:X} => None', 3)


def parse_exports(self):
    """
    Parse PE exports.
    """
    if not self.NTHeader.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress.value:
        return
    exp_dir = self.NTHeader.ExportDirectory
    num_names, num_funs = exp_dir.NumberOfNames.value, exp_dir.NumberOfFunctions.value
    base = exp_dir.Base.value
    fmt = '<' + 'I' * num_names
    offs = self.rva2offs(exp_dir.AddressOfNames)
    name_rvas = struct.unpack(fmt, self.dataview[offs:offs + struct.calcsize(fmt)])
    fmt = '<' + 'I' * num_funs
    offs = self.rva2offs(exp_dir.AddressOfFunctions)
    fun_rvas = struct.unpack(fmt, self.dataview[offs:offs + struct.calcsize(fmt)])
    fmt = '<' + 'H' * num_names
    offs = self.rva2offs(exp_dir.AddressOfNameOrdinals)
    name_ordinals = struct.unpack(fmt, self.dataview[offs:offs + struct.calcsize(fmt)])
    exports = {exp_dir.Base.value + i:{} for i in range(num_funs)}
    for i, (ordinal, e) in enumerate(exports.items()):
        e['Ordinal'] = ordinal
        e['FunctionRVA'] = fun_rvas[i]
        e['FunctionOffset'] = self.rva2offs(fun_rvas[i])
    for i, ordinal in enumerate(name_ordinals):
        ordinal += base
        name_rva = name_rvas[i]
        name_offs = self.rva2offs(name_rva)
        name = AS(name='_', offset=name_offs, dataview=self.dataview).value
        exports[ordinal]['Name'] = name
    self.Exports = exports


def parse_resources(self):
    """
    Parse PE resources.
    """
    rva = self.NTHeader.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_RESOURCE].VirtualAddress.value
    if not rva:
        return
    ...


def pe_post_parse(self):
    """
    Parse more complicated structures in the PE.
    """
    self._size = max(s[0] + s[1] for s in self._r2o_sections)
    parse_exports(self)
    parse_resources(self)
