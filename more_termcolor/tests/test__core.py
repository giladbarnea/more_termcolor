"""This module does not really assert anything programmatically. It just prints and describes what you're supposed to see with your eyes.
Optionally pass '--confirm' to prompt before starting each test, e.g.:
pytest -sxl more_termcolor/tests/test__core.py --confirm"""

from more_termcolor import core, util
from more_termcolor.main import COLOR_CODES_RE
from more_termcolor.colors import bold
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
    return bold(f'\n{text}\n', 'bright white', 'ul')


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
    for color, code in core.FOREGROUND_COLOR_CODES.items():
        _print(color, code)


def test__std_bg_color_codes__sanity(confirm):
    print(title('standard background colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.STANDARD_BACKGROUND_COLOR_CODES.items():
        _print(color, code)


def test__bright_bg_color_codes__sanity(confirm):
    print(title('bright background colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.BRIGHT_BACKGROUND_COLOR_CODES.items():
        _print(color, code)


def test__bright_fg_color_codes__sanity(confirm):
    print(title('bright foreground colors: sanity'))
    if confirm and not util.confirm():
        return
    for color, code in core.BRIGHT_FOREGROUND_COLOR_CODES.items():
        _print(color, code)


def test__std_foreground_on_std_background(confirm):
    print(title(f'standard foreground on standard background (random {K})'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.background_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.background_colors, k=K)))
    
    for fg, bg in pairs:
        fg_code = core.FOREGROUND_COLOR_CODES[fg]
        bg_code = core.BACKGROUND_COLOR_CODES[bg]
        
        _print(f"{fg} on {bg}", f"{fg_code};{bg_code}")


def test__bright_foreground_on_std_background(confirm):
    print(title(f'bright foreground on standard background (random {K})'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.bright_fg_colors, k=K), choices(common.background_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.bright_fg_colors, k=K), choices(common.background_colors, k=K)))
    for bright_fg, bg in pairs:
        bright_fg_code = core.BRIGHT_FOREGROUND_COLOR_CODES[bright_fg]
        bg_code = core.BACKGROUND_COLOR_CODES[bg]
        
        _print(f"bright {bright_fg} on {bg}", f"{bright_fg_code};{bg_code}")


def test__std_foreground_on_bright_background(confirm):
    print(title(f'standard foreground on bright background (random {K})'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.bright_bg_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.foreground_colors, k=K), choices(common.bright_bg_colors, k=K)))
    for fg, bright_bg in pairs:
        fg_code = core.FOREGROUND_COLOR_CODES[fg]
        bright_bg_code = core.BRIGHT_BACKGROUND_COLOR_CODES[bright_bg]
        
        _print(f"{fg} on bright {bright_bg}", f"{fg_code};{bright_bg_code}")


def test__bright_foreground_on_bright_background(confirm):
    print(title(f'bright foreground on bright background (random {K})'))
    if confirm and not util.confirm():
        return
    pairs = list(zip(choices(common.bright_fg_colors, k=K), choices(common.bright_bg_colors, k=K)))
    while common.has_duplicates(pairs) or any(p[0] == p[1] for p in pairs):
        # prevent ('white', 'white')
        pairs = list(zip(choices(common.bright_fg_colors, k=K), choices(common.bright_bg_colors, k=K)))
    for bright_fg, bright_bg in pairs:
        bright_fg_code = core.BRIGHT_FOREGROUND_COLOR_CODES[bright_fg]
        bright_bg_code = core.BRIGHT_BACKGROUND_COLOR_CODES[bright_bg]
        
        _print(f"bright {bright_fg} on bright {bright_bg}", f"{bright_fg_code};{bright_bg_code}")
