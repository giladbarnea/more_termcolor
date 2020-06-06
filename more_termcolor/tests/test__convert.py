from more_termcolor import convert, core
from more_termcolor.tests import common


# flat_color_codes = common.flatten_dict(core.COLOR_CODES)


def test__to_code__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_code(color) == code
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_code(f'sat {color}') == code
    
    for color, code in core.BG_COLOR_CODES.items():
        assert convert.to_code(f'bg {color}') == code
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == code
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_code(f'sat bg {color}') == code


def test__to_code__from_code():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_code(color) == convert.to_code(code)
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_code(f'sat {color}') == convert.to_code(code)
    
    for color, code in core.BG_COLOR_CODES.items():
        assert convert.to_code(f'bg {color}') == convert.to_code(code)
    
    for color, code in core.RESET_COLOR_CODES.items():
        assert convert.to_code(f'reset {color}') == convert.to_code(code)
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_code(f'sat bg {color}') == convert.to_code(code)


def test__to_code__edge_cases():
    with common.assert_raises(KeyError):
        convert.to_code('grin')
        convert.to_code('satblue')
        convert.to_code('bg sat blue')


def test__to_color__sanity():
    for color, code in core.FORMATTING_COLOR_CODES.items():
        assert convert.to_color(code) == color
    
    for color, code in core.FG_COLOR_CODES.items():
        assert convert.to_color(code) == color
    
    for color, code in core.SAT_FG_COLOR_CODES.items():
        assert convert.to_color(code) == f'sat {color}'
    
    for color, code in core.BG_COLOR_CODES.items():
        assert convert.to_color(code) == f'bg {color}'
    
    for color, code in core.RESET_COLOR_CODES.items():
        try:
            assert convert.to_color(code) == f'reset {color}'
        except AssertionError as e:
            if code not in (22, 24, 25, 54):
                # reset codes for multiple colors
                raise
    
    for color, code in core.SAT_BG_COLOR_CODES.items():
        assert convert.to_color(code) == f'sat bg {color}'


def test__reset():
    no_reset = ('default', 'fraktur')
    for color, code in core.FORMATTING_COLOR_CODES.items():
        if color in no_reset:
            continue
        with common.assert_doesnt_raise(KeyError):
            convert.reset(color)
