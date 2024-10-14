"""
vstruct2: .vs2 and .vs2.py definition parser & converter (YAML-like).

WARNING: definition files contain live Python code - only accept definition files from trusted
sources!

Author: Vlad Topan (vtopan/gmail).
"""
import ast
import glob
import os
import re
import struct

from .logging import log, dbg, err
from .basefields import BASE_TYPES
import libvstruct2 as vs2


CTX_NORMAL = 1
CTX_MULTILINE = 2

MARKER = 'vs2'
VS2_PREFIX = f'{MARKER}_'

PFX_MAP = {
    '=': 'validator',
    '@': 'dyn_offset',
    '~': 'formatter',
    '?=': 'should_be',
    '.': 'hidden',
    '"': 'description',
    '{': 'bit_map',
    '?': 'lookahead',
    '*': 'out_of_struct',
    '!': 'required',
    ';': 'post_parse',
    ':': 'post_parse_value',
    '<': 'condition',
    }
FLAGS = ('hidden', 'lookahead', 'out_of_struct', 'required', 'update_offset', 'second_pass')

RX = {
    'line': (r'^(?:([\t ]+)(\?=|[<!:;*{"~=@?\.|-]|in))?(?:\s*(\w+)\s*:([=:]?)\s*)?(.*)$',),
    }
for k in RX:
    RX[k] = re.compile(*RX[k])


