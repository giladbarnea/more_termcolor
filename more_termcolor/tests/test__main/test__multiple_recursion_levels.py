import pytest

from more_termcolor import colored
from more_termcolor.tests.common import print_and_compare


@print_and_compare
class Test:
    @pytest.mark.skip
    def test__merge_open_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(f'{red} Bold', 'bold')
        expected = '\x1b[1;31mRed\x1b[39m Bold\x1b[0m'
        return actual, expected
    
    @pytest.mark.skip
    def test__merge_reset_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(f'Bold {red}', 'bold')
        expected = '\x1b[1Bold \x1b[31mRed\x1b[0m'
        return actual, expected
    
    @pytest.mark.skip
    def test__merge_reset_codes_if_no_text__real_world(self):
        foobar = colored(f'Foo:Bar', 'dark')
        actual = colored(f'Baz {foobar}', 'bold', 'bright white', 'on black')
        expected = '\x1b[1;97;40mBaz \x1b[2mFoo:Bar\x1b[0m'
        return actual, expected
    
    @pytest.mark.skip
    def test__merge_all_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(red, 'bold')
        expected = '\x1b[1;31mRed\x1b[0m'
        return actual, expected
