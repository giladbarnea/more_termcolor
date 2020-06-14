from more_termcolor import convert, core
from more_termcolor.tests import common


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
    with common.assert_raises(KeyError):
        convert.to_code('grin')
    with common.assert_raises(KeyError):
        convert.to_code('brightblue')
    with common.assert_raises(KeyError):
        convert.to_code('on bright blue')


def test__to_code__docstring_examples():
    assert convert.to_code('green') == '32'
    assert convert.to_code('on red') == '41'
    assert convert.to_code('on bright yellow') == '103'
    assert convert.to_code(32) == '32' == convert.to_code('32')


def test__to_color__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        actual = convert.to_color(code)
        try:
            assert actual == color
        except AssertionError as e:
            # aliases
            if (actual, color) not in (
                    ('ul', 'underline'),
                    ('conceal', 'concealed'),
                    ('ol', 'overline'),
                    ):
                raise
    
    for color, code in core.FOREGROUND_COLOR_CODES.items():
        assert convert.to_color(code) == color
    
    for color, code in core.BRIGHT_FOREGROUND_COLOR_CODES.items():
        assert convert.to_color(code) == f'bright {color}'
    
    for color, code in core.STANDARD_BACKGROUND_COLOR_CODES.items():
        assert convert.to_color(code) == f'on {color}'
    
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        assert convert.to_color(code) == f'on bright {color}'
    
    for color, code in core.RESET_COLOR_CODES.items():
        actual = convert.to_color(code)
        expected = f'reset {color}'
        try:
            assert actual == expected
        except AssertionError as e:
            # same reset codes, different colors (or aliases)
            if (actual, expected) not in ((f'reset {pair[0]}', f'reset {pair[1]}') for pair in (
                    ('bold', 'dark'),
                    ('ul', 'underline'),
                    ('ul', 'doubleul'),
                    ('blink', 'fastblink'),
                    ('conceal', 'concealed'),
                    ('frame', 'circle'),
                    ('ol', 'overline'),
                    )):
                raise
    
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        assert convert.to_color(code) == f'on bright {color}'


def test__to_color__docstring_examples():
    assert convert.to_color(32) == 'green' == convert.to_color('32')
    assert convert.to_color(41) == 'on red' == convert.to_color('41')
    assert convert.to_color(103) == 'on bright yellow' == convert.to_color('103')
    assert convert.to_color('green') == 'green'


def test__to_reset_code():
    assert convert.to_reset_code('bold') == '22'
    assert convert.to_reset_code('dark') == '22'
    assert convert.to_reset_code(22) == '22' == convert.to_reset_code('22')
    assert convert.to_reset_code('green') == '39' == core.RESET_COLOR_CODES['fg']
    assert convert.to_reset_code('on red') == '49'
    assert convert.to_reset_code('bright red') == '39'
    with common.assert_raises(KeyError, convert.BACKGROUND_RE.pattern, r"`actual_color` ('BAD') not in STANDARD_BACKGROUND_COLOR_CODES"):
        convert.to_reset_code('on BAD')
    with common.assert_raises(KeyError, convert.BACKGROUND_RE.pattern, r"`actual_color` ('BAD') not in STANDARD_BACKGROUND_COLOR_CODES"):
        convert.to_reset_code('on bright BAD')
    assert convert.to_reset_code('on bright yellow') == '49'
    with common.assert_raises(KeyError, 'BAD'):
        convert.to_reset_code('BAD')
    with common.assert_raises(KeyError, 'bright'):
        convert.to_reset_code('bright')
    with common.assert_raises(KeyError, 'on'):
        convert.to_reset_code('on')


# def test___try_get_bright_reset_code():
#     assert convert._try_get_bright_reset_code('green') is None
#
#     # provides safety only for 'bright ...' (unlike to_reset_code())
#     assert convert._try_get_bright_reset_code('BAD') is None
#
#     assert convert._try_get_bright_reset_code('bright green') == 39
#     with common.assert_raises(KeyError, convert.BRIGHT_RE.pattern, "`actual_color` ('on red')", "BRIGHT_FOREGROUND_COLOR_CODES"):
#         convert._try_get_bright_reset_code('on bright red')
#     with common.assert_raises(KeyError, convert.BRIGHT_RE.pattern, "`actual_color` ('red')", "BRIGHT_FOREGROUND_COLOR_CODES"):
#         convert._try_get_bright_reset_code('on red')


# def test___try_get_bg_reset_code():
#     assert convert._try_get_bg_reset_code('green') is None
#
#     # provides safety only for 'on ...' (unlike to_reset_code())
#     assert convert._try_get_bg_reset_code('BAD') is None
#     with common.assert_raises(KeyError, convert.BACKGROUND_RE.pattern, r"`actual_color` ('BAD') not in STANDARD_BACKGROUND_COLOR_CODES"):
#         convert._try_get_bg_reset_code('on BAD')
#
#     assert convert._try_get_bg_reset_code('bright green') is None
#     assert convert._try_get_bg_reset_code('on bright red') == 101
#     assert convert._try_get_bg_reset_code('on red') == 49


def test__reset():
    no_reset = ('default', 'fraktur')
    for color, code in core.FORMATTING_COLOR_CODES.items():
        if color in no_reset:
            continue
        with common.assert_doesnt_raise(KeyError):
            convert.reset(color)
