import re
from typing import Union, Optional

from more_termcolor import core

RESET_RE = re.compile(r'(?<=reset ).*')
BRIGHT_RE = re.compile(r'(?<=bright ).*')
BACKGROUND_RE = re.compile(r'(?<=on ).*')
COLOR_STRING_RE = re.compile(fr'(?:reset )?(?P<on>on )?(?P<bright>bright )?(?P<actual_color>{"|".join(core.COLORS) + "|" + "|".join(core.FORMATTING_COLORS)})')


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
    
    # TODO: probably remove; decide whether this module is for inner use and if so, raise hard errors
    def _soft_keyerror(_obj, _key, _e: KeyError):
        from pprint import pformat
        _errmsg = '\n'.join([f"Got a KeyError when trying to convert the color name {repr(name_or_code)} to color code.",
                             f'key: "{_key}" is not found in obj:',
                             pformat(_obj, depth=1),
                             f"Additional exception args: {', '.join(_e.args)}" if _e.args else ''])
        print(f'\x1b[91;40m{_errmsg}\x1b[39;22m')
    
    if isinstance(name_or_code, int) or name_or_code.isdigit():
        # name_or_code is actually a color code
        return str(name_or_code)
    obj = core.COLOR_CODES
    if ' ' in name_or_code:
        keys = name_or_code.split()
        for key in keys:
            try:
                obj = obj[key]
            except KeyError as e:
                if name_or_code in core.COLORS or name_or_code in core.FORMATTING_COLORS:
                    raise KeyError
                    _soft_keyerror(obj, key, e)
                    return name_or_code
                else:
                    raise
        return obj
    else:
        try:
            return obj[name_or_code]
        except KeyError as e:
            if name_or_code in core.COLORS or name_or_code in core.FORMATTING_COLORS:
                _soft_keyerror(obj, name_or_code, e)
                return name_or_code
            else:
                raise


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
    return f'\x1b[{";".join(map(to_code, names_or_codes))}m'
