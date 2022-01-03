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

# code style:
#   no guessing on spelling: never tmp_X always temporary_X
#   dont_makedirs -> no_makedirs
#   no guessing on case: local vars, functions and methods are lower case. classes are ThisClass(). Globals are THIS.
#   del vars explicitely ASAP, assumptions are buggy
#   rely on the compiler, code verbosity and explicitness can only be overruled by benchamrks (are really compiler bugs)
#   no tabs. code must display the same independent of viewer
#   no recursion, recursion is undecidiable, randomly bounded, and hard to reason about
#   each elementis the same, no special cases for the first or last elemetnt:
#       [1, 2, 3,] not [1, 2, 3]
#       def this(*.
#                a: bool,
#                b: bool,
#               ):
#
#   expicit loop control is better than while (condition):
#       while True:
#           # continue/break explicit logic


# TODO:
#   https://github.com/kvesteri/validators
import os
import sys
import click
import time
import sh
from clicktool import clock_add_options, click_global_options
from signal import signal, SIGPIPE, SIG_DFL
from pathlib import Path
#from with_sshfs import sshfs
#from with_chdir import chdir
from asserttool import tv
from asserttool import validate_slice
from asserttool import eprint, ic
from asserttool import verify
from retry_on_exception import retry_on_exception
from enumerate_input import enumerate_input
#from collections import defaultdict
#from prettyprinter import cpprint
#from prettyprinter import install_extras
#install_extras(['attrs'])
#from timetool import get_timestamp
#from configtool import click_read_config
#from configtool import click_write_config_entry

#from asserttool import not_root
#from pathtool import path_is_block_special
#from pathtool import write_line_to_file
#from getdents import files
#from prettytable import PrettyTable
#output_table = PrettyTable()

from typing import List
from typing import Tuple
from typing import Sequence
from typing import Generator
from typing import Iterable
from typing import ByteString
from typing import Optional
from typing import Union

# click-command-tree
#from click_plugins import with_plugins
#from pkg_resources import iter_entry_points

# import pdb; pdb.set_trace()
# #set_trace(term_size=(80, 24))
# from pudb import set_trace; set_trace(paused=False)

##def log_uncaught_exceptions(ex_cls, ex, tb):
##   eprint(''.join(traceback.format_tb(tb)))
##   eprint('{0}: {1}'.format(ex_cls, ex))
##
##sys.excepthook = log_uncaught_exceptions

#this should be earlier in the imports, but isort stops working
signal(SIGPIPE, SIG_DFL)

#@with_plugins(iter_entry_points('click_command_tree'))
#@click.group()
#@click_add_options(click_global_options)
#@click.pass_context
#def cli(ctx,
#        verbose: int,
#        verbose_inf: bool,
#        ):
#
#    tty, verbose = tv(ctx=ctx,
#                      verbose=verbose,
#                      verbose_inf=verbose_inf,
#                      )


# update setup.py if changing function name
#@click.argument("slice_syntax", type=validate_slice, nargs=1)
@click.command()
@click.argument("paths", type=str, nargs=-1)
@click.argument("sysskel",
                type=click.Path(exists=False,
                                dir_okay=True,
                                file_okay=False,
                                allow_dash=False,
                                path_type=Path,),
                nargs=1,
                required=True,)
@click.option('--ipython', is_flag=True)
#@click_add_options(click_global_options)
@click.pass_context
def cli(ctx,
        paths: Optional[tuple[str]],
        sysskel: Path,
        ipython: bool,
        verbose: int,
        verbose_inf: bool,
        ):

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )

    if paths:
        iterator = paths
        del paths
    else:
        iterator = unmp(allow_types=[bytes,], verbose=verbose)

    index = 0
    #for index, path in enumerate_input(iterator=iterator,
    #                                   dont_decode=True,  # paths are bytes
    #                                   progress=False,
    #                                   verbose=verbose,
    #                                   ):
    for index, path in enumerate(iterator):
        path = Path(os.fsdecode(path))

        if verbose:  # or simulate:
            ic(index, path)
        #if count:
        #    if count > (index + 1):
        #        ic(count)
        #        sys.exit(0)

        #if simulate:
        #    continue

        with open(path, 'rb') as fh:
            path_bytes_data = fh.read()

        if not count:
            output(path, tty=tty, verbose=verbose)

    if count:
        output(index + 1, tty=tty, verbose=verbose)

#        if ipython:
#            import IPython; IPython.embed()



#!/usr/bin/env python3

# pylint: disable=C0111  # docstrings are always outdated and wrong
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

import os
import secrets
import sys
import time
from collections import deque
from math import inf
from stat import S_ISFIFO
from typing import Iterator
from typing import Optional
from typing import Union

