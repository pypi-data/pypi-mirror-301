"""
vstruct2: Template structure and field classes.

Actual structures are extracted from *.vs2 files and automagically instantiated from VStruct.
"""

import libvstruct2 as vs2

import ast
from inspect import getmodule
import math
import re
import struct


DEFAULT_MAX_REGEX = 64 * 1024
DEFAULT_ENDIANNESS = '<'
ATTRMAP = {'&': '', '$': '.value', '@': '.offset', ':': '.size'}
FLG_HIDDEN = 0x0001                                 # don't show field when displaying the structure (for internal/debug fields)
FLG_OUT_OF_STRUCT = 0x0002                          # field is at an offset outside the current structure
FLG_LOOKAHEAD = FLG_HIDDEN | FLG_OUT_OF_STRUCT
FLG_REQUIRED = 0x0004                               # field must be present
FLG_UPDATE_OFFSET = 0x0008                          # forcibly update parent's current offset based on this field
FLG_SECOND_PASS = 0x0010                            # only parse this on the second pass

class ParseError(ValueError): pass
class ValidationError(ParseError): pass


class DynExpr(str):
    """
    Dynamic expression - will be evaluated at runtime.
    """


class VSBase:
    """
    Base class for VStruct and Field.
    """
    SFORMAT = None
    ENDIANNESS = None


    def __init__(self, name, description=None, parent=None, offset=0, size=None, dataview=None, lazy=None, sformat=None,
                endianness=None, value=None, flags=0, validator=None, condition=None, count=None, regex=None, **kwargs):
        self._present = True        # set to False in .parse if not present
        self.flags = flags
        self.name = name
        self.description = description
        self.lazy = lazy
        self.offset = offset
        self._size = size
        self._fields = []
        self.set_parent(parent)
        if isinstance(endianness, DynExpr):
            endianness = self.parent.eval(endianness)
        self._fieldmap = {}
        self.condition = condition
        self.count = count
        self.endianness = endianness or getattr(self.parent, 'endianness', None) or getattr(self.__class__, 'ENDIANNESS', None)
        self.has_second_pass = False
        self.parsing = False
        self._next_field_number = -1
        self.regex = regex or getattr(self.__class__, 'REGEX', None)
        if type(self.regex) in (str, bytes):
            self.regex = re.compile(self.regex)
        if sformat or self.__class__.SFORMAT:
            self.sformat = (self.endianness or DEFAULT_ENDIANNESS) + (sformat or self.__class__.SFORMAT)
        else:
            self.sformat = None
        self.unusual_value = False
        if dataview:
            self.dataview = dataview
        if self.lazy is None:
            self.lazy = True
        self._parsed = False
        self.validator = validator
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.value = value
        if not self.lazy and not self._parsed:
            self.parse()


    def parse(self, silent_fail=False):
        """
        Call ._parse() in a try..except and call *post_parse after.
        """
        try:
            self._parse()
            if not self._present and self.flags & FLG_REQUIRED:
                raise ParseError(f'Required field {self.name} @ 0x{self.offset:X} is missing!')
            self._parsed = True     # must be marked here to allow *_post_parse() to use .value
            if hasattr(self, 'post_parse_value') and self._present:
                # extra processing on the value
                ppv = self.post_parse_value
                if type(ppv) in (list, tuple):
                    self._value = [ppv[i](e) for i, e in enumerate(self._value)]
                else:
                    self._value = ppv(self)     # API change: pass a reference to the actual object, not just the value
                    vs2.dbg(f'{self.depth * "  "}Value of {self.name} post-processed to {self.formatted_value()}')
            if hasattr(self.__class__, 'POST_PARSE'):
                # post parsing trigger / hook
                self.__class__.POST_PARSE(self)
            if hasattr(self, '_post_parse'):
                # internal post parsing trigger / hook
                self._post_parse()
            if hasattr(self, 'post_parse'):
                # post parsing trigger / hook
                self.post_parse(self)
            if self.field_number < 0x10 and not isinstance(self, VStruct):
                vs2.dbg(f'{self.depth * "  "}  => {self.format().rstrip()}')
        except Exception as e:
            vs2.err(f'Failed parsing {self.name} @ {self.offset}: {e}')
            if not silent_fail:
                raise


    def __getitem__(self, key):
        """
        Emulate dictionary.
        """
        if not self._parsed:
            self.parse()
        return self._fieldmap[key]


    def next_field_number(self):
        """
        Each field gets a sequential number.
        """
        self._next_field_number += 1
        return self._next_field_number


    def set_parent(self, parent):
        """
        Set the parent (and the inheritable attributes, if any).

        Note: this will be called on fields which may not be present - don't change anything in .parent!
        """
        self.parent = parent
        if parent:
            self.dataview = parent.dataview
            if self.lazy is None:
                self.lazy = parent.lazy
            # compute depth & full name
            name_parts = [self.name]
            self.depth = 0
            obj = self
            while obj.parent:
                obj = obj.parent
                self.depth += 1
                name_parts.insert(0, obj.name)
            self.root = obj
            self.full_name = '.'.join(name_parts)
            self.field_number = self.parent.next_field_number()
        else:
            self.depth = 0
            self.full_name = self.name
            self.field_number = 0


    def first_parent(self, type_or_typename):
        """
        Returns the first (grand)parent of the given type name.
        """
        if type(type_or_typename) is not str:
            type_or_typename = type_or_typename.__class__.__name__
        obj = self
        while obj and obj.__class__.__name__ != type_or_typename:
            obj = obj.parent
        return obj


    def last_parent(self, type_or_typename):
        """
        Returns the last / most top-level (grand)parent of the given type name.
        """
        if type(type_or_typename) is not str:
            type_or_typename = type_or_typename.__class__.__name__
        obj, gp = self, None
        while obj:
            obj = obj.parent
            if obj.__class__.__name__ == type_or_typename:
                gp = obj
        return gp


    @property
    def size(self):
        if not self._parsed:
            self.parse()
        return self._size


    @property
    def value(self):
        if not self._parsed:
            self.parse()
        return self._value


    @property
    def present(self):
        if not self._parsed:
            self.parse()
        return self._present


    @value.setter
    def value(self, value):
        if value is None:
            self._value = value
            return
        # fixme: move validation to .parse(), after calling *_post_parse() hooks
        validator = getattr(self, 'validator', getattr(self.__class__, 'VALIDATOR', None))
        if validator:
            if isinstance(validator, DynExpr):  # fixme: validator DynExpr is either True/False or a dict/list/etc., not both
                if not self.eval(validator):
                    raise ValidationError(f'Value {value} of {self.parent.name}.{self.name} is invalid!')
            elif not self.validate(value, validator):
                raise ValidationError(f'Value {value} of {self.parent.name}.{self.name} is invalid!')
        validator = getattr(self, 'should_be', getattr(self.__class__, 'SHOULD_BE', None))
        if validator and not self.validate(value, validator):
            vs2.warn(f'Value {value} of {self.parent.name}.{self.name} is unusual/invalid!')
            self.unusual_value = True
        self._value = value
        # self._parsed = True   # DON'T - this marks partially-parsed (for .parse_struct) fields as parsed


    def validate(self, value, validator):
        """
        Check a value with the given validator.

        :param validator: A sequence (list, tuple or dict), a function (must return True if valid), a DynExpr() or an exact value.
        """
        if isinstance(validator, DynExpr):
            self.eval(validator)
        if isinstance(validator, (list, tuple, dict)):
            if value not in validator:
                return False
        elif hasattr(validator, '__call__'):
            if not validator(value):
                return False
        elif value != validator:
            return False
        return True


    def parse_struct(self):
        """
        Parse this field/structure as a Python struct (if possible).
        """
        if self.sformat:
            try:
                self._size = struct.calcsize(self.sformat)
                if self.field_number < 0x10:
                    vs2.dbg(f'{self.depth * "  "}Unpacking {self.name}: {self.sformat} ({self._size} bytes) @ {self.offset} (0x{self.offset:X})...')
                value = struct.unpack(self.sformat, self.dataview[self.offset:self.offset + self._size])
                if isinstance(self, Field) and len(self.sformat.lstrip('0123456789<>=@')) == 1:  # this will bite at some point
                    value = value[0]
                self.value = value
                self.soffsets = getattr(self.__class__, 'SOFFSETS', None)
            except struct.error as e:
                vs2.err(f'Failed parsing {self.name}:struct({self.sformat}) @ 0x{self.offset:X}!')
                raise
            return self._size
        raise NotImplementedError(f'This function must be overriden in custom fields/structures ({self.name}:{self.__class__.__name__})!')


    def parse_regex(self):
        """
        Parse this field/structure as a regex.
        """
        self.parsing = True
        maxlen = getattr(self, 'maxlen', DEFAULT_MAX_REGEX)
        if isinstance(maxlen, DynExpr):
            maxlen = self.parent.eval(maxlen)
        offset = self.parent.crt_offset
        if getattr(self, 'length', None):
            length = self.parent.eval(self.length) if isinstance(self.length, DynExpr) else self.length
        else:
            length = len(self.dataview) - offset
        if maxlen and maxlen > 0 and length > maxlen:
            length = maxlen
        buffer = self.dataview[offset:offset + length]
        m = self.regex.search(buffer)
        if m:
            self.offset = offset + m.start()
            self.raw_match = m.group()
            self._size = len(self.raw_match)
            value = m.groups() or self.raw_match
            if type(value) is tuple and len(value) == 1:
                value = value[0]
            self.value = value
        else:
            self._present = False
            self._size = 0
        self.parsing = False
        return self._size


    def set_crt_offset(self, offset):
        """
        Set the current offset (and the .bytes_left attribute).
        """
        vs2.dbg(f'Current offset: 0x{offset:X} ({offset})', 2)
        if type(offset) is not int:
            raise ValueError(f'Invalid offset: {offset}!')
        self.data_available = offset < len(self.dataview)
        self.crt_offset = offset
        self.bytes_left = len(self.dataview) - self.crt_offset


    def eval(self, expr, silent=False):
        """
        Evaluate a dynamic expression in the context of the current struct/field.
        """
        m = re.search(r'^\s*([@:]*)/(.+)/([msif])*\s*(.*)', expr)
        if m:
            # regex
            op, expr, flags, rest = m.groups()
            flags = {k:getattr(re, k.upper(), 0xFFFF) for k in (flags or '')}
            offs = self.crt_offset
            end = len(self.dataview) if flags.pop('f', None) else offs + 8192
            vs2.dbg(f'{self.depth * "  "}<{self.full_name}> Evaluating the regex expression {expr} in data[0x{offs:X}:0x{end:X}] = {self.dataview[offs:offs+16]}...')
            m = re.search(expr.encode('ascii'), self.dataview[offs:end], flags=sum(flags.values()))
            if op == '@':
                res = (offs + m.start()) if m else -1
            elif op == ':':
                res = (m.end() - m.start()) if m else 0
            else:
                res = bool(m)
            vs2.dbg(f'{self.depth * "  "}  => {res} (0x{res if isinstance(res, int) else 0:X})')
            return self.eval(f'{repr(res)} {rest}') if rest else res
        expr = re.sub(r'[:&@\$](\^*)([\.\w\[\]]+)',
                lambda m:rf'self{len(m.group(1)) * ".parent"}.{m.group(2)}{ATTRMAP[m.group()[0]]}', expr)
                # removed {"."*bool(m.group(2))} and made the attribute name (.group(2)) required - shouldn't break anything
        vs2.dbg(f'{self.depth * "  "}<{self.full_name}> Evaluating the expression {expr} @ 0x{self.crt_offset:X}...')
        env = {'self': self}
        env.update(getmodule(self.__class__).__dict__)
        try:
            res = eval(expr, globals(), env)
        except Exception as e:
            raise ValueError(f'Failed evaluating expression: {expr} => {repr(e)}')
        vs2.dbg(f'{self.depth * "  "}  => {res} (0x{res if isinstance(res, int) else 0:X})')
        return res



