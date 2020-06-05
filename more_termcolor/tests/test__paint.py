import pytest

from more_termcolor import paint

faint = paint('faint', 'faint')


def _print(*values):
    print('\n', *values, sep='\n', end='\n')


def test__nested_incompat_colors():
    red_green_red = paint('Red' + paint('Green', 'green') + 'Red', 'red')
    _print(f'red_green_red:', red_green_red)
    expected = '\x1b[31mRed\x1b[32mGreen\x1b[31mRed\x1b[0m'
    # doesn't reset green, just re-opens red (because incompatible)
    # TODO: decide: easier impl and same visual result if green is reset
    #  in that case, expected is:
    #  '\x1b[31mRed\x1b[0m\x1b[32mGreen\x1b[0m\x1b[31mRed\x1b[0m'
    _print('expected:', expected)
    assert red_green_red == expected


def test__nested_compat_colors():
    red_faint_red = paint('Red' + paint('FaintAndRed', 'faint') + 'Red', 'red')
    _print(f'red_faint_red:', red_faint_red)
    expected = '\x1b[31mRed\x1b[2mFaintAndRed\x1b[22mRed\x1b[0m'
    _print('expected:', expected)
    # smart reset faint in the middle, and does not re-open red
    assert red_faint_red == expected


def test__nested_compat_colors__adv_0():
    italic_bold_italic = paint('Italic' + paint('BoldAndItalic', 'bold') + 'Italic', 'italic')
    _print(f'italic_bold_italic:', italic_bold_italic)
    expected0 = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[22;3mItalic\x1b[0m'
    expected1 = '\x1b[3mItalic\x1b[1mBoldAndItalic\x1b[0;3mItalic\x1b[0m'
    _print(f'expected0:', expected0)
    _print(f'expected1:', expected1)
    # both options ok
    assert italic_bold_italic in (expected0, expected1)


def test__nested_compat_colors__adv_1():
    bold_italic_bold = paint('Bold' + paint('ItalicAndBold', 'italic') + 'Bold', 'bold')
    _print(f'bold_italic_bold:', bold_italic_bold)
    expected = '\x1b[1mBold\x1b[3mItalicAndBold\x1b[23mBold\x1b[0m'
    _print('expected:', expected)
    # smart reset italic (23), no reopen bold
    assert bold_italic_bold == expected


def test__nested_compat_colors__adv_2():
    bold_faint_bold = paint('Bold' + paint('FaintAndBold', 'faint') + 'Bold', 'bold')
    _print(f'bold_faint_bold:', bold_faint_bold)
    expected0 = '\x1b[1mBold\x1b[2mFaintAndBold\x1b[22;1mBold\x1b[0m'
    expected1 = '\x1b[1mBold\x1b[2mFaintAndBold\x1b[0;1mBold\x1b[0m'
    _print(f'expected0:', expected0)
    _print(f'expected1:', expected1)
    # both options ok
    assert bold_faint_bold in (expected0, expected1)


def test__nested_compat_colors__adv_3():
    sat_faint_sat = paint('Sat' + paint('FaintAndSat', 'faint') + 'Sat', 'sat white')
    _print(f'sat_faint_sat:', sat_faint_sat)
    expected = '\x1b[97mSat\x1b[2mFaintAndSat\x1b[22mSat\x1b[0m'
    # smart reset faint, no re-open sat
    _print('expected:', expected)
    assert sat_faint_sat == expected


def test__nested_compat_colors__adv_4():
    sat_red_sat = paint('Sat' + paint('RedAndSat', 'red') + 'Sat', 'sat white')
    _print(f'sat_red_sat:', sat_red_sat)
    expected0 = '\x1b[97mSat\x1b[31mRedAndSat\x1b[37mSat\x1b[0m'  # reset red via 'white' (37)
    expected1 = '\x1b[97mSat\x1b[31mRedAndSat\x1b[97mSat\x1b[0m'  # re-assert sat via 97
    _print(f'expected0:', expected0)
    _print(f'expected1:', expected1)
    # either reset red with white,
    assert sat_red_sat in (expected0, expected1)


# @pytest.mark.skip
def test__nested_colors__compat_and_incompat():
    bold_satwhite__faint__bold_satwhite = paint('BoldSat' + paint('BoldFaint', 'faint') + 'BoldSat', 'bold', 'sat white')
    _print('bold_satwhite__faint__bold_satwhite:', bold_satwhite__faint__bold_satwhite)
    # merge faint reset with bold re-open (22;1)
    # recognize bold is lost by 22, so need to re-open it
    # recognize sat is not lost and is restored automatically by 22
    expected = '\x1b[1;97mBoldSat\x1b[2mBoldFaint\x1b[22;1mBoldSat\x1b[0m'
    _print(f'expected:', expected)
    
    assert bold_satwhite__faint__bold_satwhite == expected
