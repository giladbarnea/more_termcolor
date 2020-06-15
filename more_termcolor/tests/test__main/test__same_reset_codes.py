from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare


######################
## Same reset codes ##
######################

# 1 inner color
###############


@print_and_compare
def test__bold_dark_bold():
    """B    F       /F/B B
       1    2   →   22;1"""
    bold_dark_bold = colored('Bold' + colored('DarkAndBold', 'dark') + 'Bold', 'bold')
    expected = '\x1b[1mBold\x1b[2mDarkAndBold\x1b[22;1mBold\x1b[0m'
    return bold_dark_bold, expected


@print_and_compare
def test__dark_bold_dark():
    dark_bold_dark = colored(' Dark ' + colored(' DarkAndBold ', 'bold') + ' Dark ', 'dark')
    expected = '\x1b[2m Dark \x1b[1m DarkAndBold \x1b[22;2m Dark \x1b[0m'
    return dark_bold_dark, expected


@print_and_compare
def test__red_green_red():
    """R    G       R
       31   32  →   31"""
    
    green = colored('Green', 'green')
    red_green_red = colored('Red' + green + 'Red', 'red')
    # doesn't reset green, just re-opens red (because incompatible)
    expected = '\x1b[31mRed\x1b[32mGreen\x1b[31mRed\x1b[0m'
    return red_green_red, expected


@print_and_compare
def test__onblack_ongreen_onblack():
    ongreen = colored(' OnGreen ', 'on green')
    onblack_ongreen_onblack = colored(' OnBlack ' + ongreen + ' OnBlack ', 'on black')
    
    expected = '\x1b[40m OnBlack \x1b[42m OnGreen \x1b[49;40m OnBlack \x1b[0m'
    
    return onblack_ongreen_onblack, expected


# 2 outer colors
################
@print_and_compare
def test__boldbrightwhite__dark__boldbrightwhite():
    """S+B  F       /F/B B
       1;97 2   →   22;1"""
    dark = colored(' Dark ', 'dark')
    boldbrightwhite__dark__boldbrightwhite = colored(' BoldBright ' + dark + ' BoldBright ', 'bold', 'bright white')
    
    # merge dark reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize bright is not lost and is restored automatically by 22 (resetting dark)
    # TODO: why is bright restored when resetting dark?
    # In IPython:
    # # print('\x1b[97m Bright (#EEEEEC) \x1b[2m Bright and Dark (#9F9F9D) \x1b[22m Bright (#EEEEEC) \x1b[0m Normal (#AAAAAA) \x1b[2m Dark (#717171) \x1b[0m')
    expected = '\x1b[1;97m BoldBright \x1b[2m Dark \x1b[22;1m BoldBright \x1b[0m'
    
    return boldbrightwhite__dark__boldbrightwhite, expected


@print_and_compare
def test__darkbold__brightwhite__darkbold():
    brightwhite = colored(' BrightWhite ', 'bright white')
    darkbold__brightwhite__darkbold = colored(' DarkBold ' + brightwhite + ' DarkBold ', 'bold', 'dark')
    
    expected = '\x1b[1;2m DarkBold \x1b[97m BrightWhite \x1b[39m DarkBold \x1b[0m'
    
    return darkbold__brightwhite__darkbold, expected