import pickle
import re
from pathlib import Path

import pytest

from more_termcolor import colored, bold, dark, ita, brightgreen, ul
from more_termcolor.tests.common import print_and_compare, codes_perm


@print_and_compare
class TestMerge:
    def test__merge_open_codes_if_no_text__different_reset(self):
        red = colored('Red', 'red')
        actual = colored(f'{red}Bold', 'bold') + ' NORMAL'
        expected = f'\x1b[1;31mRed\x1b[39mBold\x1b[22m NORMAL'
        return actual, expected
    
    def test__merge_reset_codes_if_no_text__different_reset(self):
        red = colored('Red', 'red')
        actual = colored(f'Bold {red}', 'bold') + ' NORMAL'
        expected = f'\x1b[1mBold \x1b[31mRed\x1b[39;22m NORMAL'
        return actual, expected
    
    def test__merge_open_codes_if_no_text__same_reset(self):
        dark_ = colored('Dark', 'dark')
        actual = colored(f'{dark_}Bold', 'bold') + ' NORMAL'
        expected = f'\x1b[2mDark\x1b[1mBold\x1b[22m NORMAL'
        return actual, expected
    
    def test__merge_reset_codes_if_no_text__same_reset(self):
        dark_ = colored('Dark', 'dark')
        actual = colored(f'Bold {dark_}', 'bold') + ' NORMAL'
        expected = f'\x1b[1mBold \x1b[2mDark\x1b[22m NORMAL'
        return actual, expected

    def test__merge_open_codes_if_no_text__same_open(self):
        bold_ = colored('Bold', 'bold')
        actual = colored(f'{bold_}Bold', 'bold') + ' NORMAL'
        expected = f'\x1b[2mBoldBold\x1b[22m NORMAL'
        return actual, expected

    def test__merge_reset_codes_if_no_text__same_open(self):
        bold_ = colored('Bold', 'bold')
        actual = colored(f'Bold {bold_}', 'bold') + ' NORMAL'
        expected = f'\x1b[1mBold Bold\x1b[22m NORMAL'
        return actual, expected
    
    def test__merge_reset_codes_if_no_text__real_world(self):
        foobar = colored(f'Foo:Bar', 'dark')
        actual = colored(f'Baz {foobar}', 'bold', 'bright magenta', 'on black') + ' NORMAL'
        expected = f'\x1b[1;95;40mBaz\x1b[2mFoo:Bar\x1b[22;49;39m NORMAL'
        return actual, expected
    
    def test__merge_all_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(red, 'bold') + ' NORMAL'
        expected_str = rf'{codes_perm(1, 31)}Red{codes_perm(39, 22)} NORMAL'
        expected = re.compile(expected_str)
        return actual, expected


@print_and_compare
class TestRealWorld:
    @pytest.mark.skip
    def test__exchandler(self):
        with open(Path(__file__).parent / 'exchandler_colors.pickle', mode='rb') as f:
            colors = pickle.load(f)
        with open(Path(__file__).parent / 'exchandler_text.pickle', mode='rb') as f:
            text = pickle.load(f)
        with open(Path(__file__).parent / 'exchandler_expected.pickle', mode='rb') as f:
            expected = pickle.load(f)
        actual = colored(text, *colors)
        return actual, expected
    
    def test__readme_example(self):
        add_up = bold('add-up')
        if_possible = dark('(if possible)')
        dont = ita(ul("don't"))
        actual = brightgreen(f"Overlapping colors {add_up} {if_possible} and {dont} cancel each other out") + ' NORMAL'
        expected_str = rf"\x1b\[92mOverlapping colors \x1b\[1madd-up\x1b\[22m \x1b\[2m(if possible)\x1b\[22m and {codes_perm(3, 4)}don't{codes_perm(23, 24)} cancel each other out\x1b\[39m NORMAL"
        expected = re.compile(expected_str)
        return actual, expected
