from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare, codes_perm
import re


######################
## Same reset codes ##
######################

# 1 inner color
###############


@print_and_compare
def test__bold_dark_bold():
    """B    F       /F/B B
       1    2   →   22;1"""
    dark = colored(' Dark ', 'dark')
    bold_dark_bold = colored(' Bold ' + dark + ' Bold ', 'bold') + ' NORMAL'
    expected = '\x1b[1m Bold \x1b[2m Dark \x1b[22;1m Bold \x1b[22m NORMAL'
    # expected = re.compile(expected_str)
    return bold_dark_bold, expected


@print_and_compare
def test__dark_bold_dark():
    dark_bold_dark = colored(' Dark ' + colored(' Bold ', 'bold') + ' Dark ', 'dark') + ' NORMAL'
    expected_str = rf'\x1b\[2m Dark \x1b\[1m Bold {codes_perm(22, 2)} Dark \x1b\[22m NORMAL'
    expected = re.compile(expected_str)
    return dark_bold_dark, expected


@print_and_compare
def test__red_green_red():
    """R    G       R
       31   32  →   31"""
    
    green = colored(' Green ', 'green')
    red_green_red = colored(' Red ' + green + ' Red ', 'red') + ' NORMAL'
    # doesn't reset green, just re-opens red (because incompatible)
    expected = '\x1b[31m Red \x1b[32m Green \x1b[31m Red \x1b[39m NORMAL'
    return red_green_red, expected


@print_and_compare
def test__onblack_ongreen_onblack():
    ongreen = colored(' OnGreen ', 'on green')
    onblack_ongreen_onblack = colored(' OnBlack ' + ongreen + ' OnBlack ', 'on black') + ' NORMAL'
    # doesn't reset OnGreen, just re-opens OnBlack (because incompatible)
    
    expected = '\x1b[40m OnBlack \x1b[42m OnGreen \x1b[40m OnBlack \x1b[49m NORMAL'
    return onblack_ongreen_onblack, expected


# 2 outer colors
################
@print_and_compare
def test__boldbrightwhite__dark__boldbrightwhite():
    """S+B  F       /F/B B
       1;97 2   →   22;1"""
    dark = colored(' Dark ', 'dark')
    boldbrightwhite__dark__boldbrightwhite = colored(' BoldBright ' + dark + ' BoldBright ', 'bold', 'bright white') + ' NORMAL'
    
    # merge dark reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize bright is not lost and is restored automatically by 22 (resetting dark)
    # TODO: why is bright restored when resetting dark?
    # In IPython:
    # # print('\x1b[97m Bright (#EEEEEC) \x1b[2m Bright and Dark (#9F9F9D) \x1b[22m Bright (#EEEEEC) \x1b[0m Normal (#AAAAAA) \x1b[2m Dark (#717171) \x1b[0m')
    expected_str = rf'{codes_perm(1, 97)} BoldBright \x1b\[2m Dark {codes_perm(22, 1)} BoldBright {codes_perm(39, 22)} NORMAL'
    expected = re.compile(expected_str)
    return boldbrightwhite__dark__boldbrightwhite, expected


@print_and_compare
def test__darkbold__brightwhite__darkbold():
    brightwhite = colored(' BrightWhite ', 'bright white')
    darkbold__brightwhite__darkbold = colored(' DarkBold ' + brightwhite + ' DarkBold ', 'bold', 'dark') + ' NORMAL'
    
    expected_str = rf'{codes_perm(1, 2)} DarkBold \x1b\[97m BrightWhite \x1b\[39m DarkBold \x1b\[22m NORMAL'
    expected = re.compile(expected_str)
    return darkbold__brightwhite__darkbold, expected
