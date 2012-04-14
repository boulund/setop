#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2012 Tigr <tigr42@centrum.cz>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
setop - line-wise set operations on files

Make line-wise union, intersection, difference, or Cartesian product of files
and print it to stdout.

Author: Tigr
URL:    https://github.com/tigr42/setop

"""

import sys
import argparse
import functools
import itertools

__VERSION__ = (0, 1)


def line_set(file):
    """Read lines from a file object into a set."""
    if file.name == "<stdin>": file = file.buffer  # binary mode

    strip_trailing_newline = lambda s: s.rstrip(b"\r\n")
    line_set = set(map(strip_trailing_newline, file.readlines()))
    line_set.discard(b"")
    return line_set


def reduce_line_sets(files, function):
    """Reduce sets of lines using given function."""
    if len(files) >= 1:
        x, *xs = map(line_set, files)
        return functools.reduce(function, xs, x)
    else:
        return set()


class SetOp:
    def __init__(self):
        newline_mode = "windows" if sys.platform == "win32" else "unix"
                
        self.parser = parser = argparse.ArgumentParser(description=__doc__,
                                                       formatter_class=argparse.RawTextHelpFormatter)
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("-u", "--union",
                          dest="mode", action="store_const", const="union",
                          help="lines(file1) UNION lines(file2) ...")
        mode.add_argument("-i", "--intersection",
                          dest="mode", action="store_const", const="intersection",
                          help="lines(file1) INTERSECTION lines(file2) ...")
        mode.add_argument("-d", "--difference",
                          dest="mode", action="store_const", const="difference",
                          help="lines(file1) - lines(file2) - lines(file3) ...")
        mode.add_argument("-p", "--product",
                          dest="mode", action="store_const", const="product",
                          help="lines(file1) x lines(file2) x lines(file3) ...")
        parser.add_argument("-D", "--delimiter",
                            nargs="?", default="\t",
                            metavar="delimiter",
                            help="field delimiter in product mode (default: TAB)")
        parser.add_argument("-n", "--newlines",
                            choices=["unix", "windows"],
                            default=newline_mode,
                            help="line separator, unix = LF and windows = CR+LF "
                                 "(default value according to detected OS: %s)" % newline_mode)
        parser.add_argument("files",
                            nargs="*", type=argparse.FileType("rb"),
                            metavar="file",
                            help="input files (use \"-\" for stdin)")
        parser.add_argument("-v", "--version",
                            action="version", version="setop v%d.%d" % __VERSION__)
    
    def run(self, args):
        arguments = self.parser.parse_args(args)
        files = arguments.files
        mode = arguments.mode
        delimiter = arguments.delimiter.encode("ascii")
        EOL = dict(unix=b"\n", windows=b"\r\n")[arguments.newlines]

        if mode == "union":
            output_lines = sorted(reduce_line_sets(files, set.union))
        elif mode == "intersection":
            output_lines = sorted(reduce_line_sets(files, set.intersection))
        elif mode == "difference":
            output_lines = sorted(reduce_line_sets(files, set.difference))
        elif mode == "product":
            sorted_line_lists = map(lambda f: sorted(line_set(f)), files)
            output_lines = (delimiter.join(t)
                            for t in itertools.product(*sorted_line_lists))
        
        for line in output_lines:
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.write(EOL)


if __name__ == "__main__":
    application = SetOp()
    application.run(sys.argv[1:])
