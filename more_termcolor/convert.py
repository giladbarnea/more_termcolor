import re
from typing import Union, Optional

from more_termcolor import core

RESET_RE = re.compile(r'(?<=reset ).*')
BRIGHT_RE = re.compile(r'(?<=bright ).*')
BACKGROUND_RE = re.compile(r'(?<=on ).*')
COLOR_STRING_RE = re.compile(r'(?:reset )?(?P<on>on )?(?P<bright>bright )?(?P<actual_color>\w{3,9})')


def to_color(val: Union[str, int], obj: dict = None) -> Optional[str]:
    """Examples:
    ::
        to_color(32) # 'green'
        to_color(41) # 'on red'
        to_color(103) # 'on bright yellow'
        to_color('green') # 'green'
    """
    
    if isinstance(val, int):
        val = str(val)
    elif not val.isdigit():
        # val is actually a color name
        return val
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


def to_code(val: Union[str, int]) -> str:
    """Examples:
    ::
        to_code('green') # '32'
        to_code('on red') # '41'
        to_code('on bright yellow') # '103'
        to_code(32) # '32'
        """
    if isinstance(val, int) or val.isdigit():
        # val is actually a color code
        return str(val)
    obj = core.COLOR_CODES
    if ' ' in val:
        keys = val.split()
        for key in keys:
            obj = obj[key]
        return obj
    else:
        return obj[val]


# def _try_get_bg_reset_code(color: str) -> Optional[int]:
#     """Examples:
#     ::
#      ('on red') → 49
#      ('on brightred') → 49
#      ('green') → None
#      ('BAD') → None
#      ('bright green') → None
#      ('on BAD') → KeyError
#     """
#     match = BACKGROUND_RE.search(color)
#     if match:
#         # e.g. 'on [bright ]yellow'
#         actual_color = match.group()
#         if actual_color not in core.STANDARD_BACKGROUND_COLOR_CODES:
#             raise KeyError(f"`color` ('{color}') matches '{BACKGROUND_RE.pattern}' but `actual_color` ('{actual_color}') not in STANDARD_BACKGROUND_COLOR_CODES")
#         resetcode = core.RESET_COLOR_CODES['on']
#         return resetcode
#     return None


# def _try_get_bright_reset_code(color: str) -> Optional[int]:
#     """Examples:
#     ::
#      ('bright green') → 39
#      ('green') → None
#      ('BAD') → None
#      ('bright BAD') → KeyError
#      ('on red') → KeyError
#      ('on brightred') → KeyError
#     """
#     match = BRIGHT_RE.search(color)
#     if match:
#         # e.g. 'bright yellow'
#         actual_color = match.group()
#         if actual_color not in core.BRIGHT_FOREGROUND_COLOR_CODES:
#             raise KeyError(f"`color` ('{color}') matches '{BRIGHT_RE.pattern}' but `actual_color` ('{actual_color}') not in BRIGHT_FOREGROUND_COLOR_CODES")
#         # 39 resets both std fg and bright fg
#         return core.RESET_COLOR_CODES['fg']
#     return None


def to_reset_code(val):
    """Examples:
    ::
     ('bold') → 22
     ('dark') → 22
     ('green') → 39
     ('bright green') → 39
     ('on red') → 49
     ('on bright red') → 101
     (22) → 22
     ('BAD') → KeyError
    """
    color = to_color(val)
    try:
        return core.RESET_COLOR_CODES[color]
    except KeyError as e:
        # discard 'reset' if exists (non-captured)
        d = COLOR_STRING_RE.match(color).groupdict()
        actual_color = d['actual_color']
        bg = d['on'] is not None
        bright = d['bright'] is not None
        # if actual_color in core.RESET_COLOR_CODES:
        #     return core.RESET_COLOR_CODES[color]
        
        # if match:
        #     # happens when val is e.g. '22',
        #     # in which case to_color(val) → 'reset bold';
        #     # call again with just 'bold'
        #     actual_color = match.group()
        #     return to_reset_code(actual_color)
        # d = COLOR_STRING_RE.match(color).groupdict()
        
        if not bg and not bright:
            if actual_color in core.RESET_COLOR_CODES:
                return core.RESET_COLOR_CODES[actual_color]
            if actual_color in core.FOREGROUND_COLOR_CODES:
                return core.RESET_COLOR_CODES['fg']
            raise KeyError(f"to_reset_code({repr(val)}): actual_color ({actual_color}) isn't a reset key nor a foreground color, and there's no preceding 'on'/'bright'") from e
        if bg:
            # standard bg and bright bg colors are both reset by 49
            return core.RESET_COLOR_CODES['on']
        return core.RESET_COLOR_CODES['fg']
        # if color in core.FOREGROUND_COLOR_CODES:
        #     resetcode = core.RESET_COLOR_CODES['fg']
        #     return resetcode
        # resetcode = _try_get_bg_reset_code(color)
        # if resetcode:
        #     return resetcode
        # resetcode = _try_get_bright_reset_code(color)
        # if resetcode:
        #     return resetcode
        # raise


def reset(val: Union[str, int]):
    resetcode = to_reset_code(val)
    return f'\033[{resetcode}m'
