"""This module does not assert anything programmatically. It just prints and describes what you're supposed to see with your eyes."""
from more_termcolor import COLOR_CODES
from more_termcolor.paint import paint
from random import choices

from more_termcolor.tests import common


def _print(color, code):
    print(f'\n{color} ({code})',
          f'\033[{code}m{color}\033[0m',
          sep='\n', end='\n')


def title(text):
    return paint(f'\n{text}', 'bold', 'sat white', 'ul')


foreground_color_codes = {k: v for k, v in COLOR_CODES.items() if not isinstance(v, dict)}  # skip 'bg', 'sat'
saturated_color_codes = {k: v for k, v in COLOR_CODES['sat'].items() if not isinstance(v, dict)}
saturated_background_color_codes = {k: v for k, v in COLOR_CODES['sat']['bg'].items()}
background_color_codes = COLOR_CODES['bg']
background_colors = list(background_color_codes.keys())
foreground_colors = list(foreground_color_codes.keys())
saturated_colors = list(saturated_color_codes.keys())
saturated_background_colors = list(saturated_background_color_codes.keys())


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


def test__std_foreground_on_std_background():
    print(title('standard foreground on standard background'))
    
    pairs = list(zip(choices(foreground_colors, k=15), choices(background_colors, k=15)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(foreground_colors, k=15), choices(background_colors, k=15)))
    
    for fg, bg in pairs:
        fg_code = foreground_color_codes[fg]
        bg_code = background_color_codes[bg]
        
        _print(f"{fg} on {bg}", f"{fg_code};{bg_code}")


def test__saturated_foreground_on_std_background():
    print(title('saturated foreground on standard background'))
    
    pairs = list(zip(choices(saturated_colors, k=15), choices(background_colors, k=15)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(saturated_colors, k=15), choices(background_colors, k=15)))
    for sat_fg, bg in pairs:
        sat_fg_code = saturated_color_codes[sat_fg]
        bg_code = background_color_codes[bg]
        
        _print(f"saturated {sat_fg} on {bg}", f"{sat_fg_code};{bg_code}")


def test__std_foreground_on_saturated_background():
    print(title('standard foreground on saturated background'))
    
    pairs = list(zip(choices(foreground_colors, k=15), choices(saturated_background_colors, k=15)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(foreground_colors, k=15), choices(saturated_background_colors, k=15)))
    for fg, sat_bg in pairs:
        fg_code = foreground_color_codes[fg]
        sat_bg_code = saturated_background_color_codes[sat_bg]
        
        _print(f"{fg} on saturated {sat_bg}", f"{fg_code};{sat_bg_code}")


def test__saturated_foreground_on_saturated_background():
    print(title('saturated foreground on saturated background'))
    
    pairs = list(zip(choices(saturated_colors, k=15), choices(saturated_background_colors, k=15)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(saturated_colors, k=15), choices(saturated_background_colors, k=15)))
    for sat_fg, sat_bg in pairs:
        sat_fg_code = saturated_color_codes[sat_fg]
        sat_bg_code = saturated_background_color_codes[sat_bg]
        
        _print(f"saturated {sat_fg} on saturated {sat_bg}", f"{sat_fg_code};{sat_bg_code}")
