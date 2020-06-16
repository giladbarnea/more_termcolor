import io
import re
from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare, codes_perm


###########################
## Different reset codes ##
###########################

# Trivial
#########


# 1 inner color
###############
@print_and_compare
def test__red_dark_red():
    """R    F       /F/B
       31   2   →   22"""
    dark = colored(' Dark ', 'dark')
    red_dark_red = colored(' Red ' + dark + ' Red ', 'red') + ' NORMAL'
    expected = '\x1b[31m Red \x1b[2m Dark \x1b[22m Red \x1b[39m NORMAL'
    
    # smart reset dark in the middle, and does not re-open red
    return red_dark_red, expected


@print_and_compare
def test__italic_bold_italic():
    """I    B       /F/B
       3    1   →   22"""
    bold = colored(' Bold ', 'bold')
    italic_bold_italic = colored(' Italic ' + bold + ' Italic ', 'italic') + ' NORMAL'
    expected = '\x1b[3m Italic \x1b[1m Bold \x1b[22m Italic \x1b[23m NORMAL'
    
    return italic_bold_italic, expected


@print_and_compare
def test__italic_red_italic():
    """I    R       /FG
       3    31  →   39"""
    red = colored(' Red ', 'red')
    italic_red_italic = colored(' Italic ' + red + ' Italic ', 'italic') + ' NORMAL'
    expected = '\x1b[3m Italic \x1b[31m Red \x1b[39m Italic \x1b[23m NORMAL'
    
    return italic_red_italic, expected


@print_and_compare
def test__italic_brightgreen_italic():
    """I    SG      /FG
       3    92  →   39"""
    italic_brightgreen_italic = colored(' Italic ' + colored(' BrightGreen ', 'bright green') + ' Italic ', 'italic') + ' NORMAL'
    expected = '\x1b[3m Italic \x1b[92m BrightGreen \x1b[39m Italic \x1b[23m NORMAL'
    
    return italic_brightgreen_italic, expected


@print_and_compare
def test__bold_italic_bold():
    """B    I       /I
       1    3   →   23"""
    bold_italic_bold = colored(' Bold ' + colored(' Italic ', 'italic') + ' Bold ', 'bold') + ' NORMAL'
    expected = '\x1b[1m Bold \x1b[3m Italic \x1b[23m Bold \x1b[22m NORMAL'
    
    # smart reset italic (23), no reopen bold
    return bold_italic_bold, expected


@print_and_compare
def test__brightwhite_dark_brightwhite():
    """S    F       /F
       97   2   →   22"""
    brightwhite_dark_brightwhite = colored(' Bright ' + colored(' Dark ', 'dark') + ' Bright ', 'bright white') + ' NORMAL'
    expected = '\x1b[97m Bright \x1b[2m Dark \x1b[22m Bright \x1b[39m NORMAL'
    # smart reset dark, no re-open bright
    
    return brightwhite_dark_brightwhite, expected


@print_and_compare
def test__brightwhite_red_brightwhite():
    """S    R       S
       97   31  →   97"""
    red = colored(' Red ', 'red')
    brightwhite_red_brightwhite = colored(' Bright ' + red + ' Bright ', 'bright white') + ' NORMAL'
    expected = '\x1b[97m Bright \x1b[31m Red \x1b[97m Bright \x1b[39m NORMAL'
    
    return brightwhite_red_brightwhite, expected


@print_and_compare
def test__red_onblack_red():
    onblack = colored(' OnBlack ', 'on black')
    red_onblack_red = colored(' Red ' + onblack + ' Red ', 'red') + ' NORMAL'
    expected = '\x1b[31m Red \x1b[40m OnBlack \x1b[49m Red \x1b[39m NORMAL'
    
    return red_onblack_red, expected


@print_and_compare
def test__brightred_onblack_brightred():
    onblack = colored(' OnBlack ', 'on black')
    brightred_onblack_brightred = colored(' BrightRed ' + onblack + ' BrightRed ', 'bright red') + ' NORMAL'
    expected = "\x1b[91m BrightRed \x1b[40m OnBlack \x1b[49m BrightRed \x1b[39m NORMAL"
    
    return brightred_onblack_brightred, expected


@print_and_compare
def test__onblack_brightred_onblack():
    brightred = colored(' BrightRed ', 'bright red')
    onblack_brightred_onblack = colored(' OnBlack ' + brightred + ' OnBlack ', 'on black') + ' NORMAL'
    expected = '\x1b[40m OnBlack \x1b[91m BrightRed \x1b[39m OnBlack \x1b[49m NORMAL'
    
    return onblack_brightred_onblack, expected


