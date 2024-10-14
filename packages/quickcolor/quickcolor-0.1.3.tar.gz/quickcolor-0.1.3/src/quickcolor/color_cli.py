#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for exercising color handling
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import sys
import argcomplete, argparse

from .color_def import color, colors
from .color_filter import strip_ansi_esc_sequences_from_string
from .color_filter import strip_ansi_esc_sequences_from_input
from .color_show import shell_colors, color_fields, show_term_color

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Color {color.CYELLOW2}attributes{color.CEND} for python scripts',
                    epilog='-.' * 40)

        subparsers = parser.add_subparsers(dest='cmd')

        p_shellColors = subparsers.add_parser('shell.colors', help="display a color chart for current shell")
        p_shellColors.add_argument('-e', '--extended', help="display extended chart", action="store_true")

        p_colorFields = subparsers.add_parser('color.fields', help="display class color fields")

        p_stripColorFromStr = subparsers.add_parser('strip.color.string', help="strip color codes from a string")
        p_stripColorFromInput = subparsers.add_parser('strip.color.input', help="strip color codes from a byte input")

        p_termColors = subparsers.add_parser('term.colors', help="display terminal color options")

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.cmd == 'shell.colors':
            shell_colors(extended=args.extended)

        elif args.cmd == 'color.fields':
            color_fields()

        elif args.cmd == 'term.colors':
            print()
            for colorId in range(256):
                print(show_term_color(colorId), end=' ', flush=True)
                offsetColorId = colorId -4
                if colorId == 3 or offsetColorId % 12 == 11:
                # if colorId % 13 == 12:
                    print()
            print()
            # print(' '.join([show_term_color(x) for x in range(256)]))

        elif args.cmd == 'strip.color.string':
            testString=f'{color.CYELLOW2}Color formatted {color.CBLUE2}string!{color.CEND} --> More colors: {color.CCYAN}cyan, {color.CGREEN}green, {color.CVIOLET}violet!{color.CEND}'
            hdr1 = 'Test string:'
            print(f'{hdr1:<30}{testString}')
            hdr2 = 'Stripped ANSI codes:'
            print(f'{hdr2:<30}{strip_ansi_esc_sequences_from_string(stringWithAnsiCodes = testString)}')

        elif args.cmd == 'strip.color.input':
            testString = f'{colors.fg.lightred}Red, {colors.fg.lightgrey}White, and {colors.fg.lightblue}Blue!{colors.off}'
            testBytes = testString.encode(encoding="utf-8")
            hdr1 = 'Test string:'
            print(f'{hdr1:<30}{testString}')
            hdr2 = 'Test bytes:'
            print(f'{hdr2:<30}{testBytes}')
            hdr3 = 'Stripped ANSI codes:'
            print(f'{hdr3:<30}{strip_ansi_esc_sequences_from_input(stringOrBytes = testBytes)}')

    except Exception as e:
        # 2024-0706 - note - due to circular logic, exception_details is explicitly implemented below
        area = "Color Handling"
        print(f"\n{colors.fg.lightred}{type(e).__name__}{colors.fg.lightgrey} exception occurred in {colors.fg.cyan}{area}{colors.fg.lightgrey} processing!")
        exceptionArgs = e.args
        for arg in exceptionArgs:
            print(f"{colors.fg.lightblue}--> {colors.off}{arg}")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