class VStruct(VSBase):
    """
    Structure template.
    """
    IS_ROOT = False


    @property
    def fields(self):
        if not self._parsed:
            self.parse()
        return self._fields


    def add_field(self, field):
        """
        Add a field (Field or VStruct).
        """
        self._fieldmap[len(self._fields)] = field
        self._fields.append(field)
        if hasattr(field, 'alias'):
            setattr(self, field.alias, field)
            self._fieldmap[field.alias] = field
        name = getattr(field, 'name', None) if type(field) is not list else getattr(field[0], 'name', None)
        if name:
            setattr(self, name, field)
            self._fieldmap[name] = field


    def _parse(self, second_pass=False):
        """
        Parse this VStruct. Must call .add_field() for each field and set ._size.

        :return: The size of the struct.
        """
        if self.parsing and not second_pass:
            raise RuntimeError('.parse() called itself recursively - probably a property access inside .parse()!')
        if self.flags & FLG_SECOND_PASS and  self.flags & FLG_OUT_OF_STRUCT and not second_pass:
            vs2.dbg(f'{self.depth * "  "}Skipping struct {self.name} until second pass...', 10)
            self.has_second_pass = True
            return
        self.parsing = True
        self._fields = []
        self.set_crt_offset(self.offset)
        self._size = 0
        if self.sformat:
            self.parse_struct()
            for i in range(len(self.__class__.FIELDS)):
                fattr = self.__class__.FIELDS[i]
                self.set_crt_offset(self.offset + self.soffsets[i])
                field = fattr['type'](offset=self.crt_offset, value=self._value[i],
                        size=self.soffsets[i + 1] - self.soffsets[i], parent=self, is_array=False,
                        **fattr)
                # todo: handle field arrays
                self.add_field(field)
            self._size = self.soffsets[-1]
            self.parsing = False
            return self._size
        for fattr in self.__class__.FIELDS:
            vs2.dbg(f'{self.depth * "  "}Doing field {fattr["name"]} in {self.name}...', 10)
            flags = fattr.get('flags', 0)
            ftype = fattr['type']
            if type(ftype) is str:
                ftype = VStruct.map[ftype]
            dyn_offset = fattr.get('dyn_offset')
            if dyn_offset:
                flags |= FLG_OUT_OF_STRUCT
            condition = fattr.get('condition')
            count = fattr.get('count')
            is_array = bool(count)
            is_regex = fattr.get('regex')
            first = True
            old_field_offset, keep_field_offset = self.crt_offset, False
            for self.field_index in range(100000):
                if dyn_offset:
                    new_offset = self.eval(dyn_offset)
                    if new_offset is None or new_offset < 0:
                        # None or negative offset means not present
                        vs2.dbg(f'{self.depth * "  "}Field {fattr["name"]} not present (null or negative offset).', 2)
                        break
                    self.set_crt_offset(new_offset)
                if condition:
                    if not self.eval(condition):
                        vs2.dbg(f'{self.depth * "  "}Field {fattr["name"]} not present.', 2)
                        break
                if count is not None:
                    if count == '*':
                        count = True
                    elif isinstance(count, DynExpr):
                        cvalue = self.eval(count)
                        if not cvalue:
                            break
                        if type(cvalue) is int:
                            count = cvalue
                    if type(count) is int:
                        if count < 1:
                            break
                if not self.bytes_left:
                    if type(count) is not bool:
                        # field[True] means parse as long as the buffer doesn't end; in all other cases warn about it
                        vs2.warn('Buffer ended!')
                    break
                fattr['flags'] = flags
                self.crt_field = field = ftype(parent=self, offset=self.crt_offset, lazy=False, is_array=is_array, **fattr)
                if not field.present:
                    break
                if field.has_second_pass:
                    self.has_second_pass = True
                if is_array:
                    if first:
                        self.add_field([field])
                        first = False
                    else:
                        self._fields[-1].append(field)
                else:
                    self.add_field(field)
                if flags & FLG_UPDATE_OFFSET or not (flags & FLG_OUT_OF_STRUCT):
                    if field.offset >= self.offset:
                        keep_field_offset = True
                        self._size = field.offset + field._size - self.offset
                if field._size:
                    self.set_crt_offset(field.offset + field._size)
                if count:
                    if type(count) is int:
                        count -= 1
                else:
                    break
                if fattr.get('stop'):
                    if self.eval(fattr['stop']):
                        break
            else:
                raise ParseError(f'Structure {self.name} @ 0x{self.offset:X} has overflown the maximum number of fields!')
            if not keep_field_offset:
                self.set_crt_offset(old_field_offset)
        if self.has_second_pass and not self.parent:
            self.do_second_pass()
        self.parsing = False
        return self._size


    def do_second_pass(self):
        """
        Second pass of parsing (if required).
        """
        for field in self._fields:
            if isinstance(field, list):
                for e in field:
                    e.do_second_pass()
            elif field.flags & FLG_SECOND_PASS and not field._parsed:
                vs2.dbg(f'{field.depth * "  "}Parsing field {field.name} in {self.name} @ second pass...', 10)
                field.parse(second_pass=True)
            elif field.has_second_pass:
                field.do_second_pass()


    def format(self, indent=0, name_suffix='', full_name=False, max_fields=0x10):
        """
        Format the structure for printing.

        :param full_name: Print full field names.
        """
        res = []
        name = self.full_name if full_name else self.name
        name = '%-*s' % (40 - indent * 2, name + name_suffix)
        row = f'{indent*"  "}- {name} @0x{self.offset:06X} [{self.size:5}]:\n'
        res.append(row)
        for f in self.fields:
            if type(f) is list:
                print_last = False
                for i, e in enumerate(f):
                    res.append(e.format(indent=indent + 1, name_suffix=f'[{i}]', full_name=full_name))
                    if max_fields and i == max_fields - 1:
                        left = len(f) - i - 2   # last will be printed separately
                        if left >= 1:
                            res.append(f'{(indent+1)*"  "}[...] ({left} more fields)\n')
                        print_last = True
                        break
                if print_last:
                    res.append(f[-1].format(indent=indent + 1, name_suffix=f'[{len(f) - 1}]', full_name=full_name))
            elif vs2.logging.CFG['debug_level'] or not f.flags & FLG_HIDDEN:
                res.append(f.format(indent=indent + 1, full_name=full_name))
        return ''.join(res)



