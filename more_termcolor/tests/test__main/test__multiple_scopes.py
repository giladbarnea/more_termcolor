from more_termcolor import colors
from more_termcolor.tests.common import print_and_compare
import pytest
import pickle


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
    with open('./multiple_scopes__mm_apt__dark_bold.pickle', 'rb') as f:
        actual = pickle.load(f)
    expected = '\x1b[1mhello \x1b[31mthere\x1b[39m \x1b[3meveryone\x1b[23m \x1b[46mhi\x1b[49;22m'
    return actual, expected
