from more_termcolor import convert, core
from more_termcolor.tests import common


def test__to_code__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_code(f'sat {color}') == code
    
    for color, code in core.BG_COLOR_CODES.items():
        assert convert.to_code(f'on {color}') == code
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == code
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_code(f'on sat {color}') == code


def test__to_code__from_code():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_code(f'sat {color}') == convert.to_code(code)
    
    for color, code in core.STD_BG_COLOR_CODES.items():
        assert convert.to_code(f'on {color}') == convert.to_code(code)
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == convert.to_code(code)
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_code(f'on sat {color}') == convert.to_code(code)


def test__to_code__edge_cases():
    with common.assert_raises(KeyError):
        convert.to_code('grin')
        convert.to_code('satblue')
        convert.to_code('on sat blue')


def test__to_color__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_color(code) == color
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_color(code) == color
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_color(code) == f'sat {color}'
    
    for color, code in core.STD_BG_COLOR_CODES.items():
        assert convert.to_color(code) == f'on {color}'
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_color(code) == f'on sat {color}'
    
    for color, code in core.RESET_COLOR_CODES.items():
        try:
            assert convert.to_color(code) == f'reset {color}'
        except AssertionError as e:
            if code not in (22, 24, 25, 54):
                # reset codes for multiple colors
                raise
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_color(code) == f'on sat {color}'


def test__to_reset_code():
    assert convert.to_reset_code('bold') == 22
    assert convert.to_reset_code('dark') == 22
    assert convert.to_reset_code('green') == 39 == core.RESET_COLOR_CODES['fg']
    assert convert.to_reset_code(22) == 22
    assert convert.to_reset_code('on red') == 49
    assert convert.to_reset_code('sat red') == 39
    with common.assert_raises(KeyError, convert.BACKGROUND_RE.pattern, r"`actual_color` ('BAD') not in BG_COLOR_CODES"):
        convert.to_reset_code('on BAD')
        convert.to_reset_code('on satBAD')
    assert convert.to_reset_code('on satyellow') == 49
    with common.assert_raises(KeyError, 'BAD'):
        convert.to_reset_code('BAD')
    with common.assert_raises(KeyError, 'sat'):
        convert.to_reset_code('sat')
    with common.assert_raises(KeyError, 'bg'):
        convert.to_reset_code('bg')


def test___try_get_sat_reset_code():
    assert convert._try_get_sat_reset_code('green') is None
    
    # provides safety only for 'sat ...' (unlike to_reset_code())
    assert convert._try_get_sat_reset_code('BAD') is None
    
    assert convert._try_get_sat_reset_code('sat green') == 39
    with common.assert_raises(KeyError, convert.SATURATED_RE.pattern, "`actual_color` ('on red')", "SAT_FG_COLOR_CODES"):
        convert._try_get_sat_reset_code('on satred')
    with common.assert_raises(KeyError, convert.SATURATED_RE.pattern, "`actual_color` ('red')", "SAT_FG_COLOR_CODES"):
        convert._try_get_sat_reset_code('on red')


def test___try_get_bg_reset_code():
    assert convert._try_get_bg_reset_code('green') is None
    
    # provides safety only for 'on ...' (unlike to_reset_code())
    assert convert._try_get_bg_reset_code('BAD') is None
    with common.assert_raises(KeyError, convert.BACKGROUND_RE.pattern, r"`actual_color` ('BAD') not in BG_COLOR_CODES"):
        convert._try_get_bg_reset_code('on BAD')
    
    assert convert._try_get_bg_reset_code('sat green') is None
    assert convert._try_get_bg_reset_code('on satred') == 49
    assert convert._try_get_bg_reset_code('on red') == 49


def test__reset():
    no_reset = ('default', 'fraktur')
    for color, code in core.FORMATTING_COLOR_CODES.items():
        if color in no_reset:
            continue
        with common.assert_doesnt_raise(KeyError):
            convert.reset(color)
