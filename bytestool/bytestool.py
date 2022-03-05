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

import mmap
import os
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Iterator
from typing import Union

import click
from asserttool import ic
from asserttool import increment_debug
from asserttool import validate_slice
from bitstring import BitArray
from bitstring import BitStream
from bitstring import \
    ConstBitStream  # https://github.com/scott-griffiths/bitstring
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from epprint import epprint
from mptool import output
from mptool import unmp

signal(SIGPIPE, SIG_DFL)


@increment_debug
def read_by_byte(
    file_object,
    byte: bytes,
    verbose: Union[bool, int, float],
    buffer_size: int = 1024,
) -> Iterator[bytes]:  # orig by ikanobori
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
            ret, buf = buf[:sep], buf[sep + 1 :]
            yield ret
            sep = buf.find(byte)

    if verbose > 2:
        ic("fell off end:", ret, buf)
    if buf:
        yield buf


def find_byte_match_in_path(
    *,
    bytes_match: bytes,
    path: Path,
    byte_alinged: bool,
    verbose: Union[bool, int, float],
) -> tuple[int]:

    if verbose:
        ic(path, bytes_match, byte_alinged)
    const_bitstream = ConstBitStream(filename=path)
    found = const_bitstream.find(bytes_match, bytealigned=byte_alinged)
    return found


@click.group(no_args_is_help=True)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
):

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )


@cli.command()
@click.argument(
    "matches",
    type=str,
    nargs=-1,
    required=True,
)
@click.option(
    "--not-byte-alinged",
    is_flag=True,
)
@click.option(
    "--hex",
    "hexencoding",
    is_flag=True,
)
@click_add_options(click_global_options)
@click.pass_context
def byte_offset_of_match(
    ctx,
    matches: tuple[str],
    not_byte_alinged: bool,
    hexencoding: bool,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
):

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    byte_alinged = not not_byte_alinged
    iterator = unmp(
        valid_types=[
            bytes,
        ],
        verbose=verbose,
    )

    index = 0
    for index, path in enumerate(iterator):
        if verbose:
            ic(index, path)
        _path = Path(os.fsdecode(path))
        const_bitstream = ConstBitStream(filename=_path)
        for _match_str in matches:
            if hexencoding:
                _match_bytes = bytes.fromhex(_match_str)
            else:
                _match_bytes = _match_str.encode("utf8")
            # found = find_byte_match_in_path(bytes_match=_match_bytes, bitstream=const_bitstream, verbose=verbose)
            found = const_bitstream.find(_match_bytes, bytealigned=byte_alinged)
            ic(found)


class mask_byte_slices:
    def __init__(self, path: Path, slices: list[str], verbose: Union[bool, int, float]):
        self.path = path
        self.slices = slices
        self.verbose = verbose

    def __enter__(self):
        self.fh = open(self.path, "r+b")
        self.mmfh = mmap.mmap(self.fh.fileno(), 0, flags=mmap.MAP_PRIVATE)
        for _slice in self.slices:
            # ic(len(bitstream), bitstream)
            assert _slice.startswith("[")
            assert _slice.endswith("]")
            # to_eval = f"mmfh{_slice}"
            # to_eval = f"epprint({to_eval})"
            # ic(to_eval)
            # eval(to_eval)

            ##to_exec = f"self.mmfh{_slice} = 0"
            # to_exec = f"self.mmfh{_slice} = '0'.encode('utf8') * ()"
            # ic(to_exec)
            # exec(to_exec)

            slice_object_to_eval = f"self.mmfh{_slice}"
            ic(slice_object_to_eval)
            slice_object = eval(slice_object_to_eval)
            ic(slice_object)
            slice_object_length = len(slice_object)
            ic(slice_object_length)

            zero_bytes = b"0" * slice_object_length
            ic(zero_bytes)
            to_exec = f"{slice_object_to_eval} = zero_bytes"
            ic(to_exec)
            exec(to_exec)
            ic(eval(slice_object_to_eval))

            ## IPython.embed()
            ### to_eval = f"mmfh{_slice} = " + """b'\\00'"""
            ## to_eval = f"mmfh{_slice} = 0x00"
            ## ic(to_eval)
            ## eval(to_eval)

            # to_eval = f"mmfh{_slice}"
            # to_eval = f"epprint({to_eval})"
            # ic(to_eval)
            # eval(to_eval)
        return self.mmfh

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mmfh.close()
        self.fh.close()


@cli.command()
@click.argument("slices", type=validate_slice, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def delete_byte_ranges(
    ctx,
    slices: tuple[str],
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
):

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    iterator = unmp(
        valid_types=[
            bytes,
        ],
        verbose=verbose,
    )

    # iterator = [
    #    b"2EbanrRUuy0.webm.header1",
    # ]
    index = 0
    for index, path in enumerate(iterator):
        if verbose:
            ic(index, path)
        _path = Path(os.fsdecode(path))

        with mask_byte_slices(path=_path, slices=slices, verbose=verbose) as fh:
            data = fh.read()
            ic(data)
            ic(data.hex())
            output(data, reason=path, tty=tty, verbose=verbose, dict_input=dict_input)
