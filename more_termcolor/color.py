import re
from typing import Union

from more_termcolor import convert, core
from more_termcolor.util import spacyprint

COLOR_CODES_RE = r'(\d{,3})(?:;)?(\d{,3})?(?:;)?(\d{,3})?'
COLOR_BOUNDARY_RE = re.compile(fr'\033\[{COLOR_CODES_RE}m')


#####################
# Formatting (some) #
#####################

def bold(text, *colors):
    return colored(text, 'bold', *colors)


def dark(text, *colors):
    return colored(text, 'dark', *colors)


def italic(text, *colors):
    return colored(text, 'italic', *colors)


def ul(text, *colors):
    return colored(text, 'ul', *colors)


def reverse(text, *colors):
    return colored(text, 'reverse', *colors)


######################
# Foreground (30-37) #
######################


def black(text, *colors):
    return colored(text, 'black', *colors)


def red(text, *colors):
    return colored(text, 'red', *colors)


def green(text, *colors):
    return colored(text, 'green', *colors)


def yellow(text, *colors):
    return colored(text, 'yellow', *colors)


def blue(text, *colors):
    return colored(text, 'blue', *colors)


def magenta(text, *colors):
    return colored(text, 'magenta', *colors)


def cyan(text, *colors):
    return colored(text, 'cyan', *colors)


def white(text, *colors):
    return colored(text, 'white', *colors)


###############################
# Saturated foreground (some) #
###############################
def satblack(text, *colors):
    return colored(text, 'sat black', *colors)


def satwhite(text, *colors):
    return colored(text, 'sat white', *colors)


def satred(text, *colors):
    return colored(text, 'sat red', *colors)


def satgreen(text, *colors):
    return colored(text, 'sat green', *colors)


def satyellow(text, *colors):
    return colored(text, 'sat yellow', *colors)


###########
# colored #
###########

def colored(text: str, *colors: Union[str, int]):
    # spacyprint(f'text: {text}', f'colors: {colors}')
    outer_open_codes = [convert.to_code(c) for c in colors]
    # TODO: remove map str
    start = f'\033[{";".join(outer_open_codes)}m'
    # spacyprint(f'outer_open_codes:', outer_open_codes, f'colors:', colors)
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
        # match = COLOR_BOUNDARY_RE.search(text)
        # nested_codes = [g for g in match.groups() if g]
        
        # if more than one open/reset pairs exist in text,
        # ignore them (*_) assuming they'd been recursively
        # taken care of.
        nested_open, *_, nested_reset = re.finditer(COLOR_BOUNDARY_RE, text)
        nested_open_codes = [c for c in nested_open.groups() if c]
        outer_has_formatting = any(c in core.FORMATTING_CODES for c in outer_open_codes)
        nested_has_formatting = any(c in core.FORMATTING_CODES for c in nested_open_codes)
        nested_reset_codes = [rc for rc in nested_reset.groups() if rc]
        # spacyprint(f'nested_open: {nested_open}',
        #            f'nested_reset: {nested_reset}',
        #            f'nested_open_codes: {nested_open_codes}',
        #            f'outer_has_formatting: {outer_has_formatting}',
        #            f'nested_has_formatting: {nested_has_formatting}',
        #            f'nested_reset_codes: {nested_reset_codes}')
        if nested_has_formatting:
            proper_nested_reset_codes = [convert.to_reset_code(c) for c in nested_open_codes]
            if outer_has_formatting:
                outer_reset_codes = [convert.to_reset_code(c) for c in outer_open_codes]
                if any(oc in proper_nested_reset_codes for oc in outer_reset_codes):
                    proper_nested_reset_codes.extend(outer_open_codes)
            proper_nested_reset = f'\033[{";".join(proper_nested_reset_codes)}m'
            # spacyprint(f'replacing nested reset with proper nested reset. before: ', repr(text), text)
            text = text.replace(nested_reset.group(), proper_nested_reset, 1)
            # spacyprint(f'after: ', repr(text), text)
        
        else:
            if outer_has_formatting:
                # spacyprint(f'replacing nested reset with fg reset. before: ', repr(text), text)
                # reset fg
                text = text.replace(nested_reset.group(), '\033[39m', 1)
                # spacyprint(f'after: ', repr(text), text)
            else:
                # spacyprint(f'replacing nested reset with outer open. before: ', repr(text), text)
                # replace nested reset with outer open
                text = text.replace(nested_reset.group(), start, 1)
                # spacyprint(f'after: ', repr(text), text)
    except ValueError as e:  # not enough values to unpack (COLOR_BOUNDARY_RE did not match)
        pass
    # reset = f'\033[{";".join(map(str, map(convert.to_reset_code, colors)))}m'
    reset = f'\033[0m'
    ret = f'{start}{text}{reset}'
    # spacyprint(f'returning: {repr(ret)}', ret)
    return ret


def cprint(text, color=None, on_color=None, attrs=None, *colors, **kwargs):
    """Print colorized text.
    
    Can be used instead of the original termcolor's cprint() and would work exactly the same,
    but also allows for passing any extra colors, or skipping the awkward signature altogether, e.g.:
    ::
        # old style
        cprint('Hello, World!', 'red', 'on_cyan', attrs=['reverse', 'blink'])
        
        # is equivalent to:
        cprint('Hello, World!', 'red', 'on cyan', 'reverse', 'blink')
    
    It accepts kw-arguments of print function.
    """
    if on_color:
        *_, actual_color = on_color.partition('_')
        on_color = f'on {actual_color}'
    
    print((colored(text, color, on_color, *attrs, *colors)), **kwargs)


__all__ = [
    'bold',
    'dark',
    'italic',
    'ul',
    'reverse',
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'satblack',
    'satwhite',
    'satred',
    'satgreen',
    'satyellow',
    'colored',
    ]
