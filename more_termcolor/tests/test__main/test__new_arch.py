import re

from more_termcolor.main import ColorScope
from more_termcolor.tests.common import print_and_compare


@print_and_compare
def test__ColorScope__bold_red():
    scope = ColorScope('bold', 'red')
    open_boundary = scope.open()
    yield open_boundary, re.compile(r'\x1b\[(1;31|31;1)m')
    reset_boundary = scope.reset()
    yield reset_boundary, re.compile(r'\x1b\[(22;39|39;22)m')


@print_and_compare
def test__ColorScope__bold_dark():
    scope = ColorScope('bold', 'dark')
    open_boundary = scope.open()
    yield open_boundary, re.compile(r'\x1b\[(1;2|2;1)m')
    reset_boundary = scope.reset()
    # merge codes if same
    yield reset_boundary, '\x1b[22m'


@print_and_compare
def test__ColorScope__bold_bold():
    scope = ColorScope('bold', 'bold')
    open_boundary = scope.open()
    yield open_boundary, '\x1b[1m'
    reset_boundary = scope.reset()
    yield reset_boundary,  '\x1b[22m'
