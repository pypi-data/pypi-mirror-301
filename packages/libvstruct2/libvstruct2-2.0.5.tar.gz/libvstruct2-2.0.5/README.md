# libvstruct2

YAML-like structured binary data representation language (partially based on Python). Goals:
- brief
- expressive (capable to describe most contemporary file/data formats)
- human-readable
- fast (enough)
- easy to parse
- easy to translate into Python parsers
- *WARNING*: very alpha release, many things are still broken / can change.

Note: some automagical conversions happen when translating `.vs2` sources to `.py` sources to simplify
writing the definitions (to-be-documented). See the included file formats for examples.

Vlad Topan (vtopan/gmail), Feb. 2020


## Format

- YAML-like, mapping structures to `- field:type` lists or detailed field descriptions.

```yaml
- field:
  - type
  - key1: value1
  - key2: value2
```

- example:


```yaml
StructName:
  - field1: I4        # 4-byte integer - this is ignored
  - field2:
    - a[100]
    - desc: some 4-byte integer field
    - offset: 1234
```

- shorthands exist (see `PFX_MAP` in `libvstruct2/defparser.py` for a full mapping), the [Fields][] section below for details:
  - `    @ ...` is equivalent to `    - offset: ...`
  - `    = ...` is equivalent to `    - validator: ...` (dynamic expression, exact value or collection)
  - `    ? ...` is equivalent to `    - lookahead: ...` (preview data, don't consume buffer)


## VStruct objects

Each VStruct object (structure or field) has the obvious attributes (`.offset`, `.size`, `.value`, `.parent`, etc.) and
some less obvious attributes and methods:

- `.root`: the top-level VStruct which initiated the parsing process
- `.first_parent(type_or_typename)`: returns the first (grand)parent of the given type

## Fields

- syntax: `<indent>- <fieldname>: <fieldtype>` followed optionally by additional modifiers
    - most modifiers also have a short syntax, either as a modifier prefix or as a suffix to the `<fieldtype>`
        - prefix example: `    - dyn_offset: <offset>` is the same as `    @ <offset>`
        - suffix example: `  - field1: R[<length>]` is the same as `  - field1: R` followed by `    - length: <length>`
    - modifiers (with prefixes/suffixes in parenthesis where available):
        - prefixes:
            - `validator` (`=`): after evaluation, test the resulting value with this expression
                - can be a `list` / `tuple`, `dict`, callable or exact (immediate) value
            - `should_be` (`?=`): same as `validator`, but instead of stopping the parser, only a warning is issued
            - `dyn_offset` (`@`): dynamic offset - evaluated at runtime (see `DynExpr`)
            - `formatter` (`~`): used to format the value for display - a callable or a `dict` (if value is not in dict, `?` is returned)
            - `hidden` (`.`): don't display when displaying the structure (flag used for internal / irrelevant fields)
            - `description` (`"..."`): field description
            - `bit_map` (`{...}`): masks mapping bits to names
            - `lookahead` (`?`): parsing the field won't consume from the buffer (the current offset is not changed)
            - `out_of_struct` (`*`): the field does not follow from the current offset (this is set automatically by `dyn_offset`)
            - `required` (`!`): flag which marks a conditional field as required (raises `ParseError` if missing)
            - `post_parse` (`;`): function to be called after parsing for additional processing (receives an object instance)
            - `post_parse_value` (`:`): function to be called after parsing to further process the value (receives the object instance, must return the new value)
                - can also be a list of functions if the value is a sequence (only the values will be passed to the functions)
        - suffixes:
            - `length` (`[...]`): number of elements (field becomes an *array*, i.e. `list` of fields)
                - exception: for string and regex types, the `length` means the number of characters!
                - if the value starts with `<`, it is interpreted as `maxlen` (maximum length), e.g. for NULL-terminated strings
            - `condition` (`<...>`): `DynExpr` which, if evaluates to False, the field is considered "not present"
        - no shortcut syntax (yet):
            - `update_offset`: flag which causes an out-of-struct field to still update its parent's `.offset`
            - `endianness`: little ('<') or big ('>'), default: little
                - note: this is inherited from parent structures if not defined in fields
            - `stop`: alternative stop condition (`DynExpr`) for arrays (in this case, `length` may be simply `True`)
            - `second_pass`: (only for out_of_struct nodes) parse only on a second pass
    - virtual fields can be created with the syntax: `  - <fieldname> := <expression>` (their `.size` will be 0, but the `.offset` will be correct)
        - these are instances of the `Eval` basic type


## Expressions


### DynExpr

- most values can be defined as dynamic expressions (to reference other fields which become available during parsing)
- automagically identified by trying to parse each expression as an immediate; on failure, a DynExpr is created
- syntax:
    - `$<field>` extracts the value of `<field>` in the current (VStruct) structure (equivalent to `self.<field>.value`)
    - `@<field>` the offset of `<field>` (`self.<field>.offset`)
    - `:<field>` the size of `<field>` (`self.<field>.size`)
    - `&<attr>` extracts the value of an attribute of the current VStruct (equivalent to `self.<attr>`)
    - parent objects can be referenced using `^`, e.g.:
        - `&^^` == `self.parent.parent`
        - `$^Field1` == `self.parent.Field1.value`
- notes:
    - depending on the context, `self` is usually the current `VStruct` (e.g. when evaluating `condition`s, `length`s, etc.);
        an exception exist though - `self` is the current field when validating (`validator` expressions)


### Regex expressions

- the match is attempted from the current position
- format: `<op>/<regex>/<flags>`
    - `<op>`: what result to return
        - default (no `<op>` field): bool (`True` if matched)
        - `@`: match offset or -1
        - `:`: match length
    - `<flags>`: sequence of classic regex flags (`s` dotall, `m` multiline, `i` case insensitive) and custom flags:
        - `f`: attempt match in full file (default: 8k from current offset)


## Datatypes

- see `libvstruct2/basefields.py` for the implementation of all the basic types


### Numbers

#### Integers

- `I1` / `I2` / `I4` / `I8`: signed 1/2/4/8-byte integer (default endianness, little if none set)
- `PK1..8`: packed integer (DWARF3 LEB128) - TBD
- **signedness** *prefix*: `S` / `U` (default: unsigned)
- **endianness** *suffix*:
    - `B`: big endian
    - `L`: little endian
    - `E`: dynamic endianness (set by a conditional expression in the struct)
    - default: little endian


#### Real numbers

- `F2` / `F4`: floating-point 2/4-byte real numbers (`float` / `double`)


#### Bit masks (flags)

- `BM#` (`#` is the number of bytes, e.g. `BM2`): flags
    - accepts a `bit_map` (`{ ... }`) key which maps bits/bit groups to names


### Text & binary blobs

- `a` / `u8/16/32` / `w` / `r`: null-terminated ASCII / UTF 8/16/32 / widechar / raw (binary) string (C strings) - TBD
- `AS[len]` / `WS[len]` / `R[len]`: fixed/maximum-length ASCII / widechar / raw (binary) string (`LPSTR` / `PWSTR`)


#### RegEx-based fields

- `RX`: basic (binary) regex field (the actual regex must be passed as the condition, e.g. `  - MyField: RX <^abc>`)
    - `.value` will contain the groups tuple if more than one, a single `bytes` otherwise
    - `.raw_match` will contain the full (binary) match
- `T`: string token (ignores whitespace) - multiple values separated by a comma (e.g. `  - MyField: T <a, b, cde>`)
- `SRX`: string regex (`UTF-8` encoded)
- `IS`: integer string (textual integer); `.value` will be the actual number


### Keys

- any type can be followed by any number of "keys" (indented `- name: value` fields) with supplemental rules / information


## Feedback

Feedback is welcome via email or as issues on the gitlab project.
