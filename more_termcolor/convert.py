from typing import Union, overload, Optional
import re
from more_termcolor import core

RESET_RE = re.compile(r'(?<=reset ).*')
SATURATED_RE = re.compile(r'(?<=sat ).*')
BACKGROUND_RE = re.compile(r'(?<=on ).*')


@overload
def to_color(val: Union[str, int], obj: dict = None) -> str:
    ...


def to_color(val: Union[str, int], obj=None):
    """Examples:
    ::
        to_color(32) # 'green'
        to_color(103) # 'on satyellow'
    """
    if isinstance(val, str):
        if not val.isdigit():
            # val is actually a color name
            return val
        # val is a string '1'
        val = int(val)
    if obj is None:
        obj = core.COLOR_CODES
    for k, v in obj.items():
        if not isinstance(v, dict):
            if v == val:
                return k
        else:
            nested = to_color(val, obj[k])
            if nested is not None:
                return f'{k} {nested}'
    return None  # recursive stop cond


def to_code(val: Union[str, int]) -> int:
    """Examples:
        ::
            to_code('green') # 32
            to_code('on satyellow') # 103
            to_code(32) # 32
        """
    if isinstance(val, int) or val.isdigit():
        # val is actually a color code
        return int(val)
    obj = core.COLOR_CODES
    if ' ' in val:
        keys = val.split()
        for key in keys:
            obj = obj[key]
        return obj
    else:
        return obj[val]


def _try_get_bg_reset_code(color: str) -> Optional[int]:
    """Examples:
    ::
     ('on red') → 49
     ('on satred') → 49
     ('green') → None
     ('BAD') → None
     ('sat green') → None
     ('on BAD') → KeyError
    """
    match = BACKGROUND_RE.search(color)
    if match:
        actual_color = match.group()
        if actual_color not in core.BG_COLOR_CODES:
            raise KeyError(f"`color` ('{color}') matches '{BACKGROUND_RE.pattern}' but `actual_color` ('{actual_color}') not in BG_COLOR_CODES")
        resetcode = core.RESET_COLOR_CODES['bg']
        return resetcode
    return None


def _try_get_sat_reset_code(color: str) -> Optional[int]:
    """Examples:
    ::
     ('sat green') → 39
     ('green') → None
     ('BAD') → None
     ('sat BAD') → KeyError
     ('on red') → KeyError
     ('on satred') → KeyError
    """
    match = SATURATED_RE.search(color)
    if match:
        # e.g. 'sat [bg ]yellow'
        actual_color = match.group()
        if actual_color not in core.SAT_FG_COLOR_CODES:
            raise KeyError(f"`color` ('{color}') matches '{SATURATED_RE.pattern}' but `actual_color` ('{actual_color}') not in SAT_FG_COLOR_CODES")
        # 39 resets both std fg and sat fg
        return core.RESET_COLOR_CODES['fg']
    return None


def to_reset_code(val):
    """Examples:
    ::
     ('bold') → 22
     ('dark') → 22
     ('green') → 39
     ('sat green') → 39
     ('on red') → 49
     ('on satred') → 49
     (22) → 22
     ('BAD') → KeyError
    """
    color = to_color(val)
    try:
        resetcode = core.RESET_COLOR_CODES[color]
    except KeyError as e:
        match = RESET_RE.search(color)
        if match:
            # happens when passed e.g. '22',
            # in which case `color` is 'reset bold';
            # call again with just 'bold'
            actual_color = match.group()
            return to_reset_code(actual_color)
        
        if color in core.FG_COLOR_CODES:
            resetcode = core.RESET_COLOR_CODES['fg']
            return resetcode
        resetcode = _try_get_bg_reset_code(color)
        if resetcode:
            return resetcode
        resetcode = _try_get_sat_reset_code(color)
        if resetcode:
            return resetcode
        raise
    return resetcode


def reset(val: Union[str, int]):
    resetcode = to_reset_code(val)
    return f'\033[{resetcode}m'
