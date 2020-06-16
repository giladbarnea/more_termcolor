import re
from typing import Union, Optional

from more_termcolor import core

RESET_RE = re.compile(r'(?<=reset ).*')
BRIGHT_RE = re.compile(r'(?<=bright ).*')
BACKGROUND_RE = re.compile(r'(?<=on ).*')
COLOR_STRING_RE = re.compile(fr'(?:reset )?(?P<on>on )?(?P<bright>bright )?(?P<actual_color>{"|".join(core.COLORS) + "|" + "|".join(core.RESET_COLOR_CODES)})')


def to_color(name_or_code: Union[str, int], obj: dict = None) -> Optional[str]:
    """Examples:
    ::
        to_color(32) # 'green'
        to_color(41) # 'on red'
        to_color(103) # 'on bright yellow'
        to_color('green') # 'green'
    """
    
    if isinstance(name_or_code, int):
        name_or_code = str(name_or_code)
    elif not name_or_code.isdigit():
        # name_or_code is actually a color name
        return name_or_code
    if obj is None:
        obj = core.COLOR_CODES
    for k, v in obj.items():
        if not isinstance(v, dict):
            if v == name_or_code:
                return k
        else:
            nested = to_color(name_or_code, obj[k])
            if nested is not None:
                return f'{k} {nested}'
    return None  # recursive stop cond


def to_code(name_or_code: Union[str, int]) -> str:
    """Examples:
    ::
        to_code('green') # '32'
        to_code('on red') # '41'
        to_code('on bright yellow') # '103'
        to_code(32) # '32'
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


def to_reset_code(name_or_code: Union[str, int]) -> str:
    """Examples:
    ::
     ('bold') → '22'
     ('dark') → '22'
     ('green') → '39'
     ('bright green') → '39'
     ('on red') → '49'
     ('on bright red') → '101'
     (22) → '22'
     (1) → '22'
     ('BAD') → KeyError
    """
    color = to_color(name_or_code)
    try:
        return core.RESET_COLOR_CODES[color]
    except KeyError as e:
        # discard 'reset' if exists (non-captured)
        match = COLOR_STRING_RE.match(color)
        if not match:
            raise KeyError(f"to_reset_code({repr(name_or_code)}): color {repr(color)} isn't recognized") from e
        d = match.groupdict()
        actual_color = d['actual_color']
        bg = d['on'] is not None
        bright = d['bright'] is not None
        
        if not bg and not bright:
            # simply "red"
            if actual_color in core.RESET_COLOR_CODES:
                return core.RESET_COLOR_CODES[actual_color]
            if actual_color in core.FOREGROUND_COLOR_CODES:
                return core.RESET_COLOR_CODES['fg']
            raise KeyError(f"to_reset_code({repr(name_or_code)}): actual_color ({actual_color}) isn't a reset key nor a foreground color, and there's no preceding 'on'/'bright'") from e
        if bg:
            if actual_color not in core.BACKGROUND_COLOR_CODES:
                raise KeyError(f"to_reset_code({repr(name_or_code)}): actual_color ({actual_color}) isn't a background color") from e
            # standard bg and bright bg colors are both reset by 49
            return core.RESET_COLOR_CODES['on']
        return core.RESET_COLOR_CODES['fg']


def to_boundary(*names_or_codes: Union[str, int]) -> str:
    code_set = set()  # allows checking for duplicates in O(1) while keeping order
    codes = []
    for code in map(to_code, names_or_codes):
        if code in code_set:
            continue
        code_set.add(code)
        codes.append(code)
    
    return f'\x1b[{";".join(codes)}m'
