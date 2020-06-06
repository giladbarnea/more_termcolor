from typing import Optional, Union

from more_termcolor.core import COLOR_CODES


def to_color(code: int, obj=None) -> Optional[str]:
    """Examples:
    ::
        to_color(32) # 'green'
        to_color(103) # 'sat bg yellow'
    """
    if isinstance(code, str):
        if not code.isdigit():
            # code is actually a color name
            return code
        # code is a string '1'
        code = int(code)
    if obj is None:
        obj = COLOR_CODES
    for k, v in obj.items():
        if not isinstance(v, dict):
            if v == code:
                return k
        else:
            nested = to_color(code, obj[k])
            if nested is not None:
                return f'{k} {nested}'
    return None  # recursive stop cond


def to_code(color: Union[str, int], obj=None) -> int:
    """Examples:
        ::
            to_code('green') # 32
            to_code('sat bg yellow') # 103
            to_code(32) # 32
        """
    if isinstance(color, int) or color.isdigit():
        # color is actually a color code
        return int(color)
    if obj is None:
        obj = COLOR_CODES
    if ' ' in color:
        keys = color.split()
        for key in keys:
            obj = obj[key]
        return obj
    else:
        return obj[color]


def code_to_ansi(_code: int) -> str:
    return f'\033[{_code}m'


def color_to_ansi(_color: str) -> str:
    """Examples:
    ::
        convert.code_to_ansi('green') # '\x1b[32m'
        color_to_code('sat bg yellow') # '\x1b[103m'
    """
    return f'\033[{color_to_code(_color)}m'


def reset_to_ansi(_reset='normal') -> str:
    return f'\033[{COLOR_CODES["reset"][_reset]}m'
