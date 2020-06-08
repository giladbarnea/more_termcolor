"""This module does not really assert anything programmatically. It just prints and describes what you're supposed to see with your eyes.
Optionally pass '--confirm' to prompt before starting each test, e.g.:
pytest -sxl more_termcolor/tests/test__core.py --confirm"""

from more_termcolor import core, util
from more_termcolor.paint import paint, COLOR_CODES_RE
from random import choices
from more_termcolor.tests import common
from more_termcolor.util import spacyprint
import re

K = 20


def _print(color, code):
    # assert isinstance(color, str)
    assert (isinstance(code, int) or (isinstance(code, str) and re.search(COLOR_CODES_RE, code)))
    spacyprint(f'{color} ({code})',
               f'\033[{code}m{color}\033[0m')


def title(text):
    return paint(f'\n{text}\n', 'bold', 'sat white', 'ul')


def test__formatting_color_codes__sanity(confirm):
    print(title(f'formatting colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.FORMATTING_COLOR_CODES.items():
        _print(color, code)


def test__fg_color_codes__sanity(confirm):
    print(title(f'foreground colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.FG_COLOR_CODES.items():
        _print(color, code)


def test__bg_color_codes__sanity(confirm):
    print(title('background colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.BG_COLOR_CODES.items():
        _print(color, code)


def test__saturated_fg_color_codes__sanity(confirm):
    print(title('saturated fg colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.SAT_FG_COLOR_CODES.items():
        _print(color, code)


def test__std_foreground_on_std_background(confirm):
    print(title('standard foreground on standard background'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.background_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.background_colors, k=K)))
    
    for fg, bg in pairs:
        fg_code = core.FG_COLOR_CODES[fg]
        bg_code = core.BG_COLOR_CODES[bg]
        
        _print(f"{fg} on {bg}", f"{fg_code};{bg_code}")


def test__saturated_foreground_on_std_background(confirm):
    print(title('saturated foreground on standard background'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.saturated_fg_colors, k=K), choices(common.background_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.saturated_fg_colors, k=K), choices(common.background_colors, k=K)))
    for sat_fg, bg in pairs:
        sat_fg_code = core.SAT_COLOR_CODES[sat_fg]
        bg_code = core.BG_COLOR_CODES[bg]
        
        _print(f"saturated {sat_fg} on {bg}", f"{sat_fg_code};{bg_code}")


def test__std_foreground_on_saturated_background(confirm):
    print(title('standard foreground on saturated background'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.saturated_bg_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.saturated_bg_colors, k=K)))
    for fg, sat_bg in pairs:
        fg_code = core.FG_COLOR_CODES[fg]
        sat_bg_code = core.SAT_BG_COLOR_CODES[sat_bg]
        
        _print(f"{fg} on saturated {sat_bg}", f"{fg_code};{sat_bg_code}")


def test__saturated_foreground_on_saturated_background(confirm):
    print(title('saturated foreground on saturated background'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.saturated_fg_colors, k=K), choices(common.saturated_bg_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.saturated_fg_colors, k=K), choices(common.saturated_bg_colors, k=K)))
    for sat_fg, sat_bg in pairs:
        sat_fg_code = core.SAT_COLOR_CODES[sat_fg]
        sat_bg_code = core.SAT_BG_COLOR_CODES[sat_bg]
        
        _print(f"saturated {sat_fg} on saturated {sat_bg}", f"{sat_fg_code};{sat_bg_code}")
