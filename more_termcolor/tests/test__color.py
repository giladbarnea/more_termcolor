"""
incompat
R    G       R
31   32  →   31
outer is std:
    nested is std:
        re-open outer

compat
R    F       /F/B
31   2   →   22
outer is std:
    nested is fmt:
        reset nested

adv_0
I    B       /F/B
3    1   →   22
outer is fmt:
    nested is fmt:
        outer.reset != nested.reset:
            reset nested
            
adv_1
I    R       /FG
3    31  →   39
outer is fmt:
    nested is std:
        reset fg
        
adv_1_b
I    SG      /FG
3    92  →   39
outer is fmt:
    nested is sat:
        reset fg

adv_2
B    I       /I
1    3   →   23
outer is fmt:
    nested is fmt:
        outer.reset != nested.reset:
            reset nested

adv_3
B    F       /F/B B
1    2   →   22;1
outer is fmt:
    nested is fmt:
        outer.reset == nested.reset:
            reset nested
            re-open outer

adv_4
S    F       /F
97   2   →   22
outer is sat:
    nested is fmt:
        reset nested

adv_5
S    R       S
97   31  →   97
outer is sat:
    nested is std:
        re-open outer

compat_and_incompat
S+B  F       /F/B B
1;97 2   →   22;1
outer has fmt:
    nested is fmt:
        outer.fmt.reset == nested.reset:
            reset nested
            re-open outer

"""

import io

from more_termcolor import util
from more_termcolor.color import colored, cprint


def _print(description, string):
    util.spacyprint(f'{description}:', string, repr(string))


def _actualprint(string):
    _print('actual', string)


def _expectedprint(string):
    _print('expected', string)


###########################
## Different reset codes ##
###########################

# Trivial
#########


# 1 inner color
###############
def test__red_dark_red():
    """R    F       /F/B
       31   2   →   22"""
    darkred = colored('DarkRed', 'dark')
    red_dark_red = colored('Red' + darkred + 'Red', 'red')
    _actualprint(red_dark_red)
    expected = '\x1b[31mRed\x1b[2mDarkRed\x1b[22mRed\x1b[0m'
    _expectedprint(expected)
    # smart reset dark in the middle, and does not re-open red
    assert red_dark_red == expected


