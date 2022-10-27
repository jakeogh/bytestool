#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement
from __future__ import annotations

import mmap
import os
from collections.abc import Iterator
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from asserttool import ic
from asserttool import validate_slice
from bitstring import \
    ConstBitStream  # https://github.com/scott-griffiths/bitstring
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from mptool import output
from unmp import unmp

# from bitstring import BitArray
# from bitstring import BitStream

signal(SIGPIPE, SIG_DFL)


def read_by_byte(
    file_object,
    byte: bytes,
    verbose: bool | int | float,
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
    verbose: bool | int | float,
) -> tuple[int]:

    if verbose:
        ic(path, bytes_match, byte_alinged)
    const_bitstream = ConstBitStream(filename=path)
    found = const_bitstream.find(bytes_match, bytealigned=byte_alinged)
    return found


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose: bool | int | float,
    verbose_inf: bool,
    dict_output: bool,
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
    verbose: bool | int | float,
    verbose_inf: bool,
    dict_output: bool,
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


class MaskedMMapOpen:
    def __init__(self, path: Path, slices: list[str], verbose: bool | int | float):
        self.path = path
        self.slices = slices
        self.verbose = verbose

    def __enter__(self):
        self.fh = open(self.path, "r+b")
        self.mmfh = mmap.mmap(self.fh.fileno(), 0, flags=mmap.MAP_PRIVATE)
        for _slice in self.slices:
            slice_object_to_eval = f"self.mmfh{_slice}"
            ic(slice_object_to_eval)
            slice_object = eval(slice_object_to_eval)
            ic(slice_object)
            slice_object_length = len(slice_object)
            ic(slice_object_length)

            zero_bytes = f"bytes({slice_object_length})"
            ic(zero_bytes)
            to_exec = f"{slice_object_to_eval} = {zero_bytes}"
            to_exec = to_exec.encode("utf8")
            ic(to_exec)
            exec(to_exec)
            ic(eval(slice_object_to_eval))

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
    verbose: bool | int | float,
    verbose_inf: bool,
    dict_output: bool,
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
    index = 0
    for index, path in enumerate(iterator):
        if verbose:
            ic(index, path)
        _path = Path(os.fsdecode(path))

        with MaskedMMapOpen(path=_path, slices=slices, verbose=verbose) as fh:
            data = fh.read()
            ic(data)
            ic(data.hex())
            output(data, reason=path, tty=tty, verbose=verbose, dict_output=dict_output)
