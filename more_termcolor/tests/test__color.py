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
    util.spacyprint(f'red_dark_red:', red_dark_red)
    expected = '\x1b[31mRed\x1b[2mDarkRed\x1b[22mRed\x1b[0m'
    util.spacyprint('expected:', expected)
    # smart reset dark in the middle, and does not re-open red
    assert red_dark_red == expected


def test__italic_bold_italic():
    """I    B       /F/B
       3    1   →   22"""
    bolditalic = colored('BoldAndItalic', 'bold')
    italic_bold_italic = colored('Italic' + bolditalic + 'Italic', 'italic')
    util.spacyprint(f'italic_bold_italic:', italic_bold_italic)
    expected = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[22mItalic\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert italic_bold_italic == expected


def test__italic_red_italic():
    """I    R       /FG
       3    31  →   39"""
    italic_red_italic = colored('Italic' + colored('RedItalic', 'red') + 'Italic', 'italic')
    util.spacyprint(f'italic_red_italic:', italic_red_italic)
    expected = '\x1b[3mItalic\x1b[31mRedItalic\x1b[39mItalic\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert italic_red_italic == expected


def test__red_green_red():
    """R    G       R
       31   32  →   31"""
    
    green = colored('Green', 'green')
    red_green_red = colored('Red' + green + 'Red', 'red')
    util.spacyprint(f'red_green_red:', red_green_red)
    # doesn't reset green, just re-opens red (because incompatible)
    expected = '\x1b[31mRed\x1b[32mGreen\x1b[31mRed\x1b[0m'
    util.spacyprint('expected:', expected)
    assert red_green_red == expected


def test__italic_satgreen_italic():
    """I    SG      /FG
       3    92  →   39"""
    italic_satgreen_italic = colored('Italic' + colored('SatGreenItalic', 'sat green') + 'Italic', 'italic')
    util.spacyprint(f'italic_satgreen_italic:', italic_satgreen_italic)
    expected = '\x1b[3mItalic\x1b[92mSatGreenItalic\x1b[39mItalic\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert italic_satgreen_italic == expected


def test__bold_italic_bold():
    """B    I       /I
       1    3   →   23"""
    bold_italic_bold = colored('Bold' + colored('ItalicAndBold', 'italic') + 'Bold', 'bold')
    util.spacyprint(f'bold_italic_bold:', bold_italic_bold)
    expected = '\x1b[1mBold\x1b[3mItalicAndBold\x1b[23mBold\x1b[0m'
    util.spacyprint('expected:', expected)
    # smart reset italic (23), no reopen bold
    assert bold_italic_bold == expected


def test__satwhite_dark_satwhite():
    """S    F       /F
       97   2   →   22"""
    satwhite_dark_satwhite = colored('Sat' + colored('DarkAndSat', 'dark') + 'Sat', 'sat white')
    util.spacyprint(f'satwhite_dark_satwhite:', satwhite_dark_satwhite)
    expected = '\x1b[97mSat\x1b[2mDarkAndSat\x1b[22mSat\x1b[0m'
    # smart reset dark, no re-open sat
    util.spacyprint('expected:', expected)
    assert satwhite_dark_satwhite == expected


def test__satwhite_red_satwhite():
    """S    R       S
       97   31  →   97"""
    satwhite_red_satwhite = colored('Sat' + colored('Red', 'red') + 'Sat', 'sat white')
    util.spacyprint(f'satwhite_red_satwhite:', satwhite_red_satwhite)
    expected = '\x1b[97mSat\x1b[31mRed\x1b[97mSat\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert satwhite_red_satwhite == expected


def test__red_blackbg_red():
    onblack = colored('OnBlack', 'on black')
    red_onblack_red = colored('Red' + onblack + 'Red', 'red')
    util.spacyprint('red_onblack_red:',
                    red_onblack_red,
                    repr(red_onblack_red))
    expected = '\x1b[31mRed\x1b[40mOnBlack\x1b[49mRed\x1b[0m'
    util.spacyprint(f'expected:', expected, repr(expected))
    
    assert red_onblack_red == expected


def test__satred_blackbg_satred():
    blackbg = colored('OnBlack', 'on black')
    satred = colored('SatRed' + blackbg + 'SatRed', 'on red')
    util.spacyprint('satred:',
                    satred,
                    repr(satred))
    expected = '\x1b[41mSatRed\x1b[40mOnBlack\x1b[49mSatRed\x1b[0m'
    util.spacyprint(f'expected:', expected, repr(expected))
    
    assert satred == expected


######################
## Same reset codes ##
######################


def test__bold_dark_bold():
    """B    F       /F/B B
       1    2   →   22;1"""
    bold_dark_bold = colored('Bold' + colored('DarkAndBold', 'dark') + 'Bold', 'bold')
    util.spacyprint(f'bold_dark_bold:', bold_dark_bold)
    expected0 = '\x1b[1mBold\x1b[2mDarkAndBold\x1b[22;1mBold\x1b[0m'
    expected1 = '\x1b[1mBold\x1b[2mDarkAndBold\x1b[0;1mBold\x1b[0m'
    util.spacyprint(f'expected0:', expected0)
    util.spacyprint(f'expected1:', expected1)
    # both options ok
    assert bold_dark_bold in (expected0, expected1)


def test__dark_bold_dark():
    dark_bold_dark = colored(' Dark ' + colored(' DarkAndBold ', 'bold') + ' Dark ', 'dark')
    util.spacyprint(f'dark_bold_dark:', dark_bold_dark)
    expected = '\x1b[2m Dark \x1b[1m DarkAndBold \x1b[22;2m Dark \x1b[0m'
    util.spacyprint(f'expected:', expected)
    # both options ok
    assert dark_bold_dark == expected


def test__bold_satwhite__dark__bold_satwhite():
    """S+B  F       /F/B B
       1;97 2   →   22;1"""
    bolddark = colored(' BoldDark ', 'dark')
    bold_satwhite__dark__bold_satwhite = colored(' BoldSat ' + bolddark + ' BoldSat ', 'bold', 'sat white')
    util.spacyprint('bold_satwhite__dark__bold_satwhite:',
                    bold_satwhite__dark__bold_satwhite,
                    repr(bold_satwhite__dark__bold_satwhite))
    # merge dark reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize sat is not lost and is restored automatically by 22
    expected = '\x1b[1;97m BoldSat \x1b[2m BoldDark \x1b[22;1m BoldSat \x1b[0m'
    util.spacyprint(f'expected:', expected, repr(expected))
    
    try:
        assert bold_satwhite__dark__bold_satwhite == expected
    except AssertionError as e:
        assert bold_satwhite__dark__bold_satwhite == '\x1b[1;97m BoldSat \x1b[2m BoldDark \x1b[22;1;97m BoldSat \x1b[0m'


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