def test__italic_bold_italic():
    """I    B       /F/B
       3    1   →   22"""
    bolditalic = colored('BoldAndItalic', 'bold')
    italic_bold_italic = colored('Italic' + bolditalic + 'Italic', 'italic')
    _actualprint(italic_bold_italic)
    expected = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[22mItalic\x1b[0m'
    _expectedprint(expected)
    assert italic_bold_italic == expected


def test__italic_red_italic():
    """I    R       /FG
       3    31  →   39"""
    italic_red_italic = colored('Italic' + colored('RedItalic', 'red') + 'Italic', 'italic')
    _actualprint(italic_red_italic)
    expected = '\x1b[3mItalic\x1b[31mRedItalic\x1b[39mItalic\x1b[0m'
    _expectedprint(expected)
    assert italic_red_italic == expected


def test__italic_satgreen_italic():
    """I    SG      /FG
       3    92  →   39"""
    italic_satgreen_italic = colored('Italic' + colored('SatGreenItalic', 'sat green') + 'Italic', 'italic')
    _actualprint(italic_satgreen_italic)
    expected = '\x1b[3mItalic\x1b[92mSatGreenItalic\x1b[39mItalic\x1b[0m'
    _expectedprint(expected)
    assert italic_satgreen_italic == expected


def test__bold_italic_bold():
    """B    I       /I
       1    3   →   23"""
    bold_italic_bold = colored('Bold' + colored('ItalicAndBold', 'italic') + 'Bold', 'bold')
    _actualprint(bold_italic_bold)
    expected = '\x1b[1mBold\x1b[3mItalicAndBold\x1b[23mBold\x1b[0m'
    _expectedprint(expected)
    # smart reset italic (23), no reopen bold
    assert bold_italic_bold == expected


def test__satwhite_dark_satwhite():
    """S    F       /F
       97   2   →   22"""
    satwhite_dark_satwhite = colored('Sat' + colored('DarkAndSat', 'dark') + 'Sat', 'sat white')
    _actualprint(satwhite_dark_satwhite)
    expected = '\x1b[97mSat\x1b[2mDarkAndSat\x1b[22mSat\x1b[0m'
    # smart reset dark, no re-open sat
    _expectedprint(expected)
    assert satwhite_dark_satwhite == expected


def test__satwhite_red_satwhite():
    """S    R       S
       97   31  →   97"""
    red = colored('Red', 'red')
    satwhite_red_satwhite = colored('Sat' + red + 'Sat', 'sat white')
    _actualprint(satwhite_red_satwhite)
    expected = '\x1b[97mSat\x1b[31mRed\x1b[97mSat\x1b[0m'
    _expectedprint(expected)
    assert satwhite_red_satwhite == expected


def test__red_onblack_red():
    onblack = colored('OnBlack', 'on black')
    red_onblack_red = colored('Red' + onblack + 'Red', 'red')
    _actualprint(red_onblack_red)
    expected = '\x1b[31mRed\x1b[40mOnBlack\x1b[49mRed\x1b[0m'
    _expectedprint(expected)
    
    assert red_onblack_red == expected


def test__satred_onblack_satred():
    onblack = colored('OnBlack', 'on black')
    satred_onblack_satred = colored('SatRed' + onblack + 'SatRed', 'sat red')
    _actualprint(satred_onblack_satred)
    expected = "\x1b[91mSatRed\x1b[40mOnBlack\x1b[49mSatRed\x1b[0m"
    _expectedprint(expected)
    assert satred_onblack_satred == expected


def test__onblack_satred_onblack():
    satred = colored('SatRed', 'sat red')
    onblack_satred_onblack = colored('OnBlack' + satred + 'OnBlack', 'on black')
    _actualprint(onblack_satred_onblack)
    expected = '\x1b[40mOnBlack\x1b[91mSatRed\x1b[39mOnBlack\x1b[0m'
    _expectedprint(expected)
    assert onblack_satred_onblack == expected


def test__onblack_underline_onblack():
    underline = colored('Underline', 'ul')
    onblack_underline_onblack = colored('OnBlack' + underline + 'OnBlack', 'on black')
    _actualprint(onblack_underline_onblack)
    expected = '\x1b[40mOnBlack\x1b[4mUnderline\x1b[24mOnBlack\x1b[0m'
    _expectedprint(expected)
    assert onblack_underline_onblack == expected


def test__underline_onblack_underline():
    onblack = colored('OnBlack', 'on black')
    underline_onblack_underline = colored('Underline' + onblack + 'Underline', 'underline')
    _actualprint(underline_onblack_underline)
    expected = '\x1b[4mUnderline\x1b[40mOnBlack\x1b[49mUnderline\x1b[0m'
    _expectedprint(expected)
    assert underline_onblack_underline == expected


# 2 inner colors
################
def test__satred__onblack_bold__satred():
    onblackbold = colored(' OnBlackBold ', 'on black', 'bold')
    satred_onblackbold_satred = colored(' SatRed ' + onblackbold + ' SatRed ', 'sat red')
    _actualprint(satred_onblackbold_satred)
    expected = "\x1b[91m SatRed \x1b[40;1m OnBlackBold \x1b[49;22m SatRed \x1b[0m"
    _expectedprint(expected)
    assert satred_onblackbold_satred == expected


def test__onblack__satred_bold__onblack():
    satredbold = colored(' SatRedBold ', 'sat red', 'bold')
    onblack_satredbold_onblack = colored(' OnBlack ' + satredbold + ' OnBlack ', 'on black')
    _actualprint(onblack_satredbold_onblack)
    expected = '\x1b[40m OnBlack \x1b[91;1m SatRedBold \x1b[39;22m OnBlack \x1b[0m'
    _expectedprint(expected)
    assert onblack_satredbold_onblack == expected


def test__bold__green_on_black__bold():
    greenonblack = colored(' GreenOnBlack ', 'green', 'on black')
    bold_greenonblack_bold = colored(' Bold ' + greenonblack + ' Bold ', 'bold')
    _actualprint(bold_greenonblack_bold)
    expected = '\x1b[1m Bold \x1b[32;40m GreenOnBlack \x1b[39;49m Bold \x1b[0m'
    _expectedprint(expected)
    assert bold_greenonblack_bold == expected


# 2 outer colors
################
def test__redonblack__bold__redonblack():
    bold = colored(' Bold ', 'bold')
    redonblack__bold__redonblack = colored(' RedOnBlack ' + bold + ' RedOnBlack ', 'red', 'on black')
    _actualprint(redonblack__bold__redonblack)
    expected = '\x1b[31;40m RedOnBlack \x1b[1m Bold \x1b[22m RedOnBlack \x1b[0m'
    _expectedprint(expected)
    assert redonblack__bold__redonblack == expected


def test__underlineonblack__red__underlineonblack():
    red = colored(' Red ', 'red')
    underlineonblack__red__underlineonblack = colored(' UnderlineOnBlack ' + red + ' UnderlineOnBlack ', 'ul', 'on black')
    _actualprint(underlineonblack__red__underlineonblack)
    expected = '\x1b[4;40m UnderlineOnBlack \x1b[31m Red \x1b[39m UnderlineOnBlack \x1b[0m'
    _expectedprint(expected)
    assert underlineonblack__red__underlineonblack == expected


def test__underlinegreen__onblack__underlinegreen():
    onblack = colored(' OnBlack ', 'on black')
    underlinegreen__onblack__underlinegreen = colored(' UnderlineGreen ' + onblack + ' UnderlineGreen ', 'ul', 'green')
    _actualprint(underlinegreen__onblack__underlinegreen)
    expected = '\x1b[4;32m UnderlineGreen \x1b[40m OnBlack \x1b[49m UnderlineGreen \x1b[0m'
    _expectedprint(expected)
    assert underlinegreen__onblack__underlinegreen == expected


######################
## Same reset codes ##
######################

# 1 inner color
###############
def test__bold_dark_bold():
    """B    F       /F/B B
       1    2   →   22;1"""
    bold_dark_bold = colored('Bold' + colored('DarkAndBold', 'dark') + 'Bold', 'bold')
    _actualprint(bold_dark_bold)
    expected = '\x1b[1mBold\x1b[2mDarkAndBold\x1b[22;1mBold\x1b[0m'
    _expectedprint(expected)
    assert bold_dark_bold == expected


def test__dark_bold_dark():
    dark_bold_dark = colored(' Dark ' + colored(' DarkAndBold ', 'bold') + ' Dark ', 'dark')
    _actualprint(dark_bold_dark)
    expected = '\x1b[2m Dark \x1b[1m DarkAndBold \x1b[22;2m Dark \x1b[0m'
    _expectedprint(expected)
    assert dark_bold_dark == expected


def test__red_green_red():
    """R    G       R
       31   32  →   31"""
    
    green = colored('Green', 'green')
    red_green_red = colored('Red' + green + 'Red', 'red')
    _actualprint(red_green_red)
    # doesn't reset green, just re-opens red (because incompatible)
    expected = '\x1b[31mRed\x1b[32mGreen\x1b[31mRed\x1b[0m'
    _expectedprint(expected)
    assert red_green_red == expected


def test__onblack_ongreen_onblack():
    ongreen = colored(' OnGreen ', 'on green')
    onblack_ongreen_onblack = colored(' OnBlack ' + ongreen + ' OnBlack ', 'on black')
    _actualprint(onblack_ongreen_onblack)
    expected = '\x1b[40m OnBlack \x1b[42m OnGreen \x1b[49;40m OnBlack \x1b[0m'
    _expectedprint(expected)
    assert onblack_ongreen_onblack == expected


# 2 outer colors
################
def test__boldsatwhite__dark__boldsatwhite():
    """S+B  F       /F/B B
       1;97 2   →   22;1"""
    dark = colored(' Dark ', 'dark')
    boldsatwhite__dark__boldsatwhite = colored(' BoldSat ' + dark + ' BoldSat ', 'bold', 'sat white')
    _actualprint(boldsatwhite__dark__boldsatwhite)
    # merge dark reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize sat is not lost and is restored automatically by 22 (resetting dark)
    # TODO: why is sat restored when resetting dark?
    #  In IPython:
    # # print('\x1b[97m Saturated (#EEEEEC) \x1b[2m Saturated and Dark (#9F9F9D) \x1b[22m Saturated (#EEEEEC) \x1b[0m Normal (#AAAAAA) \x1b[2m Dark (#717171) \x1b[0m')
    expected = '\x1b[1;97m BoldSat \x1b[2m Dark \x1b[22;1m BoldSat \x1b[0m'
    _expectedprint(expected)
    
    assert boldsatwhite__dark__boldsatwhite == expected


def test__darkbold__satwhite__darkbold():
    satwhite = colored(' SatWhite ', 'sat white')
    darkbold__satwhite__darkbold = colored(' DarkBold ' + satwhite + ' DarkBold ', 'bold', 'dark')
    _actualprint(darkbold__satwhite__darkbold)
    expected = '\x1b[1;2m DarkBold \x1b[97m SatWhite \x1b[39m DarkBold \x1b[0m'
    _expectedprint(expected)
    assert darkbold__satwhite__darkbold == expected


#############
# Bad usage #
#############

# Trivial
#########
def test__no_color():
    assert colored('foo') == 'foo'


def test__same_color():
    actual = colored('foo', 'red', 'dark', 'red')
    _actualprint(actual)
    expected = '\x1b[31;2mfoo\x1b[0m'
    _expectedprint(expected)
    assert actual == expected
    
    actual = colored('foo', 'dark', 'dark', 'red')
    _actualprint(actual)
    expected = '\x1b[2;31mfoo\x1b[0m'
    _expectedprint(expected)
    assert actual == expected


def test__too_many_colors():
    actual = colored('foo', "red", "on black", "bold", "dark", "italic", "underline", "blink", "reverse", "strike", "overline")
    _actualprint(actual)
    expected = '\x1b[31;40;1;2;3;4;5;7;9;53mfoo\x1b[0m'
    _expectedprint(expected)
    assert actual == expected


#########################################
# compatibility with original termcolor #
#########################################
def test__cprint():
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on_red', attrs=['bold'], file=f)
    s = f.getvalue()
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on red', 'bold', file=f)
    assert f.getvalue() == s
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
