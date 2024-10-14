# automatically generated from socks.vs2

from libvstruct2 import B, DynExpr, I2B, VStruct


class Socks5CAuth(VStruct):
    FIELDS = [
        {'name': 'Ver', 'type': B},
        {'name': 'IdLen', 'type': B},
        {'name': 'ID', 'count': DynExpr('$IdLen'), 'type': B},
        {'name': 'PwLen', 'type': B},
        {'name': 'PW', 'count': DynExpr('$PwLen'), 'type': B},
    ]


class Socks5AuthResp(VStruct):
    SFORMAT = 'BB'
    SOFFSETS = [0, 1, 2]
    FIELDS = [
        {'name': 'Ver', 'type': B},
        {'name': 'Status', 'type': B},
    ]


class Socks5Domain(VStruct):
    FIELDS = [
        {'name': 'Len', 'type': B},
        {'name': 'Domain', 'count': DynExpr('$Len'), 'type': B},
    ]


class Socks5Address(VStruct):
    FIELDS = [
        {'name': 'Type', 'type': B},
        {'name': 'IPv4Addr', 'count': 4, 'type': B, 'condition': '$Type == 1'},
        {'name': 'Domain', 'type': Socks5Domain, 'condition': '$Type == 3'},
        {'name': 'IPv6Addr', 'count': 16, 'type': B, 'condition': '$Type == 4'},
    ]


class Socks5ConnReq(VStruct):
    FIELDS = [
        {'name': 'Ver', 'type': B},
        {'name': 'Command', 'type': B, 'validator': (1, 2, 3), 'formatter': {1: 'TCP-connect', 2: 'TCP-bind', 3: 'UDP-associate'}},
        {'name': 'Reserved', 'type': B, 'validator': 0},
        {'name': 'DstAddr', 'type': Socks5Address},
        {'name': 'DstPort', 'type': I2B},
    ]


class Socks5ConnResp(VStruct):
    FIELDS = [
        {'name': 'Ver', 'type': B},
        {'name': 'Status', 'type': B, 'formatter': {0: 'granted', 1: 'general failure', 2: 'not allowed', 3: 'net unreachable', 4: 'host unreachable', 5: 'conn refused', 6: 'TTL expired', 7: 'protocol error', 8: 'addr type not supported'}},
        {'name': 'Reserved', 'type': B, 'validator': 0},
        {'name': 'BndAddr', 'condition': DynExpr(' $^ConnReq.Command == 2 '), 'type': Socks5Address},
        {'name': 'BndPort', 'condition': DynExpr(' $^ConnReq.Command == 2 '), 'type': I2B},
    ]


class Socks5CGreet(VStruct):
    FIELDS = [
        {'name': 'Ver', 'type': B, 'validator': 5},
        {'name': 'NAuth', 'type': B},
        {'name': 'Auth', 'count': DynExpr('$NAuth'), 'type': B},
    ]


class Socks5SChoice(VStruct):
    SFORMAT = 'BB'
    SOFFSETS = [0, 1, 2]
    FIELDS = [
        {'name': 'Ver', 'type': B, 'validator': 5},
        {'name': 'CAuth', 'type': B},
    ]


class SOCKS5(VStruct):
    ROOT = True
    FILETYPES = ('socks5',)
    FILTER = '^\\x05'
    FIELDS = [
        {'name': 'ClientGreet', 'type': Socks5CGreet},
        {'name': 'ServerChoice', 'type': Socks5SChoice},
        {'name': 'Auth', 'condition': DynExpr('$ServerChoice.CAuth != 0'), 'type': Socks5CAuth},
        {'name': 'AuthResp', 'condition': DynExpr('$ServerChoice.CAuth != 0'), 'type': Socks5AuthResp},
        {'name': 'ConnReq', 'type': Socks5ConnReq},
        {'name': 'ConnResp', 'type': Socks5ConnResp},
        {'name': 'Data', 'count': 128, 'type': B},
    ]


class SOCKS5Client(VStruct):
    ROOT = True
    FILETYPES = ('socks5client',)
    FILTER = '^\\x05'
    FIELDS = [
        {'name': 'ClientGreet', 'type': Socks5CGreet},
        {'name': 'ConnReq', 'type': Socks5ConnReq},
        {'name': 'Data', 'count': DynExpr('*'), 'type': B},
    ]


class SOCKS5Server(VStruct):
    ROOT = True
    FILETYPES = ('socks5server',)
    FILTER = '^\\x05'
    FIELDS = [
        {'name': 'ServerChoice', 'type': Socks5SChoice},
        {'name': 'ConnResp', 'type': Socks5ConnResp},
        {'name': 'Data', 'count': DynExpr('*'), 'type': B},
    ]


