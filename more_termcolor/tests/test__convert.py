from more_termcolor import convert, core
from more_termcolor.tests import common
import re
from itertools import permutations


def test__to_code__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.FOREGROUND_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.BRIGHT_FOREGROUND_COLOR_CODES.items():
        assert convert.to_code(f'bright {color}') == code
    
    for color, code in core.BACKGROUND_COLOR_CODES.items():
        assert convert.to_code(f'on {color}') == code
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == code
    
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        assert convert.to_code(f'on bright {color}') == code


def test__to_code__from_code():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.FOREGROUND_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.BRIGHT_FOREGROUND_COLOR_CODES.items():
        assert convert.to_code(f'bright {color}') == convert.to_code(code)
    
    for color, code in core.STANDARD_BACKGROUND_COLOR_CODES.items():
        assert convert.to_code(f'on {color}') == convert.to_code(code)
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == convert.to_code(code)
    
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        assert convert.to_code(f'on bright {color}') == convert.to_code(code)


def test__to_code__edge_cases():
    with common.assert_raises(KeyError, 'grin'):
        convert.to_code('grin')
    with common.assert_raises(KeyError, 'brightblue'):
        convert.to_code('brightblue')
    with common.assert_raises(KeyError, 'brightblue'):
        convert.to_code('on brightblue')


def test__to_code__docstring_examples():
    assert convert.to_code('green') == '32'
    assert convert.to_code('on red') == '41'
    assert convert.to_code('on bright yellow') == '103'
    assert convert.to_code(32) == '32' == convert.to_code('32')


@common.print_and_compare
def test__to_color__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        actual = convert.to_color(code)
        try:
            yield actual, color
        except AssertionError as e:
            print()
            # aliases
            if (actual, color) not in (
                    ('ita', 'italic'),
                    ('ul', 'underline'),
                    ('conceal', 'concealed'),
                    ('ol', 'overline'),
                    ):
                raise
    
    for color, code in core.FOREGROUND_COLOR_CODES.items():
        actual = convert.to_color(code)
        try:
            yield actual, color
        except AssertionError as e:
            if (actual, color) != ('black', 'grey'):
                raise
    
    for color, code in core.BRIGHT_FOREGROUND_COLOR_CODES.items():
        actual = convert.to_color(code)
        expected = f'bright {color}'
        try:
            yield actual, expected
        except AssertionError as e:
            if (actual, expected) != ('bright black', 'bright grey'):
                raise
    
    for color, code in core.STANDARD_BACKGROUND_COLOR_CODES.items():
        actual = convert.to_color(code)
        expected = f'on {color}'
        try:
            yield actual, expected
        except AssertionError as e:
            if (actual, expected) != ('on black', 'on grey'):
                raise
    
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        actual = convert.to_color(code)
        expected = f'on bright {color}'
        try:
            yield actual, expected
        except AssertionError as e:
            if (actual, expected) != ('on bright black', 'on bright grey'):
                raise
    
    for color, code in core.RESET_COLOR_CODES.items():
        actual = convert.to_color(code)
        expected = f'reset {color}'
        try:
            yield actual, expected
        except AssertionError as e:
            # same reset codes, different colors (or aliases)
            if (actual, expected) not in ((f'reset {pair[0]}', f'reset {pair[1]}') for pair in (
                    ('bold', 'dark'),
                    ('ita', 'italic'),
                    ('ul', 'underline'),
                    ('ul', 'doubleul'),
                    ('blink', 'fastblink'),
                    ('conceal', 'concealed'),
                    ('frame', 'circle'),
                    ('ol', 'overline'),
                    )):
                raise


def test__to_color__docstring_examples():
    assert convert.to_color(32) == 'green' == convert.to_color('32')
    assert convert.to_color(41) == 'on red' == convert.to_color('41')
    assert convert.to_color(103) == 'on bright yellow' == convert.to_color('103')
    assert convert.to_color('green') == 'green'


@common.print_and_compare
def test__to_code__fonts():
    actual = convert.to_code('10')
    expected = '10'
    return actual, expected


def test__to_reset_code():
    assert convert.to_reset_code('bold') == '22'
    assert convert.to_reset_code('dark') == '22'
    assert convert.to_reset_code(22) == '22' == convert.to_reset_code('22')
    assert convert.to_reset_code('green') == '39' == core.RESET_COLOR_CODES['fg']
    assert convert.to_reset_code('on red') == '49'
    assert convert.to_reset_code('bright red') == '39'
    assert convert.to_reset_code('on bright yellow') == '49'
    assert convert.to_reset_code('on') == '49'
    for bad in ('BAD', 'on BAD', 'on bright BAD'):
        with common.assert_raises(KeyError, f"to_reset_code('{bad}'): color '{bad}' isn't recognized"):
            convert.to_reset_code(bad)
    
    with common.assert_raises(KeyError, 'bright'):
        convert.to_reset_code('bright')


@common.print_and_compare
def test__to_boundary():
    for code in (1, '1', 'bold'):
        actual = convert.to_boundary(code)
        expected = '\x1b[1m'
        yield actual, expected
    
    actual = convert.to_boundary(1, '2', 'on bright black')
    expected = re.compile(common.codes_perm(1, 2, 100))
    yield actual, expected
