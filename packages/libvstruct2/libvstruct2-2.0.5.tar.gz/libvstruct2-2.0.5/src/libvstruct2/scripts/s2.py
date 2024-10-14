#!/usr/bin/env python3
"""
vstruct2 file parsing tool.

Author: Vlad Topan (vtopan/gmail).
"""
import argparse
import ast
import glob
import mmap
import os
import sys

from libvstruct2 import vstruct


TARGETLESS_OPS = ['regenerate']


def parse(fh, args):
    """
    Parse a file and print the information.
    """
    ft = args.struct or vs2.get_file_type(fh)
    parser = vs2.FT_MAP.get(ft, (None, None))[1]
    if not parser:
        vs2.err(f'Can\'t parse file type: {ft}!')
        return None, None
    dataview = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
    vs = parser(name=os.path.basename(fh.name), dataview=dataview)
    return (dataview, vs)


def regenerate(args):
    """
    Regenerate vstructs based on defs.
    """
    ldr = vs2.DefLoader()
    ldr.load()
    ldr.save()


def msg(s):
    """
    Output message to console (over stderr).
    """
    sys.stderr.write(s + '\n')


def main():
    global vs2, OUT

    parser = argparse.ArgumentParser(description='vstruct2 file parsing tool.')
    parser.add_argument('targets', help='target(s): file name(s) or - for stdin', nargs='*')
    parser.add_argument('-v', '--verbose', help='verbose (can use multiple times)', action='count', default=0)
    parser.add_argument('-D', '--debug', help='debug', action='count', default=0)
    # ops
    parser.add_argument('-p', '--parse', help='print info (default if no offset given)', action='store_true')
    parser.add_argument('-s', '--struct', help='parse with this VStruct')
    parser.add_argument('-q', '--query-field', help='print this field (dot-separated)', action='append', default=[])
    parser.add_argument('-b', '--binary', help='dump raw binary value (for use with -q and -o)', action='store_true')
    parser.add_argument('-r', '--regenerate', help='regenerate vstructs based on '
            'definitions (update as needed)', action='store_true')
    # output control
    parser.add_argument('-o', '--output', help='output filename (for -b only)')
    parser.add_argument('-mh', '--max-hex-chars', help='max. hex chars to display', default=10, type=int)
    parser.add_argument('-F', '--full-field-names', help='print full field names', action='store_true')
    parser.add_argument('-@', '--offset', help='start at offset', type=ast.literal_eval, default=None)
    args = parser.parse_args()

    if args.regenerate:
        # broken vstructs might prevent import
        old_init = os.path.dirname(__file__) + '/../vstructs/__init__.py'
        if os.path.isfile(old_init):
            os.remove(old_init)

    import libvstruct2 as vs2

    vs2.logging.CFG['max_hex_chars'] = args.max_hex_chars

    if not (args.parse or args.regenerate):
        args.parse = True
    vs2.logging.CFG['debug_level'] = args.debug
    vs2.dbg('Args: %s' % args, 1)

    if args.regenerate:
        regenerate(args)

    if args.binary:
        if not args.output:
            args.output = 'vstruct.bin'
            msg(f'[#] Writing output data to {args.output}...')
        open(args.output, 'wb').close()
    if args.targets:
        ldr = vs2.DefLoader()
        ldr.load()
        if args.query_field:
            args.query_field = [e.split('.') for e in args.query_field]
        for fn_pat in args.targets:
            for fn in glob.glob(fn_pat):
                if args.parse or args.query_field:
                    vs2.log(f'Opening {fn}...')
                    fh = open(fn, 'rb')
                    try:
                        dv, vs = parse(fh, args)
                        if not vs:
                            continue
                        if args.query_field:
                            for qf in args.query_field:
                                v = vs
                                for e in qf:
                                    v = v[e]
                                if args.binary:
                                    with open(args.output, 'wb') as fh:
                                        fh.write(dv[v.offset:v.offset + v.size])
                                else:
                                    print(v.format(full_name=args.full_field_names).rstrip())
                        else:
                            print(vs.format(full_name=args.full_field_names).rstrip())
                    except vs2.ParseError as e:
                        vs2.err('Parse error: ' + str(e))
                        continue
                    except KeyError as e:
                        vs2.err('Field missing: ' + str(e))
                    dv.close()
                    fh.close()


if __name__ == '__main__':
    main()
