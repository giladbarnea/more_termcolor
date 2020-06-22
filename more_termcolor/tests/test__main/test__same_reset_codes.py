import pytest
from snoop import snoop

from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare, codes_perm
from more_termcolor.main import openers_with_same_reset_code, ColorScope, Inside, ColorOpener
import re


######################
## Same reset codes ##
######################

# 1 inner color
###############
@print_and_compare
class Test_1_inside_color:
    
    def test__bold_dark_bold(self):
        """B    F       /F/B B
           1    2   →   22;1"""
        dark = colored(' Dark ', 'dark')
        assert dark == '\x1b[2m Dark \x1b[22m'
        bold_dark_bold = colored(' Bold ' + dark + ' Bold ', 'bold') + ' NORMAL'
        expected = '\x1b[1m Bold \x1b[2m Dark \x1b[22;1m Bold \x1b[22m NORMAL'
        # expected = re.compile(expected_str)
        return bold_dark_bold, expected
    
    def test__dark_bold_dark(self):
        dark_bold_dark = colored(' Dark ' + colored(' Bold ', 'bold') + ' Dark ', 'dark') + ' NORMAL'
        expected = f'\x1b[2m Dark \x1b[1m Bold \x1b[22;2m Dark \x1b[22m NORMAL'
        # expected = re.compile(expected_str)
        return dark_bold_dark, expected
    
    def test__red_green_red(self):
        """R    G       R
           31   32  →   31"""
        
        green = colored(' Green ', 'green')
        red_green_red = colored(' Red ' + green + ' Red ', 'red') + ' NORMAL'
        # doesn't reset green, just re-opens red (because incompatible)
        expected = '\x1b[31m Red \x1b[32m Green \x1b[31m Red \x1b[39m NORMAL'
        return red_green_red, expected
    
    def test__onblack_ongreen_onblack(self):
        ongreen = colored(' OnGreen ', 'on green')
        onblack_ongreen_onblack = colored(' OnBlack ' + ongreen + ' OnBlack ', 'on black') + ' NORMAL'
        # doesn't reset OnGreen, just re-opens OnBlack (because incompatible)
        
        expected = '\x1b[40m OnBlack \x1b[42m OnGreen \x1b[40m OnBlack \x1b[49m NORMAL'
        return onblack_ongreen_onblack, expected
    
    # 2 outer colors
    ################
    
    @pytest.mark.skip('advanced')
    def test__inside_opens_already_open(self):
        inside = colored('Inside', 'dark')
        actual = colored(f'Outside {inside} Outside', 'dark')
        expected = '\x1b[2mOutside Inside Outside\x1b[22m'
        return actual, expected


@print_and_compare
class Test_2_inside_colors:
    def test__bold__red_dark__bold(self):
        inside = colored(' RedDark ', 'red', 'dark')
        assert inside == '\x1b[31;2m RedDark \x1b[39;22m'
        actual = colored(f'Bold {inside} Bold', 'bold') + ' NORMAL'
        expected = '\x1b[1mBold \x1b[31;2m RedDark \x1b[22;1;39m Bold\x1b[22m NORMAL'
        return actual, expected
    
    def test__bold__red_bold__bold(self):
        inside = colored(' Inside ', 'red', 'bold')
        actual = colored(f'Outside {inside} Outside', 'bold')
        expected = '\x1b[1mOutside \x1b[31m Inside \x1b[39m Outside\x1b[22m'
        return actual, expected


@print_and_compare
class Test_2_outside_colors:
    def test__bold_brightwhite__dark__bold_brightwhite(self):
        """S+B  F       /F/B B
           1;97 2   →   22;1"""
        dark = colored(' Dark ', 'dark')
        bold_brightwhite__dark__bold_brightwhite = colored(' BoldBright ' + dark + ' BoldBright ', 'bold', 'bright white') + ' NORMAL'
        
        # merge dark reset with bold re-open (22;1)
        # recognize bold is lost by 22, so need to re-open it
        # recognize bright is not lost and is restored automatically by 22 (resetting dark)
        # TODO: why is bright restored when resetting dark?
        # In IPython:
        # # print('\x1b[97m Bright (#EEEEEC) \x1b[2m Bright and Dark (#9F9F9D) \x1b[22m Bright (#EEEEEC) \x1b[0m Normal (#AAAAAA) \x1b[2m Dark (#717171) \x1b[0m')
        expected = f'\x1b[1;97m BoldBright \x1b[2m Dark \x1b[22;1m BoldBright \x1b[39;22m NORMAL'
        return bold_brightwhite__dark__bold_brightwhite, expected
    
    def test__dark_bold__brightwhite__dark_bold(self):
        brightwhite = colored(' BrightWhite ', 'bright white')
        dark_bold__brightwhite__dark_bold = colored(' DarkBold ' + brightwhite + ' DarkBold ', 'bold', 'dark') + ' NORMAL'
        
        expected = f'\x1b[1;2m DarkBold \x1b[97m BrightWhite \x1b[39m DarkBold \x1b[22m NORMAL'
        return dark_bold__brightwhite__dark_bold, expected
    
    def test__bold_dark__red_dark__bold_dark(self):
        reddark = colored(' RedDark ', 'red', 'dark')
        bold_dark__red_dark__bold_dark = colored(' BoldDark ' + reddark + ' BoldDark ', 'bold', 'dark') + ' NORMAL'
        
        expected = f'\x1b[1;2m BoldDark \x1b[31m RedDark \x1b[39m BoldDark \x1b[22m NORMAL'
        return bold_dark__red_dark__bold_dark, expected
    
    def test__bold_green__red_dark__bold_green(self):
        reddark = colored(' RedDark ', 'red', 'dark')
        bold_green__red_dark__bold_green = colored(' BoldGreen ' + reddark + ' BoldGreen ', 'bold', 'green') + ' NORMAL'
        
        expected = f'\x1b[1;32m BoldGreen \x1b[31;2m RedDark \x1b[22;1;32m BoldGreen \x1b[22;39m NORMAL'
        return bold_green__red_dark__bold_green, expected