@print_and_compare
def test__onblack_underline_onblack():
    underline = colored(' Underline ', 'ul')
    onblack_underline_onblack = colored(' OnBlack ' + underline + ' OnBlack ', 'on black') + ' NORMAL'
    expected = '\x1b[40m OnBlack \x1b[4m Underline \x1b[24m OnBlack \x1b[49m NORMAL'
    
    return onblack_underline_onblack, expected


@print_and_compare
def test__underline_onblack_underline():
    onblack = colored(' OnBlack ', 'on black')
    underline_onblack_underline = colored(' Underline ' + onblack + ' Underline ', 'underline') + ' NORMAL'
    expected = '\x1b[4m Underline \x1b[40m OnBlack \x1b[49m Underline \x1b[24m NORMAL'
    
    return underline_onblack_underline, expected


# 2 inner colors
################
@print_and_compare
def test__brightred__onblack_bold__brightred():
    onblackbold = colored(' OnBlackBold ', 'on black', 'bold')
    brightred_onblackbold_brightred = colored(' BrightRed ' + onblackbold + ' BrightRed ', 'bright red') + ' NORMAL'
    
    expected_str = rf"\x1b\[91m BrightRed {codes_perm(40, 1)} OnBlackBold {codes_perm(49, 22)} BrightRed \x1b\[39m NORMAL"
    expected = re.compile(expected_str)
    
    return brightred_onblackbold_brightred, expected


@print_and_compare
def test__onblack__brightred_bold__onblack():
    brightredbold = colored(' BrightRedBold ', 'bright red', 'bold')
    onblack_brightredbold_onblack = colored(' OnBlack ' + brightredbold + ' OnBlack ', 'on black') + ' NORMAL'
    expected_str = rf'\x1b\[40m OnBlack {codes_perm(91, 1)} BrightRedBold {codes_perm(39, 22)} OnBlack \x1b\[49m NORMAL'
    expected = re.compile(expected_str)
    
    return onblack_brightredbold_onblack, expected


@print_and_compare
def test__bold__green_on_black__bold():
    greenonblack = colored(' GreenOnBlack ', 'green', 'on black')
    bold_greenonblack_bold = colored(' Bold ' + greenonblack + ' Bold ', 'bold') + ' NORMAL'
    expected_str = rf'\x1b\[1m Bold {codes_perm(32, 40)} GreenOnBlack {codes_perm(39, 49)} Bold \x1b\[22m NORMAL'
    expected = re.compile(expected_str)
    return bold_greenonblack_bold, expected


# 2 outer colors
################
@print_and_compare
def test__redonblack__bold__redonblack():
    bold = colored(' Bold ', 'bold')
    redonblack__bold__redonblack = colored(' RedOnBlack ' + bold + ' RedOnBlack ', 'red', 'on black') + ' NORMAL'
    expected_str = rf'{codes_perm(31, 40)} RedOnBlack \x1b\[1m Bold \x1b\[22m RedOnBlack {codes_perm(39, 49)} NORMAL'
    expected = re.compile(expected_str)
    
    return redonblack__bold__redonblack, expected


@print_and_compare
def test__underlineonblack__red__underlineonblack():
    red = colored(' Red ', 'red')
    underlineonblack__red__underlineonblack = colored(' UnderlineOnBlack ' + red + ' UnderlineOnBlack ', 'ul', 'on black') + ' NORMAL'
    expected_str = rf'{codes_perm(4, 40)} UnderlineOnBlack \x1b\[31m Red \x1b\[39m UnderlineOnBlack {codes_perm(49, 24)} NORMAL'
    expected = re.compile(expected_str)
    
    return underlineonblack__red__underlineonblack, expected


@print_and_compare
def test__underlinegreen__onblack__underlinegreen():
    onblack = colored(' OnBlack ', 'on black')
    underlinegreen__onblack__underlinegreen = colored(' UnderlineGreen ' + onblack + ' UnderlineGreen ', 'ul', 'green') + ' NORMAL'
    expected_str = rf'{codes_perm(4, 32)} UnderlineGreen \x1b\[40m OnBlack \x1b\[49m UnderlineGreen {codes_perm(39, 24)} NORMAL'
    expected = re.compile(expected_str)
    
    return underlinegreen__onblack__underlinegreen, expected
