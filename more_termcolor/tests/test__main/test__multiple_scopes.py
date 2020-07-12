import pickle
from pathlib import Path

import pytest

from more_termcolor import colors
from more_termcolor.tests.common import print_and_compare


def h1(text, **kwargs):
    return colors.bold(text, 'ul', 'reverse', 'bright white', **kwargs)


def h2(text, **kwargs):
    return colors.bold(text, 'ul', 'bright white', **kwargs)


def h3(text, **kwargs):
    return colors.bold(text, 'bright white', **kwargs)


def c(text, **kwargs):
    return colors.dark(text, **kwargs)


def i(text, **kwargs):
    return colors.italic(text, **kwargs)


def b(text, **kwargs):
    return colors.bold(text, **kwargs)


@print_and_compare
def test__real_world__git():
    strategy = colors.italic("strategy")
    actual = colors.dark(f'{strategy} --strategy={strategy}')
    expected = '\x1b[2;3mstrategy\x1b[23m --strategy=\x1b[3mstrategy\x1b[23m\x1b[22;23m'
    return actual, expected


@pytest.mark.skip("unskip when merge tests pass")
@print_and_compare
def test__real_world__guy():
    actual = colors.bold(f'hello {colors.red("there")} {colors.italic("everyone")} {colors.on_cyan("hi")}')
    expected = '\x1b[1mhello \x1b[31mthere\x1b[39m \x1b[3meveryone\x1b[23m \x1b[46mhi\x1b[49;22m'
    return actual, expected


@print_and_compare
def test__real_world__mm_apt():
    apt_file = b("apt-file")
    actual = f"""{c(f'{apt_file} searches pkgs containing specific file')}"""
    expected = '\x1b[2;1mapt-file\x1b[22;2m searches pkgs containing specific file\x1b[22m'
    
    return actual, expected
