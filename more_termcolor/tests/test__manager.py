"""This module does not assert anything programmatically. It just prints and describes what you're supposed to see with your eyes."""
from more_termcolor import COLOR_CODES
from more_termcolor.paint import paint
from more_itertools import random_combination


def _print(color, code):
    print(f'\n{color} ({code})',
          f'\033[{code}m{color}\033[0m',
          sep='\n', end='\n')


def title(text):
    return paint(f'\n{text}', 'bold', 'sat white', 'ul')


foreground_color_codes = {k: v for k, v in COLOR_CODES.items() if not isinstance(v, dict)}  # skip 'bg', 'sat'
saturated_color_codes = {k: v for k, v in COLOR_CODES['sat'].items() if not isinstance(v, dict)}
background_color_codes = COLOR_CODES['bg']
background_colors = list(background_color_codes.keys())
foreground_colors = list(foreground_color_codes.keys())


def test__foreground_color_codes__sanity():
    print(title('foreground colors: sanity'))
    for color, code in foreground_color_codes.items():
        _print(color, code)


def test__background_color_codes__sanity():
    print(title('background colors: sanity'))
    for color, code in background_color_codes.items():
        _print(color, code)


def test__saturated_color_codes__sanity():
    print(title('saturated colors: sanity'))
    for color, code in saturated_color_codes.items():
        _print(color, code)


def test__mixed_foreground_background():
    print(title('mixed foreground and background'))
    
    pairs = list(zip(random_combination(foreground_colors, 15), random_combination(background_colors + background_colors, 15)))
    while any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(random_combination(foreground_colors, 15), random_combination(background_colors + background_colors, 15)))
    
    for fg, bg in pairs:
        fg_code = foreground_color_codes[fg]
        bg_code = background_color_codes[bg]
        
        _print(f"{fg} on {bg}", f"{fg_code};{bg_code}")
