#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]

import os
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
#from typing import ByteString
#from typing import Optional
from typing import Iterator
from typing import Union

import click
from asserttool import ic
from asserttool import increment_debug
from asserttool import tv
from bitstring import ConstBitStream
from clicktool import click_add_options
from clicktool import click_global_options
from unmp import unmp

#this should be earlier in the imports, but isort stops working
signal(SIGPIPE, SIG_DFL)


@increment_debug
def read_by_byte(file_object,
                 byte,
                 verbose: Union[bool, int],
                 buffer_size: int = 1024,
                 ) -> Iterator[bytes]:    # orig by ikanobori
    if verbose:
        ic(byte)
    buf = b""
    for chunk in iter(lambda: file_object.read(buffer_size), b""):
        if verbose > 2:
            ic(chunk)
        buf += chunk
        sep = buf.find(byte)
        if verbose > 2:
            ic(buf, sep)

        ret = None
        while sep != -1:
            ret, buf = buf[:sep], buf[sep + 1:]
            yield ret
            sep = buf.find(byte)

    if verbose > 2:
        ic('fell off end:', ret, buf)
    if buf:
        yield buf


@click.group()
@click_add_options(click_global_options)
@click.pass_context
def cli(ctx,
        verbose: int,
        verbose_inf: bool,
        ):

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )


@cli.command()
@click.argument("matches", type=str, nargs=-1, required=True,)
@click_add_options(click_global_options)
@click.pass_context
def byte_offset_of_match(ctx,
                         matches: tuple[str],
                         verbose: int,
                         verbose_inf: bool,
                         ):

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )

    iterator = unmp(valid_types=[bytes,], verbose=verbose)

    index = 0
    for index, path in enumerate(iterator):
        if verbose:
            ic(index, path)
            _path = Path(os.fsdecode(path))
        const_bitstream = ConstBitStream(filename=path)
        for _match_str in matches:
            _match_bytes = _match_str.encode('utf8')
            found = const_bitstream.find(_match_bytes, bytealigned=True)
            ic(found)
