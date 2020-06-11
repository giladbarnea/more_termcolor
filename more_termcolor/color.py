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

def colored(text: str, *colors: Union[str, int]) -> str:
    """
    Multiple colors can be passed, and their color codes will be merged.
    The resulting string will always end with a 'reset all' code (0).
    There will never be a 'reset all' code in the middle of the resulting string.
    
    If any colors already exist within `text`, this function
    tries to keep them intact as much as possible.

    For example, if a user passes `colored(mytext, "bold")`,
    and `mytext` is already underlined, the result will be both bold AND underlined.

    If `mytext` only contains an underlined substring, surrounded by regular text,
    the whole resulting text will be bold, but only the underlined substring will be underlined.

    This behavior is similar to nesting html tags (i.e. "<b>bold <i>and italic</i></b>").
    
    Any duplicate colors are merged.
    
    I'm not sure about the maximum number of colors that can be passed,
    because I stopped adding after `("foo", "red", "on black", "bold", "dark", "italic", "underline", "blink", "reverse", "strike", "overline")` worked.
    
    :param colors: each color can have a "sat [color]", "on [color]", or "on sat [color]" preceding it, so "on sat blue"
     will color the text with a saturated blue background.
     If no color is passed, returns `text` unmodified.
    
    :return: the formatted string.
    """
    
    if not colors:
        return text
    
    def _is_non_foreground(_code):
        return _code not in core.FOREGROUND_CODES and _code not in core.SATURATED_FOREGROUND_CODES
    
    outer_open_codes = []
    outer_reset_codes = []
    outer_reset_2_open = dict()
    outer_has_non_foreground = False
    for color in colors:
        open_code = convert.to_code(color)
        # TODO: complexity
        if open_code in outer_open_codes:
            continue
        outer_open_codes.append(open_code)
        reset_code = convert.to_reset_code(open_code)
        # TODO: this probably fails when open colors are bold,dark!
        outer_reset_2_open[reset_code] = open_code
        outer_reset_codes.append(reset_code)
        if not outer_has_non_foreground and _is_non_foreground(open_code):
            outer_has_non_foreground = True
    start = f'\033[{";".join(outer_open_codes)}m'
    try:
        # TODO (performance): don't replace substrings if not needed
        # if more than one open/reset pairs exist in text,
        # ignore them (*_) assuming they'd been recursively
        # taken care of.
        inner_open, *_, inner_reset = re.finditer(COLOR_BOUNDARY_RE, text)
        inner_open_codes = []
        inner_has_non_foreground = False
        inner_reset_codes = []
        outer_open_codes_to_reopen = []
        for inner_open_code in inner_open.groups():
            if not inner_open_code:
                continue
            inner_open_codes.append(inner_open_code)
            inner_reset_code = convert.to_reset_code(inner_open_code)
            inner_reset_codes.append(inner_reset_code)
            for outer_reset_code in outer_reset_codes:
                if inner_reset_code == outer_reset_code:
                    outer_open_code = outer_reset_2_open[outer_reset_code]
                    outer_open_codes_to_reopen.append(outer_open_code)
            if not inner_has_non_foreground and _is_non_foreground(inner_open_code):
                inner_has_non_foreground = True
        
        if inner_has_non_foreground:
            # replace existing inner reset codes with
            # the inner colors' matching reset codes
            
            if outer_has_non_foreground:
                inner_reset_codes.extend(outer_open_codes_to_reopen)
            proper_inner_reset = f'\033[{";".join(inner_reset_codes)}m'
            text = text.replace(inner_reset.group(), proper_inner_reset, 1)
        
        else:
            if outer_has_non_foreground:
                # reset fg
                text = text.replace(inner_reset.group(), '\033[39m', 1)
            else:
                # replace inner reset with outer open
                text = text.replace(inner_reset.group(), start, 1)
    except ValueError as e:
        # not enough values to unpack (COLOR_BOUNDARY_RE did not match)
        pass
    reset = f'\033[0m'
    ret = f'{start}{text}{reset}'
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
