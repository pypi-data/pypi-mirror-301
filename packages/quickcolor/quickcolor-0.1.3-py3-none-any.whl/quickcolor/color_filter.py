#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Methods to filter ANSI escape sequences from input strings
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

import re

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def strip_ansi_esc_sequences_from_string(stringWithAnsiCodes):
    '''
    Remove ANSI escape sequences from input string
    Intended use is to remove color codes, however other escape sequenc
       are also filtered out
    Greedy match to any numeral - assumes well formatted input
    '''
    return re.sub(r'\033\[(\d|;)+?m', '', stringWithAnsiCodes)

# ------------------------------------------------------------------------------------------------------

def strip_ansi_esc_sequences_from_input(stringOrBytes):
    '''
    Remove ANSI escape sequences from input data as either string or bytes.
    Any byte encoded data will be decoded using UTF-8.
    Intended use is to remove color codes, however other escape sequenc
       are also filtered out
    Greedy match to any numeral - assumes well formatted input
    '''
    if isinstance(stringOrBytes, bytes):
        return re.sub(r"\x1b[^m]*m", "", stringOrBytes.decode("utf-8"))

    return re.sub(r"\x1b[^m]*m", "", stringOrBytes)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

