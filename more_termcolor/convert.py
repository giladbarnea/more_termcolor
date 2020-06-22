import re
from typing import Union, Optional

from more_termcolor import core

# from snoop import snoop, spy
# from birdseye import eye

# from birdseye import BirdsEye
#
# eye = BirdsEye(num_samples=dict(
#         big=dict(
#                 attributes=100,
#                 dict=100,
#                 list=100,
#                 set=100,
#                 pandas_rows=100,
#                 pandas_cols=100,
#                 ),
#         small=dict(
#                 attributes=100,
#                 dict=100,
#                 list=100,
#                 set=100,
#                 pandas_rows=100,
#                 pandas_cols=100,
#                 ),
#         ))
# RESET_RE = re.compile(r'(?<=reset ).*')
# BRIGHT_RE = re.compile(r'(?<=bright ).*')
# BACKGROUND_RE = re.compile(r'(?<=on ).*')
# COLOR_STRING_RE = re.compile(fr'(?:reset )?(?P<on>on )?(?P<bright>bright )?(?P<actual_color>{"|".join(core.COLORS) + "|" + "|".join(core.RESET_COLOR_CODES)})')

# e.g '[reset ]on [bright ]black'
BACKGROUND_COLOR_RE = re.compile(fr'(?:reset )?(?:on )(?:bright )?(?P<actual_color>{"|".join(core.COLORS)})')
# e.g '[reset ][bright ]black'
FOREGROUND_COLOR_RE = re.compile(fr'(?:reset )?(?:bright )?(?P<actual_color>{"|".join(core.COLORS)})')
# e.g '[reset ]all'
FORMATTING_COLOR_RE = re.compile(fr'(?:reset )?(?P<actual_color>{"|".join(core.RESET_COLOR_CODES)})')
# e.g '[reset ]1'
COLOR_CODE_RE = re.compile(fr'(?:reset )?(?P<color_code>{"|".join(map(str, (*range(0, 10), *range(21, 38), *range(39, 56), *range(90, 98), *range(100, 108))))})')


def to_name(name_or_code: Union[str, int], obj: dict = None) -> Optional[str]:
    """
    >>> to_name(32)
    'green'
    >>> to_name('41')
    'on red'
    >>> to_name(103)
    'on bright yellow'
    >>> to_name('green')
    'green'
    >>> to_name('grin') # doesn't raise!
    'grin'
    """
    
    if isinstance(name_or_code, int):
        name_or_code = str(name_or_code)
    elif not name_or_code.isdigit():
        # name_or_code is actually a color name
        return name_or_code
    if obj is None:
        obj = core.COLOR_CODES
    for k, v in obj.items():
        if isinstance(v, dict):
            nested = to_name(name_or_code, obj[k])
            if nested is not None:
                return f'{k} {nested}'
        else:
            if v == name_or_code:
                return k
    return None  # recursive stop cond


def to_code(name_or_code: Union[str, int]) -> str:
    """
    >>> to_code('green')
    '32'
    >>> to_code('on red')
    '41'
    >>> to_code('on bright yellow')
    '103'
    >>> to_code(32)
    '32'
    """
    
    if isinstance(name_or_code, int) or name_or_code.isdigit():
        # name_or_code is actually a color code
        return str(name_or_code)
    obj = core.COLOR_CODES
    if ' ' in name_or_code:
        keys = name_or_code.split()
        for key in keys:
            obj = obj[key]
        return obj
    else:
        return obj[name_or_code]


# @snoop
def to_reset_code(name_or_code: Union[str, int]) -> str:
    """
     >>> to_reset_code('bold')
     '22'
     >>> to_reset_code('dark')
     '22'
     >>> to_reset_code('green')
     '39'
     >>> to_reset_code('bright green')
     '39'
     >>> to_reset_code('on red')
     '49'
     >>> to_reset_code('on bright red')
     '49'
     >>> to_reset_code(22)
     '22'
     >>> to_reset_code('1')
     '22'
     >>> to_reset_code('reset bold')
     '22'
     >>> to_reset_code('BAD')
     Traceback (most recent call last):
     ...
     KeyError: "to_reset_code('BAD'): color 'BAD' isn't recognized"
    
    """
    color = to_name(name_or_code)
    try:
        return core.RESET_COLOR_CODES[color]
    except KeyError as e:
        # discard 'reset' if exists (non-captured)
        background_match = BACKGROUND_COLOR_RE.fullmatch(color)
        if background_match:
            return core.RESET_COLOR_CODES['on']
        foreground_match = FOREGROUND_COLOR_RE.fullmatch(color)
        if foreground_match:
            return core.RESET_COLOR_CODES['fg']
        formatting_match = FORMATTING_COLOR_RE.fullmatch(color)
        if formatting_match:
            actual_color = formatting_match.groupdict()['actual_color']
            return core.RESET_COLOR_CODES[actual_color]
        code_match = COLOR_CODE_RE.fullmatch(color)
        if code_match:
            color_code = code_match.groupdict()['color_code']
            actual_color = to_name(color_code)
            return core.RESET_COLOR_CODES[actual_color]
        raise KeyError(f"to_reset_code({repr(name_or_code)}): color {repr(color)} isn't recognized") from e


def to_boundary(*names_or_codes: Union[str, int]) -> str:
    r"""
    >>> to_boundary(1)
    '\x1b[1m'
    >>> to_boundary('bold')
    '\x1b[1m'
    >>> to_boundary(1, '2', 'on bright black')
    '\x1b[1;2;100m'
    """
    code_set = set()  # allows checking for duplicates in O(1) while keeping order
    codes = []
    for code in map(to_code, names_or_codes):
        if code in code_set:
            continue
        code_set.add(code)
        codes.append(code)
    
    return f'\x1b[{";".join(codes)}m'
