from typing import Optional

from more_termcolor.manager import COLOR_CODES


def code_to_color(_code: int, _obj=None) -> Optional[str]:
    """Examples:
    ::
        code_to_color(32) # 'green'
        code_to_color(103) # 'sat bg yellow'
    """
    if _obj is None:
        _obj = COLOR_CODES
    for k, v in _obj.items():
        if not isinstance(v, dict):
            if v == _code:
                return k
        else:
            nested = code_to_color(_code, _obj[k])
            if nested is not None:
                return f'{k} {nested}'
    return None  # recursive stop cond


def color_to_code(_color: str, _obj=None) -> int:
    """Examples:
    ::
        color_to_code('green') # 32
        color_to_code('sat bg yellow') # 103
    """
    if _obj is None:
        _obj = COLOR_CODES
    if ' ' in _color:
        keys = _color.split()
        for key in keys:
            _obj = _obj[key]
        return _obj
    else:
        return _obj[_color]


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