from asserttool import eprint
from asserttool import ic
from asserttool import increment_debug


@increment_debug
def read_by_byte(file_object,
                 byte,
                 verbose: Union[bool, int],
                 buffer_size: int = 1024,
                 ) -> Iterator[bytes]:    # orig by ikanobori
    if verbose:
        ic(byte)
    buf = b""
    #for chunk in iter(lambda: file_object.read(131072), b""):
    #for chunk in iter(lambda: file_object.read(8192), b""):
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


@increment_debug
def filtergen(*,
              iterator,
              filter_function: object,
              verbose: bool,
              ):
    if verbose:
        ic(filter_function)
    if verbose == inf:
        ic(iterator)
    for item in iterator:
        if verbose == inf:
            ic(item)
        if not filter_function(item):
            continue
        yield item


@increment_debug
def skipgen(*,
            iterator,
            count,
            verbose: bool,
            ):
    if verbose:
        ic(count)
    if verbose == inf:
        ic(iterator)
    for index, item in enumerate(iterator):
        if verbose == inf:
            ic(index, item)
        if (index + 1) <= count:
            continue
        yield item


@increment_debug
def headgen(*,
            iterator,
            count,
            verbose: bool,
            ):
    if verbose:
        ic(count)
    if verbose == inf:
        ic(iterator)
    for index, item in enumerate(iterator):
        if verbose == inf:
            ic(index, item)
        yield item
        if verbose == inf:
            ic(index + 1, count)
        if (index + 1) == count:
            return


@increment_debug
def append_to_set(*,
                  iterator,
                  the_set: set,
                  max_wait_time: float,
                  min_pool_size: int,  # the_set always has 1 item
                  verbose: bool,
                  ):

    assert max_wait_time > 0.01
    assert min_pool_size >= 2

    time_loops = 0
    eprint("\nWaiting for min_pool_size: {}\n".format(min_pool_size))
    while len(the_set) < min_pool_size:
        start_time = time.time()
        while (time.time() - start_time) < max_wait_time:
            time_loops += 1
            try:
                the_set.add(next(iterator))
            except StopIteration:
                pass

        if time_loops > 1:
            msg = "\nWarning: min_pool_size: {} was not reached in max_wait_time: {}s so actual wait time was: {}x {}s\n"
            msg = msg.format(min_pool_size,
                             max_wait_time,
                             time_loops,
                             max_wait_time * time_loops,)
            eprint(msg)

        if len(the_set) < min_pool_size:
            eprint("\nlen(the_set) is {} waiting for min_pool_size: {}\n".format(len(the_set), min_pool_size))

    assert time_loops > 0
    return the_set


# add time-like memory limit
# the longer the max_wait, the larger buffer_set will be,
# resulting in better mixing
@increment_debug
def randomize_iterator(iterator,
                       *,
                       min_pool_size: int,
                       max_wait_time: float,
                       buffer_set=None,
                       verbose: bool = False,
                       ):

    assert max_wait_time
    assert min_pool_size

    if min_pool_size < 2:
        min_pool_size = 2

    if not buffer_set:
        buffer_set = set()
        try:
            buffer_set.add(next(iterator))
        except StopIteration:
            pass

    buffer_set = append_to_set(iterator=iterator,
                               the_set=buffer_set,
                               min_pool_size=min_pool_size,
                               max_wait_time=max_wait_time,
                               verbose=verbose,
                               )

    while buffer_set:
        try:
            buffer_set.add(next(iterator))
            buffer_set.add(next(iterator))
        except StopIteration:
            pass

        buffer_set_length = len(buffer_set)
        random_index = secrets.randbelow(buffer_set_length)
        next_item = list(buffer_set).pop(random_index)
        buffer_set.remove(next_item)
        if verbose == inf:
            eprint("Chose 1 item out of", buffer_set_length)
        if verbose == inf:
            eprint("len(buffer_set):", buffer_set_length - 1)
        if verbose:
            ic(len(buffer_set), random_index, next_item)

        yield next_item


