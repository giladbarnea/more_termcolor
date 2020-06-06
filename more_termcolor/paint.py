import re
from typing import Union
from more_termcolor import convert, settings, core
from pprint import pformat

from more_termcolor.util import spacyprint

CODES_RE = re.compile(r'\033\[(\d{,3})(?:;)?(\d{,3})?(?:;)?(\d{,3})?m')
COLOR_BOUNDARY = r'\033\[\d{,3}(;\d{,3})?m'
NESTED_RE = re.compile(fr'(?P<outer_open>{COLOR_BOUNDARY})'
                       r'(?P<outer_content_a>[^\033]*)'
                       fr'(?P<inner_open>{COLOR_BOUNDARY})'
                       r'(?P<inner_content>[^\033]*)'
                       fr'(?P<inner_close>{COLOR_BOUNDARY})'
                       r'(?P<outer_content_b>[^\033]*)'
                       fr'(?P<outer_close>{COLOR_BOUNDARY})'
                       )


def reset_text(text: str, reset_color='all'):
    return f'{text}{convert.reset(reset_color)}'


def fix_nested_colors(m: re.Match):
    dct = m.groupdict()
    outer_open = dct['outer_open']
    outer_close = dct['outer_close']
    outer_content_a = dct['outer_content_a']
    outer_content_b = dct['outer_content_b']
    inner_content = dct['inner_content']
    inner_open = dct['inner_open']
    inner_close = dct['inner_close']
    ret = f'{outer_open}{outer_content_a}{outer_close}{inner_open}{inner_content}{inner_close}{outer_open}{outer_content_b}{outer_close}'
    if settings.debug:
        print('\nfix_nested_colors()', f'ret: ', ret, repr(ret), pformat(dct), sep='\n', end='\n')
    return ret


def yellow(text: any, reset_all: bool = True):
    # 33
    return paint(text, 'yellow', reset='all' if reset_all is True else False)


def red(text: any, reset_all: bool = True):
    # text = re.sub(r'(?<=\033)(.*)(\[\d{,3}m)', lambda m: m.groups()[0] + '[31m', text)
    # 31
    return paint(text, 'red', reset='all' if reset_all is True else False)


def green(text: any, reset_all: bool = True):
    # 32
    return paint(text, 'green', reset='all' if reset_all is True else False)


def bold(text: any, reset_all: bool = True):
    # 1
    return paint(text, 'bold', reset='all' if reset_all is True else False)


def faint(text: any, reset_all: bool = True):
    # 2
    return paint(text, 'faint', reset='all' if reset_all is True else False)


def satblack(text: any, reset_all: bool = True):
    # 90
    return paint(text, 'sat black', reset='all' if reset_all is True else False)


def satwhite(text: any, reset_all: bool = True):
    # sat white
    return paint(text, 'sat white', reset='all' if reset_all is True else False)


def ul(text, reset_all: bool = True):
    """
    If specified `True` (default), `reset_all` passes `{ 'reset' : 'all' }` which resets `all` (everything).
    Otherwise, passes `{ 'reset' : 'ul' }` which resets only ul
    """
    # 4
    return paint(text, 'ul', reset='all' if reset_all is True else 'ul')


def italic(text, reset_all: bool = True):
    """
    If specified `True` (default), `reset_all` passes `{ 'reset' : 'all' }` which resets `all` (everything).
    Otherwise, passes `{ 'reset' : 'italic' }` which resets only italic
    """
    return paint(text, 'italic', reset='all' if reset_all is True else 'italic')


def paint(text: any, *colors: Union[str, int]):
    if settings.debug:
        spacyprint(f'text: {text}', f'colors: {colors}')
    outer_open_codes = [convert.to_code(c) for c in colors]
    start = f'\033[{";".join(map(str, outer_open_codes))}m'
    if settings.debug:
        spacyprint(f'outer_open_codes:', outer_open_codes, f'colors', colors)
    # TODO:
    #  if nested is fmt:
    #       reset nested
    #       if outer is fmt and outer.reset == nested.reset:
    #           also re-open outer
    #  else:
    #       if outer is fmt:
    #           reset fg
    #       else:
    #           re-open outer
    try:
        # match = CODES_RE.search(text)
        # nested_codes = [g for g in match.groups() if g]
        
        # if more than one open/reset pairs exist in text,
        # ignore them (*_) because they'd been recursively
        # taken care of.
        nested_open, *_, nested_reset = re.finditer(CODES_RE, text)
        nested_open_codes = nested_open.groups()
        outer_has_formatting = any(c in core.FORMATTING_CODES for c in outer_open_codes)
        nested_has_formatting = any(c in core.FORMATTING_CODES for c in nested_open_codes)
        nested_reset_codes = nested_reset.groups()
        if settings.debug:
            spacyprint(f'nested_open: {nested_open}',
                       f'nested_reset: {nested_reset}',
                       f'nested_open_codes: {nested_open_codes}',
                       f'outer_has_formatting: {outer_has_formatting}',
                       f'nested_has_formatting: {nested_has_formatting}',
                       f'nested_reset_codes: {nested_reset_codes}')
        if nested_has_formatting:
            should_change = nested_reset_codes != [convert.to_reset_code(c) for c in nested_open_codes]
            print()
            # nested_reset = f'\033[{";".join(map(str, map(convert.to_reset_code, nested_codes)))}m'
            # painted = f'{start}{text}{reset}'
            # try:
            #     # in painted substrings, replace their reset start_code with current's start start_code
            #     # [RED]bla[PURPLE]plurp[/PURPLE]bzorg[/RED] → [RED]bla[PURPLE]plurp[RED]bzorg[/RED]
            #     # what's needed:
            #     # [RED]bla[PURPLE]plurp[/PURPLE]bzorg[/RED] → [RED]bla[/RED][PURPLE]plurp[/PURPLE][RED]bzorg[/RED]
            #
            #     painted = re.sub(NESTED_RE, fix_nested_colors, painted)
            # except TypeError as e:
            #     pass
        else:
            if outer_has_formatting:
                # reset fg
                pass
            else:
                # replace nested reset with outer open
                if settings.debug:
                    spacyprint(f'replacing nested reset with outer open. before: ', repr(text), text)
                text = text.replace(nested_reset.group(), start, 1)
                if settings.debug:
                    spacyprint(f'after: ', repr(text), text)
    except ValueError as e:  # not enough values to unpack (CODES_RE did not match)
        pass
    # reset = f'\033[{";".join(map(str, map(convert.to_reset_code, colors)))}m'
    reset = f'\033[0m'
    painted = f'{start}{text}{reset}'
    if settings.debug:
        spacyprint(f'returning painted: {repr(painted)}', painted)
    if settings.print:
        print(painted)
    return painted

# __all__ = ['yellow',
#            'red',
#            'green',
#            'bold',
#            'faint',
#            'satblack',
#            'satwhite',
#            'ul',
#            'italic',
#            'paint']
# if __name__ == '__main__':
#     _termcolors()
