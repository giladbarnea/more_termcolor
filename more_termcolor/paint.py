import re
from typing import Union
from more_termcolor import convert, settings


def reset_text(text: str, reset_color='normal'):
    return f'{text}{convert.reset_to_ansi(reset_color)}'


def fix_internal_colors(m: re.Match):
    return ''.join(m.groups()[0:2]) + m.groups()[-1] + ''.join(m.groups()[2:5]) + m.groups()[0] + ''.join(m.groups()[-2:])


def _termcolors():
    for i in range(1, 108):
        if i in [5, 6, 8, 30, 38, 39, 98, 99] or (10 <= i <= 20) or (22 <= i <= 29) or (48 <= i <= 89):
            continue
        
        print(paint(f'{i}\thello\t', convert.code_to_color(i)))


def yellow(text: any, reset_normal: bool = True):
    # 33
    return paint(text, 'yellow', reset='normal' if reset_normal is True else False)


def red(text: any, reset_normal: bool = True):
    # text = re.sub(r'(?<=\033)(.*)(\[\d{,3}m)', lambda m: m.groups()[0] + '[31m', text)
    # 31
    return paint(text, 'red', reset='normal' if reset_normal is True else False)


def green(text: any, reset_normal: bool = True):
    # 32
    return paint(text, 'green', reset='normal' if reset_normal is True else False)


def bold(text: any, reset_normal: bool = True):
    # 1
    return paint(text, 'bold', reset='normal' if reset_normal is True else False)


def grey(text: any, reset_normal: bool = True):
    # 2
    return paint(text, 'grey', reset='normal' if reset_normal is True else False)


def lightgrey(text: any, reset_normal: bool = True):
    # 90
    return paint(text, 'lightgrey', reset='normal' if reset_normal is True else False)


def satwhite(text: any):
    # sat white
    return paint(text, 97)


def ul(text, reset_normal: bool = True):
    """
    If specified `True` (default), `reset_normal` passes `{ 'reset' : 'normal' }` which resets `normal` (everything).
    Otherwise, passes `{ 'reset' : 'ul' }` which resets only ul
    """
    # 4
    return paint(text, 'ul', reset='normal' if reset_normal is True else 'ul')


def italic(text, reset_normal: bool = True):
    """
    If specified `True` (default), `reset_normal` passes `{ 'reset' : 'normal' }` which resets `normal` (everything).
    Otherwise, passes `{ 'reset' : 'italic' }` which resets only italic
    """
    return paint(text, 'italic', reset='normal' if reset_normal is True else 'italic')


def paint(text: any, *colors: Union[str, int], reset: Union[str, bool] = 'normal'):
    if settings.debug:
        print(f'text: {text}', f'colors: {colors}', f'reset: {reset}')
    start = ''
    for clr in colors:
        if isinstance(clr, int):
            # * 31
            start_code = clr
        else:
            # * 'red'
            start_code = convert.color_to_code(clr)
        start_ansi = convert.code_to_ansi(start_code)
        start += start_ansi
        if settings.debug:
            print(rf'code: {start_code}, ansi: {repr(start_ansi)}, start: {start}')
    # this also works: '\033[01;97mHI'
    
    if reset is not False:
        # this means reset is a string.
        # otherwise, (when reset is False), not resetting at all
        reset_ansi = convert.reset_to_ansi(reset)
        # painted = reset_text(f'{start}{text}', reset)
        painted = f'{start}{text}{reset_ansi}'
        if len(colors) == 1:
            # currently only works for single color
            try:
                # in painted substrings, replace their reset start_code with current's start start_code
                # [RED]bla[PURPLE]plurp[/PURPLE]bzorg[/RED] → [RED]bla[PURPLE]plurp[RED]bzorg[/RED]
                # what's needed:
                # [RED]bla[PURPLE]plurp[/PURPLE]bzorg[/RED] → [RED]bla[/RED][PURPLE]plurp[/PURPLE][RED]bzorg[/RED]
                # text = re.sub(r'(?<=\033)(.*)(\[\d{,3}m)', lambda m: m.groups()[0] + f'[{start_code}m', text)
                regex = r'(\033\[\d{,3}m)(.*)(\033\[\d{,3}m)(.*)(\033\[\d{,3}m)(.*)(\033\[\d{,3}m)'
                painted = re.sub(regex, fix_internal_colors, painted)
            except TypeError as e:
                pass
        if settings.debug:
            print(f'reset: {repr(reset)}, painted: {repr(painted)}')
    else:
        painted = f'{start}{text}'
    if settings.print:
        print(painted)
    return painted

# if __name__ == '__main__':
#     _termcolors()
