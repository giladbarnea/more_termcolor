import io

from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare


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
    darkred = colored(' DarkRed ', 'dark')
    red_dark_red = colored(' Red ' + darkred + ' Red ', 'red')
    expected = '\x1b[31m Red \x1b[2m DarkRed \x1b[22m Red \x1b[0m'
    
    # smart reset dark in the middle, and does not re-open red
    return red_dark_red, expected


@print_and_compare
def test__italic_bold_italic():
    """I    B       /F/B
       3    1   →   22"""
    bolditalic = colored('BoldAndItalic', 'bold')
    italic_bold_italic = colored('Italic' + bolditalic + 'Italic', 'italic')
    expected = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[22mItalic\x1b[0m'
    
    return italic_bold_italic, expected


@print_and_compare
def test__italic_red_italic():
    """I    R       /FG
       3    31  →   39"""
    italic_red_italic = colored('Italic' + colored('RedItalic', 'red') + 'Italic', 'italic')
    expected = '\x1b[3mItalic\x1b[31mRedItalic\x1b[39mItalic\x1b[0m'
    
    return italic_red_italic, expected


@print_and_compare
def test__italic_brightgreen_italic():
    """I    SG      /FG
       3    92  →   39"""
    italic_brightgreen_italic = colored('Italic' + colored('BrightGreenItalic', 'bright green') + 'Italic', 'italic')
    expected = '\x1b[3mItalic\x1b[92mBrightGreenItalic\x1b[39mItalic\x1b[0m'
    
    return italic_brightgreen_italic, expected


@print_and_compare
def test__bold_italic_bold():
    """B    I       /I
       1    3   →   23"""
    bold_italic_bold = colored('Bold' + colored('ItalicAndBold', 'italic') + 'Bold', 'bold')
    expected = '\x1b[1mBold\x1b[3mItalicAndBold\x1b[23mBold\x1b[0m'
    
    # smart reset italic (23), no reopen bold
    return bold_italic_bold, expected


@print_and_compare
def test__brightwhite_dark_brightwhite():
    """S    F       /F
       97   2   →   22"""
    brightwhite_dark_brightwhite = colored('Bright' + colored('DarkAndBright', 'dark') + 'Bright', 'bright white')
    expected = '\x1b[97mBright\x1b[2mDarkAndBright\x1b[22mBright\x1b[0m'
    # smart reset dark, no re-open bright
    
    return brightwhite_dark_brightwhite, expected


@print_and_compare
def test__brightwhite_red_brightwhite():
    """S    R       S
       97   31  →   97"""
    red = colored('Red', 'red')
    brightwhite_red_brightwhite = colored('Bright' + red + 'Bright', 'bright white')
    expected = '\x1b[97mBright\x1b[31mRed\x1b[97mBright\x1b[0m'
    
    return brightwhite_red_brightwhite, expected


@print_and_compare
def test__red_onblack_red():
    onblack = colored('OnBlack', 'on black')
    red_onblack_red = colored('Red' + onblack + 'Red', 'red')
    expected = '\x1b[31mRed\x1b[40mOnBlack\x1b[49mRed\x1b[0m'
    
    return red_onblack_red, expected


@print_and_compare
def test__brightred_onblack_brightred():
    onblack = colored('OnBlack', 'on black')
    brightred_onblack_brightred = colored('BrightRed' + onblack + 'BrightRed', 'bright red')
    expected = "\x1b[91mBrightRed\x1b[40mOnBlack\x1b[49mBrightRed\x1b[0m"
    
    return brightred_onblack_brightred, expected


@print_and_compare
def test__onblack_brightred_onblack():
    brightred = colored('BrightRed', 'bright red')
    onblack_brightred_onblack = colored('OnBlack' + brightred + 'OnBlack', 'on black')
    expected = '\x1b[40mOnBlack\x1b[91mBrightRed\x1b[39mOnBlack\x1b[0m'
    
    return onblack_brightred_onblack, expected


@print_and_compare
def test__onblack_underline_onblack():
    underline = colored('Underline', 'ul')
    onblack_underline_onblack = colored('OnBlack' + underline + 'OnBlack', 'on black')
    expected = '\x1b[40mOnBlack\x1b[4mUnderline\x1b[24mOnBlack\x1b[0m'
    
    return onblack_underline_onblack, expected


@print_and_compare
def test__underline_onblack_underline():
    onblack = colored('OnBlack', 'on black')
    underline_onblack_underline = colored('Underline' + onblack + 'Underline', 'underline')
    expected = '\x1b[4mUnderline\x1b[40mOnBlack\x1b[49mUnderline\x1b[0m'
    
    return underline_onblack_underline, expected


# 2 inner colors
################
@print_and_compare
def test__brightred__onblack_bold__brightred():
    onblackbold = colored(' OnBlackBold ', 'on black', 'bold')
    brightred_onblackbold_brightred = colored(' BrightRed ' + onblackbold + ' BrightRed ', 'bright red')
    expected = "\x1b[91m BrightRed \x1b[40;1m OnBlackBold \x1b[49;22m BrightRed \x1b[0m"
    
    return brightred_onblackbold_brightred, expected


@print_and_compare
def test__onblack__brightred_bold__onblack():
    brightredbold = colored(' BrightRedBold ', 'bright red', 'bold')
    onblack_brightredbold_onblack = colored(' OnBlack ' + brightredbold + ' OnBlack ', 'on black')
    expected = '\x1b[40m OnBlack \x1b[91;1m BrightRedBold \x1b[39;22m OnBlack \x1b[0m'
    
    return onblack_brightredbold_onblack, expected


@print_and_compare
def test__bold__green_on_black__bold():
    greenonblack = colored(' GreenOnBlack ', 'green', 'on black')
    bold_greenonblack_bold = colored(' Bold ' + greenonblack + ' Bold ', 'bold')
    expected = '\x1b[1m Bold \x1b[32;40m GreenOnBlack \x1b[39;49m Bold \x1b[0m'
    
    return bold_greenonblack_bold, expected


# 2 outer colors
################
@print_and_compare
def test__redonblack__bold__redonblack():
    bold = colored(' Bold ', 'bold')
    redonblack__bold__redonblack = colored(' RedOnBlack ' + bold + ' RedOnBlack ', 'red', 'on black')
    expected = '\x1b[31;40m RedOnBlack \x1b[1m Bold \x1b[22m RedOnBlack \x1b[0m'
    
    return redonblack__bold__redonblack, expected


@print_and_compare
def test__underlineonblack__red__underlineonblack():
    red = colored(' Red ', 'red')
    underlineonblack__red__underlineonblack = colored(' UnderlineOnBlack ' + red + ' UnderlineOnBlack ', 'ul', 'on black')
    expected = '\x1b[4;40m UnderlineOnBlack \x1b[31m Red \x1b[39m UnderlineOnBlack \x1b[0m'
    
    return underlineonblack__red__underlineonblack, expected


@print_and_compare
def test__underlinegreen__onblack__underlinegreen():
    onblack = colored(' OnBlack ', 'on black')
    underlinegreen__onblack__underlinegreen = colored(' UnderlineGreen ' + onblack + ' UnderlineGreen ', 'ul', 'green')
    expected = '\x1b[4;32m UnderlineGreen \x1b[40m OnBlack \x1b[49m UnderlineGreen \x1b[0m'
    
    return underlinegreen__onblack__underlinegreen, expected
