from typing import Optional, Union

from more_termcolor import core


def to_color(val: Union[str, int], obj=None) -> Optional[str]:
    """Examples:
    ::
        to_color(32) # 'green'
        to_color(103) # 'sat bg yellow'
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


def to_code(val: Union[str, int], obj=None) -> int:
    """Examples:
        ::
            to_code('green') # 32
            to_code('sat bg yellow') # 103
            to_code(32) # 32
        """
    if isinstance(val, int) or val.isdigit():
        # val is actually a color code
        return int(val)
    if obj is None:
        obj = core.COLOR_CODES
    if ' ' in val:
        keys = val.split()
        for key in keys:
            obj = obj[key]
        return obj
    else:
        return obj[val]


# def code_to_ansi(_code: int) -> str:
#     return f'\033[{_code}m'


# def color_to_ansi(_color: str) -> str:
#     """Examples:
#     ::
#         convert.code_to_ansi('green') # '\x1b[32m'
#         color_to_code('sat bg yellow') # '\x1b[103m'
#     """
#     return f'\033[{to_code(_color)}m'

def reset(val: Union[str, int]):
    color = to_color(val)
    return f'\033[{core.RESET_COLOR_CODES[color]}m'

# def reset_to_ansi(_reset='normal') -> str:
#     return f'\033[{COLOR_CODES["reset"][_reset]}m'
