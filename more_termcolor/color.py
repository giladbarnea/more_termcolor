import re
from typing import Union

from more_termcolor import convert, core

COLOR_CODES_RE = r'(\d{,3})(?:;)?(\d{,3})?(?:;)?(\d{,3})?'
COLOR_BOUNDARY_RE = re.compile(fr'\033\[{COLOR_CODES_RE}m')
ON_COLOR_RE = re.compile(r'on[_ ](\w{3,9})')


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
    outer_open_codes = [convert.to_code(c) for c in colors]
    start = f'\033[{";".join(outer_open_codes)}m'
    # TODO:
    #  if inner has fmt or inner has bg:
    #       reset inner
    #       if outer has fmt and outer.reset == inner.reset:
    #           also re-open outer
    #  else:
    #       if outer is fmt:
    #           reset fg
    #       else:
    #           re-open outer
    try:
        # TODO (performance): less iterations, also don't replace substrings if not needed
        # if more than one open/reset pairs exist in text,
        # ignore them (*_) assuming they'd been recursively
        # taken care of.
        inner_open, *_, inner_reset = re.finditer(COLOR_BOUNDARY_RE, text)
        inner_open_codes = [c for c in inner_open.groups() if c]
        outer_has_formatting = any(c in core.FORMATTING_CODES for c in outer_open_codes)
        inner_has_formatting = any(c in core.FORMATTING_CODES for c in inner_open_codes)
        
        if inner_has_formatting:
            # replace existing inner reset codes with the inner colors' matching reset codes
            #
            proper_inner_reset_codes = [convert.to_reset_code(c) for c in inner_open_codes]
            if outer_has_formatting:
                #
                outer_reset_codes = [convert.to_reset_code(c) for c in outer_open_codes]
                if any(oc in proper_inner_reset_codes for oc in outer_reset_codes):
                    proper_inner_reset_codes.extend(outer_open_codes)
            proper_inner_reset = f'\033[{";".join(proper_inner_reset_codes)}m'
            text = text.replace(inner_reset.group(), proper_inner_reset, 1)
        
        else:
            if outer_has_formatting:
                # reset fg
                text = text.replace(inner_reset.group(), '\033[39m', 1)
            else:
                # replace inner reset with outer open
                text = text.replace(inner_reset.group(), start, 1)
    except ValueError as e:  # not enough values to unpack (COLOR_BOUNDARY_RE did not match)
        pass
    # reset = f'\033[{";".join(map(str, map(convert.to_reset_code, colors)))}m'
    reset = f'\033[0m'
    ret = f'{start}{text}{reset}'
    # spacyprint(f'returning: {repr(ret)}', ret)
    return ret


def cprint(text, color=None, on_color=None, attrs=(), *colors, **kwargs):
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
        actual_color = ON_COLOR_RE.match(on_color).groups()[0]
        on_color = f'on {actual_color}'
    if isinstance(attrs, (str, int)):
        print((colored(text, color, on_color, attrs, *colors)), **kwargs)
    else:
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
