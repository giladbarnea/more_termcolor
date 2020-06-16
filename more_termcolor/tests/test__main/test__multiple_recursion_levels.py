import pytest
import pickle
from more_termcolor import colored, bold, dark, ita, brightgreen, ul
from more_termcolor.tests.common import print_and_compare
from pathlib import Path


@print_and_compare
class Test:
    def test__merge_open_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(f'{red} Bold', 'bold')
        expected = '\x1b[1;31mRed\x1b[39m Bold\x1b[0m'
        return actual, expected
    
    def test__merge_reset_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(f'Bold {red}', 'bold')
        expected = '\x1b[1mBold \x1b[31mRed\x1b[0m'
        return actual, expected
    
    def test__merge_reset_codes_if_no_text__real_world(self):
        foobar = colored(f'Foo:Bar', 'dark')
        actual = colored(f'Baz {foobar}', 'bold', 'bright white', 'on black')
        expected = '\x1b[1;97;40mBaz \x1b[2mFoo:Bar\x1b[0m'
        return actual, expected
    
    def test__merge_all_codes_if_no_text(self):
        red = colored('Red', 'red')
        actual = colored(red, 'bold')
        expected = '\x1b[1;31mRed\x1b[0m'
        return actual, expected
    
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
        actual = brightgreen(f"Overlapping colors {add_up} {if_possible} and {dont} cancel each other out")
        expected = "\x1b[92mOverlapping colors \x1b[1madd-up\x1b[22m \x1b[2m(if possible)\x1b[22m and \x1b[3;4mdon't\x1b[23;24m cancel each other out\x1b[0m"
        return actual, expected