class DefLoader:
    """
    Load VStruct from definitions (.vs2 + optional .vs2.py).

    In both `source` and `dest`, '$proj' is replaced with the project path.

    :param sources: Source file glob pattern or list.
    :param dest: Destination folder name.
    """

    def __init__(self, sources=f'$proj/defs/*.{MARKER}', dest='$proj/vstructs'):
        self.defs = []
        proj = os.path.dirname(__file__)
        self.sources = sources.replace('$proj', proj)
        self.dest = dest.replace('$proj', proj)


    def load(self):
        """
        Load all given sources.
        """
        if type(self.sources) in (list, tuple):
            lst = self.sources
        else:
            lst = glob.glob(self.sources)
        for f in lst:
            self.load_def(f)


    def load_def(self, source):
        """
        Load .vs2 definition file (+optional .vs2.py).
        """
        def line_err(msg):
            return ValueError(f'{srcname}[{lineno}]: {msg}!\nLine: {line}')

        if not os.path.isfile(source):
            raise ValueError(f'Invalid/missing source file [{source}]!')
        dbg(f'Parsing {source}...')
        srcname = os.path.basename(source)
        py_source = source + '.py'
        extra_code = open(py_source).read() if os.path.isfile(py_source) else None
        structs = []
        crt_indent, crt_struct = None, {}
        context = CTX_NORMAL
        for i, line in enumerate(open(source)):
            lineno = i + 1
            # ignore comments
            if '#' in line:
                line = line[:line.find('#')]
            # ignore blank lines
            if not line.strip():
                continue
            if context == CTX_MULTILINE:
                # on an expression continuation line
                multiline += ' ' + line.lstrip(' ')
                if multiline.rstrip().endswith('}'):
                    line = multiline
                    context = CTX_NORMAL
                else:
                    continue
            m = RX['line'].search(line)
            if not m:
                raise line_err('invalid line')
            indent, pfx, name, is_root_or_eval, rest = m.groups()
            if pfx == '{':
                if not line.rstrip().endswith('}'):
                    # multiline expression
                    context = CTX_MULTILINE
                    multiline = line.rstrip()
                    continue
                elif name:
                    rest, name = f'{name}: {rest}', None
            if not indent:
                # new top-level structure
                if crt_struct:
                    structs.append(crt_struct)
                crt_struct = {'name': name, 'fields': [], 'attrs':{}}
                crt_indent = None
                if is_root_or_eval:
                    crt_struct['root'] = True
                    if rest:
                        crt_struct['filetypes'] = tuple(x.strip() for x in rest.split(','))
                elif rest:
                    raise line_err(f'extraneous data "{rest}"')
                continue
            elif not crt_indent:
                crt_indent = indent
            if len(indent) < len(crt_indent):
                raise line_err(f'invalid indent')
            if rest and rest.strip() in FLAGS:
                # field flag
                crt_field['flags'] |= getattr(vs2, 'FLG_' + rest.strip().upper())
                continue
            if pfx == '<':
                rest = rest.strip(' <>')
            pfx = PFX_MAP.get(pfx, pfx)
            if indent == crt_indent:
                if pfx == '|':    # class attribute
                    crt_struct['attrs'][name] = rest.strip()
                    continue
                # new field
                if not name:
                    raise line_err(f'missing field name')
                crt_field = {'name': name, 'flags': 0}
                if is_root_or_eval:
                    # Eval field
                    crt_field['expression'] = rest.strip()
                    crt_field['type'] = 'Eval'
                    rest = None
                    pfx = 'out_of_struct'
                if rest:
                    # todo: rest == '[' => multiple types
                    for c1, c2, attr_name in [
                            ('[', ']', 'count'),
                            ('<', '>', 'condition'),
                        ]:
                        if re.search(r'^\s*[\'"]?\w+[\'"]?\s*' + re.escape(c1) + '.+' + re.escape(c2) + r'\s*$', rest):
                            rest, attr = rest.rstrip(' \t\r\n')[:-1].split(c1, 1)
                            attr = vs2.const_or_DynExpr(attr)
                            crt_field[attr_name] = attr
                    crt_field['type'] = rest.strip()
                    if crt_field['type'] in vs2.BASE_STRING_TYPES or crt_field['type'] in vs2.BASE_REGEX_TYPES:
                        # string field
                        length = crt_field.pop('count', None)
                        if isinstance(length, str):
                            m = re.search(r'^\s*<\s*(.+)', length, flags=re.I)
                            if m:
                                crt_field['maxlen'] = vs2.const_or_DynExpr(m.groups()[0])
                                length = None
                        if length:
                            crt_field['length'] = length
                if pfx in FLAGS:
                    crt_field['flags'] |= getattr(vs2, 'FLG_' + pfx.upper())
                crt_struct['fields'].append(crt_field)
            else:
                # extra field info
                rest = rest.strip()
                if pfx == 'description':
                    if not rest.endswith('"'):
                        raise line_err(f'missing trailing quote (")')
                    rest = rest[:-1]
                if pfx in ['in', 'validator', 'bit_map'] or name in ['endianness', 'maxlen']:
                    if pfx == 'bit_map':
                        rest = '{ ' + rest
                    # handle exponentiation to allow literal eval
                    rest = re.sub(r'\d+\s*\*\*\s*\d+', lambda m:str(eval(m.group())), rest)
                    rest = vs2.const_or_DynExpr(rest)
                if pfx in ('should_be', 'stop'):
                    rest = vs2.const_or_DynExpr(rest)
                crt_field[pfx if pfx != '-' else name] = rest
        if crt_struct:
            structs.append(crt_struct)
        # compute SFORMAT for VStructs (where possible)
        for s in structs:
            fields = s['fields']
            formats = [(f.get('count') is None and (f.get('sformat') or getattr(getattr(vs2, f['type'], None), 'SFORMAT', None))) for f in fields]
            if not all(formats):
                continue
            ends = [getattr(getattr(vs2, f['type'], None), 'ENDIANNESS', None) for f in fields]
            if '>' in ends and '<' in ends:
                continue
            s['soffsets'] = [0] + [struct.calcsize('=' + ''.join(formats[:i + 1])) for i in range(len(fields))]
            s['sformat'] = ''.join(formats)
            endianness = [x for x in ends if x]
            if endianness:
                s['endianness'] = endianness[0]
        vsdef = {'structs': structs, 'extra_code': extra_code}
        vsdef['source'] = os.path.basename(source).rsplit('.', 1)[0]
        self.defs.append(vsdef)


    def save(self):
        """
        Save the loaded defs to vstruct2 sources.
        """
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        filetype_map, root_vstructs = {}, {}
        for vsdef in self.defs:
            base_types_used = set(['VStruct'])
            extra_imports = set()
            lib = f'{MARKER}_{vsdef["source"]}'
            dst_fn = os.path.join(self.dest, f'{lib}.py')
            log(f'Creating [{dst_fn}]...')
            h = open(dst_fn, 'w')
            h.write(f'# automatically generated from {vsdef["source"]}.{MARKER}\n\n')
            lines = []
            if vsdef['extra_code']:
                lines.append(vsdef['extra_code'].strip() + '\n\n\n')
            for s in vsdef['structs']:
                lines.append(f'class {s["name"]}(VStruct):\n')
                for attr in ('root', 'filetypes', 'sformat', 'soffsets', 'endianness'):
                    if s.get(attr):
                        lines.append(f'    {attr.upper()} = {repr(s[attr])}\n')
                        if attr == 'filetypes':
                            for e in s[attr]:
                                filetype_map[e] = (lib, s['name'])
                        elif attr == 'root':
                            if lib not in root_vstructs:
                                root_vstructs[lib] = []
                            root_vstructs[lib].append(s['name'])
                methods = s['attrs'].pop('methods', '').split(',')
                for k, v in s['attrs'].items():
                    if k in ('post_parse',):
                        lines.append(f'    {k.upper()} = {v}\n')
                    else:
                        lines.append(f'    {k.upper()} = {repr(v)}\n')
                lines.append('    FIELDS = [\n')
                for field in s['fields']:
                    if field.get('dyn_offset'):
                        field['flags'] |= vs2.FLG_OUT_OF_STRUCT
                    if 'flags' in field and not field['flags']:
                        del field['flags']
                    if field['type'] in vs2.BASE_REGEX_TYPES and 'condition' in field:
                        field['regex'] = field.pop('condition')
                        if field['type'] in ('T', 'Token'):
                            field['regex'] = '\\s*(' + '|'.join(re.escape(e.strip()) for e in field['regex'].split(',')) + ')\\s*'
                    if 'regex' in field:
                        extra_imports.add('re')
                        flags = field.pop('regex_flags', None)
                        value = 're.compile(b' + repr(field['regex'])
                        if flags:
                            value += ', flags=' + ' | '.join(f're.{e}' for e in flags)
                        field['regex'] = value + ')'
                    attrs = []
                    for k, v in field.items():
                        if k not in ('type', 'regex'):
                            if isinstance(v, vs2.DynExpr):
                                v = f'DynExpr({repr(v)})'
                                base_types_used.add('DynExpr')
                            elif k not in ('length', 'formatter', 'post_parse', 'post_parse_value'):
                                v = repr(v)
                        attrs.append(f"'{k}': {v}")
                    attrs = '{%s}' % ', '.join(attrs)
                    lines.append(f'        {attrs},\n')
                    ftype = field['type']
                    if ftype in BASE_TYPES:
                        base_types_used.add(ftype)
                lines.append('    ]\n')
                if methods:
                    lines.append('\n')
                    for e in methods:
                        e = e.strip()
                        if not e:
                            continue
                        lines.append(f'    {e} = {e}\n')
                lines.append('\n')
            if base_types_used:
                h.write(f'from libvstruct2 import {", ".join(sorted(base_types_used))}\n\n')
            h.write('\n')
            if extra_imports:
                h.write(''.join(f'import {e}\n' for e in sorted(extra_imports)))
            for line in lines:
                h.write(line)
            h.close()
        dst_fn = os.path.join(self.dest, '__init__.py')
        h = open(dst_fn, 'w')
        h.write('# automatically generated from definition files\n\n')
        for k, v in sorted(root_vstructs.items()):
            h.write(f'from .{k} import {", ".join(sorted(v))}\n')
        h.write('\n')
        h.write(f'ROOT_PARSERS = [{", ".join(sorted(e for p in root_vstructs.values() for e in p))}]\n\n')
        h.write('FT_MAP = {\n')
        for k, v in sorted(filetype_map.items()):
            h.write(f'    {repr(k)}: ({repr(v[0])}, {v[1]}),\n')
        h.write('    }\n\n')
        h.close()