class Field(VSBase):
    """
    Structure field.

    :param parent: A VStruct instance.
    :param lazy: Lazy evaluation (default: True).
    """
    IS_BASIC = False
    IS_NUMERIC = False
    REGEX = None


    def _parse(self):
        """
        Parse this VStruct. Must set ._value and ._size.

        :return: The size of the field.
        """
        if self.parsing:
            raise RuntimeError('.parse() called itself recursively - probably a property access inside .parse()!')
        self.parsing = True
        res = self.parse_struct()
        self.parsing = False
        return res


    def formatted_value(self):
        """
        Formats the value for printing.
        """
        formatter = getattr(self, 'formatter', None)
        if type(self.value) in (bytes, bytearray):
            value = self.value.hex()
            value = ' '.join([value[i:i + 2] for i in range(0, len(value), 2)])
            max_chars = vs2.logging.CFG['max_hex_chars']
            max_hex_chars = max_chars * 3 - 1
            if len(value) > max_hex_chars:     # max size must be 3n-1
                value = value[:max_hex_chars] + '[...]'
            if len([e for e in self.value[:max_chars] if 0x20 <= e < 0x7F]) >= min(0.5 * self.size, 5):
                # also render as ASCII
                value += ' ("' + ''.join(chr(e) if 0x20 <= e < 0x7F else '.' for e in self.value[:max_chars]) + '")'
            return value
        if hasattr(self, 'bit_map') and self._parsed:
            value = self.value
            res = []
            for k, v in sorted(self.bit_map.items()):
                if value & k:
                    k = value & k
                    first_bit_pos = int(math.log2(k & -k) + 1)
                    k = k >> (first_bit_pos - 1)
                    res.append(v if k == 1 else f'{v}:{k}')
            return f'0x{value:X} ({", ".join(res) or "no bits set"})'
        if formatter:
            if hasattr(formatter, '__call__'):
                value = formatter(self.value)
            elif isinstance(formatter, dict):
                value = f'0x{self.value:X} ({formatter.get(self.value, "?")})'
            else:
                raise ValueError(f'Invalid formatter {formatter} ({type(formatter)})!')
        else:
            value = str(self.value)
            if type(self.value) is int:
                value += f' (0x{self.value:X})'
        return value


    def format(self, indent=0, name_suffix='', full_name=False):
        """
        Format the field for printing.

        :param full_name: Print full field names.
        """
        value = self.formatted_value()
        name = self.full_name if full_name else self.name
        name = '%-*s' % (40 - indent * 2, name + name_suffix)
        row = f'{indent*"  "}- {name} @0x{self.offset:06X} [{self.size:5}] = {value}\n'
        return row


def const_or_DynExpr(data):
    """
    Evaluate the data to a constant (if possible) or convert to DynExpr.
    """
    try:
        value = ast.literal_eval(data)
    except (SyntaxError, ValueError) as e:
        value = DynExpr(data)
    return value
