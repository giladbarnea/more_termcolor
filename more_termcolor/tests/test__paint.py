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

from more_termcolor.paint import paint
from more_termcolor import util


def test__nested_incompat_colors():
    """R    G       R
       31   32  →   31"""
    from more_termcolor import settings
    settings.debug = True
    green = paint('Green', 'green')
    red_green_red = paint('Red' + green + 'Red', 'red')
    util.spacyprint(f'red_green_red:', red_green_red)
    # doesn't reset green, just re-opens red (because incompatible)
    expected = '\x1b[31mRed\x1b[32mGreen\x1b[31mRed\x1b[0m'
    util.spacyprint('expected:', expected)
    assert red_green_red == expected


def test__nested_compat_colors():
    """R    F       /F/B
       31   2   →   22"""
    red_faint_red = paint('Red' + paint('FaintAndRed', 'faint') + 'Red', 'red')
    util.spacyprint(f'red_faint_red:', red_faint_red)
    expected = '\x1b[31mRed\x1b[2mFaintAndRed\x1b[22mRed\x1b[0m'
    util.spacyprint('expected:', expected)
    # smart reset faint in the middle, and does not re-open red
    assert red_faint_red == expected


def test__nested_compat_colors__adv_0():
    """I    B       /F/B
       3    1   →   22"""
    italic_bold_italic = paint('Italic' + paint('BoldAndItalic', 'bold') + 'Italic', 'italic')
    util.spacyprint(f'italic_bold_italic:', italic_bold_italic)
    expected = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[22;3mItalic\x1b[0m'
    
    util.spacyprint(f'expected:', expected)
    assert italic_bold_italic == expected


def test__nested_compat_colors__adv_1():
    """I    R       /FG
       3    31  →   39"""
    italic_red_italic = paint('Italic' + paint('RedItalic', 'red') + 'Italic', 'italic')
    util.spacyprint(f'italic_red_italic:', italic_red_italic)
    expected = '\x1b[3mItalic\x1b[31mRedItalic\x1b[39mItalic\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert italic_red_italic == expected


def test__nested_compat_colors__adv_1_b():
    """I    SG      /FG
       3    92  →   39"""
    italic_satgreen_italic = paint('Italic' + paint('SatGreenItalic', 'sat green') + 'Italic', 'italic')
    util.spacyprint(f'italic_satgreen_italic:', italic_satgreen_italic)
    expected = '\x1b[3mItalic\x1b[92mSatGreenItalic\x1b[39mItalic\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert italic_satgreen_italic == expected


def test__nested_compat_colors__adv_2():
    """B    I       /I
       1    3   →   23"""
    bold_italic_bold = paint('Bold' + paint('ItalicAndBold', 'italic') + 'Bold', 'bold')
    util.spacyprint(f'bold_italic_bold:', bold_italic_bold)
    expected = '\x1b[1mBold\x1b[3mItalicAndBold\x1b[23mBold\x1b[0m'
    util.spacyprint('expected:', expected)
    # smart reset italic (23), no reopen bold
    assert bold_italic_bold == expected


def test__nested_compat_colors__adv_3():
    """B    F       /F/B B
       1    2   →   22;1"""
    bold_faint_bold = paint('Bold' + paint('FaintAndBold', 'faint') + 'Bold', 'bold')
    util.spacyprint(f'bold_faint_bold:', bold_faint_bold)
    expected0 = '\x1b[1mBold\x1b[2mFaintAndBold\x1b[22;1mBold\x1b[0m'
    expected1 = '\x1b[1mBold\x1b[2mFaintAndBold\x1b[0;1mBold\x1b[0m'
    util.spacyprint(f'expected0:', expected0)
    util.spacyprint(f'expected1:', expected1)
    # both options ok
    assert bold_faint_bold in (expected0, expected1)


def test__nested_compat_colors__adv_4():
    """S    F       /F
       97   2   →   22"""
    sat_faint_sat = paint('Sat' + paint('FaintAndSat', 'faint') + 'Sat', 'sat white')
    util.spacyprint(f'sat_faint_sat:', sat_faint_sat)
    expected = '\x1b[97mSat\x1b[2mFaintAndSat\x1b[22mSat\x1b[0m'
    # smart reset faint, no re-open sat
    util.spacyprint('expected:', expected)
    assert sat_faint_sat == expected


def test__nested_compat_colors__adv_5():
    """S    R       S
       97   31  →   97"""
    sat_red_sat = paint('Sat' + paint('Red', 'red') + 'Sat', 'sat white')
    util.spacyprint(f'sat_red_sat:', sat_red_sat)
    expected = '\x1b[97mSat\x1b[31mRed\x1b[97mSat\x1b[0m'
    util.spacyprint(f'expected:', expected)
    assert sat_red_sat == expected


# @pytest.mark.skip
def test__nested_colors__compat_and_incompat():
    """S+B  F       /F/B B
       1;97 2   →   22;1"""
    bold_satwhite__faint__bold_satwhite = paint('BoldSat' + paint('BoldFaint', 'faint') + 'BoldSat', 'bold', 'sat white')
    util.spacyprint('bold_satwhite__faint__bold_satwhite:', bold_satwhite__faint__bold_satwhite)
    # merge faint reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize sat is not lost and is restored automatically by 22
    expected = '\x1b[1;97mBoldSat\x1b[2mBoldFaint\x1b[22;1mBoldSat\x1b[0m'
    util.spacyprint(f'expected:', expected)
    
    assert bold_satwhite__faint__bold_satwhite == expected