@increment_debug
def iterate_input(iterator,
                  null: bool,
                  disable_stdin: bool,
                  dont_decode: bool,
                  head: Optional[int],
                  tail: Optional[int],
                  skip: Optional[int],
                  random: bool,
                  loop: bool,
                  verbose: bool,
                  input_filter_function: object,
                  buffer_size: int = 128,
                  ):

    byte = b'\n'
    if null:
        byte = b'\x00'

    if skip:
        if isinstance(skip, bool) or (skip <= 0):
            #ic('BUG', skip)
            skip = None
            #raise ValueError('skip must be False or a positive integer, not:', skip)
    if head:
        if isinstance(head, bool) or (head <= 0):
            #ic('BUG', head)
            head = None
            #raise ValueError('head must be False or a positive integer, not:', head)
    if tail:
        if isinstance(tail, bool) or (tail <= 0):
            #ic('BUG', tail)
            tail = None
            #raise ValueError('tail must be False or a positive integer, not:', tail)

    if not iterator:
        if disable_stdin:
            raise ValueError('iterator is None and disable_stdin=True, nothing to read')

    stdin_is_a_tty = sys.stdin.isatty()
    if disable_stdin:
        stdin_is_a_fifo = False
    else:
        stdin_is_a_fifo = S_ISFIFO(os.fstat(sys.stdin.fileno()).st_mode)
        #stdin_given = select.select([sys.stdin,], [], [], 0.0)[0]

    if verbose:
        ic(byte, skip, head, tail, null, disable_stdin, random, dont_decode, stdin_is_a_tty, stdin_is_a_fifo)

    if stdin_is_a_fifo:
        iterator = sys.stdin.buffer
        if verbose:
            ic('waiting for input on sys.stdin.buffer', byte)

    if hasattr(iterator, 'read'):
        iterator = read_by_byte(iterator,
                                byte=byte,
                                verbose=verbose,
                                buffer_size=buffer_size,
                                )

    if input_filter_function:
        if verbose:
            ic(random)
        iterator = filtergen(iterator=iterator,
                             filter_function=input_filter_function,
                             verbose=verbose,
                             )
        if verbose == inf:
            ic(iterator)

    if random:
        if verbose:
            ic(random)
        iterator = randomize_iterator(iterator,
                                      min_pool_size=1,
                                      max_wait_time=1,
                                      verbose=verbose,)
        if verbose == inf:
            ic(iterator)

    if skip:
        if verbose:
            ic(skip)
        iterator = skipgen(iterator=iterator,
                           count=skip,
                           verbose=verbose,
                           )
        if verbose == inf:
            ic(iterator)

    if head:
        if verbose:
            ic(head)
        iterator = headgen(iterator=iterator,
                           count=head,
                           verbose=verbose,
                           )
        if verbose == inf:
            ic(iterator)

    if tail:  # this seems like the right order, can access any "tail"
        if verbose:
            ic(tail)
        iterator = deque(iterator,
                         maxlen=tail,)
        if verbose == inf:
            ic(iterator)

    lines_output = 0
    for index, string in enumerate(iterator):
        if verbose == inf:
            ic(index, string)

        if not dont_decode:
            if isinstance(string, bytes):
                try:
                    string = string.decode('utf8')
                except UnicodeDecodeError as e:
                    if verbose:
                        ic(e)
                    ic(string)
                    raise e


        if verbose == inf:
            try:
                ic(len(string))
            except (TypeError, AttributeError):
                pass    # need to be able to iterate over arb objects

        yield string
        lines_output += 1


@increment_debug
def enumerate_input(*,
                    iterator,
                    buffer_size: Optional[int] = 1024,
                    verbose: bool,
                    newline_record_sep: bool = False,
                    loop: bool = False,
                    disable_stdin: bool = False,
                    random: bool = False,
                    dont_decode: bool = False,
                    progress: bool = False,
                    skip: Optional[int] = None,
                    head: Optional[int] = None,
                    tail: Optional[int] = None,
                    input_filter_function: Optional[object] = None,
                    ):

    null = not newline_record_sep
    if progress and verbose:
        raise ValueError('--progress and --verbose are mutually exclusive')
    if verbose:
        ic(skip, head, tail, null, loop, disable_stdin, random, dont_decode, progress)

    inner_iterator = iterate_input(iterator=iterator,
                                   null=null,
                                   disable_stdin=disable_stdin,
                                   buffer_size=buffer_size,
                                   head=head,
                                   tail=tail,
                                   skip=skip,
                                   dont_decode=dont_decode,
                                   loop=loop,
                                   random=random,
                                   verbose=verbose,
                                   input_filter_function=input_filter_function,)
    start_time = time.time()
    if verbose == inf:
        ic(inner_iterator)

    for index, thing in enumerate(inner_iterator):
        # would strip empty lines...
        #try:
        #    if len(thing) == 0:
        #        continue
        #except TypeError as e:  # iterating over objects
        #    if verbose:
        #        ic(e)

        if progress:
            if index % 100 == 0:
                items_total = index + 1
                time_running = time.time() - start_time
                items_per_second = int(items_total / time_running)
                #print(index + 1, file=sys.stderr, end='\r')
                print(items_total, items_per_second, file=sys.stderr, end='\r')
        yield index, thing
    if progress:
        print("", file=sys.stderr)
