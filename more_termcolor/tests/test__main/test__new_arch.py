import re

from more_termcolor.main import ColorScope
from more_termcolor.tests.common import print_and_compare, codes_perm


@print_and_compare
def test__ColorScope__bold_red():
    scope = ColorScope('bold', 'red')
    open_boundary = scope.open()
    yield open_boundary, re.compile(codes_perm(1, 31))
    reset_boundary = scope.reset()
    yield reset_boundary, re.compile(codes_perm(22, 39))


@print_and_compare
def test__ColorScope__bold_dark():
    scope = ColorScope('bold', 'dark')
    open_boundary = scope.open()
    yield open_boundary, re.compile(codes_perm(1, 2))
    reset_boundary = scope.reset()
    # merge codes if same
    yield reset_boundary, '\x1b[22m'


@print_and_compare
def test__ColorScope__bold_bold():
    scope = ColorScope('bold', 'bold')
    open_boundary = scope.open()
    yield open_boundary, '\x1b[1m'
    reset_boundary = scope.reset()
    yield reset_boundary, '\x1b[22m'
