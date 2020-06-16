import re
from typing import Union, List, Tuple, Set, Dict, Generator

from more_termcolor import convert, core

COLOR_CODES_RE = r'(\d{,3})(?:;)?' * 6
"""
first, *_ = re.finditer(COLOR_BOUNDARY_RE, '\x1b[31;1mFOO\x1b[0m')
first.group() → '\x1b[31;1m'
first.groups() → ('31', '1', '', '', '', '')
"""

COLOR_BOUNDARY_RE = re.compile(fr'\x1b\[{COLOR_CODES_RE}m')
# COLOR_BOUNDARY_RE2 = re.compile(fr'\x1b\[{COLOR_CODES_RE}m([^\x1b]+)*')
ON_COLOR_RE = re.compile(fr'on[_ ]({"|".join(core.COLORS)})')


class Color:
    code: str
    # name: str
    reset: str
    text_start_i: int  # the index where the color code started (where the first digit is is)
    text_end_i: int  # the index where the color code ended (where the last digit is + 1)
    is_non_foreground: bool
    
    def __init__(self, name_or_code: Union[str, int]):
        name = convert.to_color(name_or_code)
        self.reset = convert.to_reset_code(name)
        self.code = convert.to_code(name)
        self._is_non_foreground = None
    
    def __hash__(self) -> int:
        return hash(self.code)
    
    @property
    def is_non_foreground(self):
        if self._is_non_foreground is None:
            self._is_non_foreground = self.code not in core.FOREGROUND_CODES and self.code not in core.BRIGHT_FOREGROUND_CODES
        return self._is_non_foreground


class ColorScope:
    colors: List[Color]
    reset2color: Dict[str, Color]
    has_non_foreground: bool  # value is set in self.addcolor()
    
    def __init__(self, *names_or_codes: Union[str, int]):
        self.colors = []
        self._colors_set: Set[Color] = set()  # allows checking for duplicates in O(1) while keeping order
        self.reset2color: Dict[str, Color] = dict()
        self.has_non_foreground = None
        for name_or_code in names_or_codes:
            self.addcolor(name_or_code)
        
        if self.has_non_foreground is None:
            # self.has_non_foreground remained None,
            # because none of the colors was color.is_non_foreground == True
            self.has_non_foreground = False
    
    def __bool__(self):
        return bool(self.colors)
    
    def addcolor(self, name_or_code: Union[str, int]) -> Color:
        if name_or_code is None:
            return None
        
        color = Color(name_or_code)
        if color in self._colors_set:
            return None
        self._colors_set.add(color)
        self.reset2color[color.reset] = color
        self.colors.append(color)
        # check whether color.is_non_foreground only if needed
        if self.has_non_foreground is None and color.is_non_foreground:
            self.has_non_foreground = True
        
        return color
    
    def open(self):
        """
        >>> ColorScope('bold','red').open() == '\x1b[1;31m'
        """
        return convert.to_boundary(*map(lambda color: color.code, self.colors))
    
    def reset(self):
        """
        >>> ColorScope('bold','red').reset() == '\x1b[22;39m'
        """
        return convert.to_boundary(*map(lambda color: color.reset, self.colors))


class Inside(ColorScope):
    has_reset_all: bool = None
    
    def addcolor(self, name_or_code: Union[str, int], text_start_i: int, text_end_i: int) -> Color:
        color = super().addcolor(name_or_code)
        color.text_start_i = text_start_i  # by ref
        color.text_end_i = text_end_i
        if self.has_reset_all is None and color.code == '0':
            self.has_reset_all = True
        
        if self.has_reset_all is None:
            # self.has_reset_all remained None,
            # because none of the color codes was '0'
            self.has_reset_all = False
        return color
    
    @classmethod
    def from_text(cls, text: str):
        instance = cls()
        i = 0
        while True:
            try:
                char = text[i]
                
                if char == '\x1b':
                    j = i + 2  # skip [
                    # TODO: replace boundary_idx with list of chars, then join it instead of slice
                    # boundary_idx = j
                    code_digits = []
                    while True:
                        jchar = text[j]
                        if jchar.isdigit():
                            code_digits.append(jchar)
                        else:
                            # ; or m
                            
                            code = ''.join(code_digits)
                            instance.addcolor(code, i + 2, j)
                            if jchar == 'm':
                                i = j
                                break
                            # jchar is ';'
                            code_digits = []
                        j += 1
                i += 1
            except IndexError as e:
                return instance


def get_same_reset_color_pairs(outside: ColorScope, inside: Inside) -> List[Tuple[Color, Color]]:
    """[ ( out, in ), ( out, in ), ... ]"""
    # TODO: complexity
    pairs: List[Tuple[Color, Color]] = []
    for in_reset, in_color in inside.reset2color.items():
        out_color = outside.reset2color.get(in_reset)
        if out_color is not None:
            pairs.append((out_color, in_color))
    return pairs


def colored_(text: str, *colors: Union[str, int]) -> str:
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
    if not text:
        return ''
    text = str(text)
    outside = ColorScope(*colors)
    inside = Inside.from_text(text)
    
    if inside.has_non_foreground or outside.has_non_foreground:
        return f'{outside.open()}{text}{outside.reset()}'
    print(f'inside: {bool(inside)}',
          '\ninside.has_non_foreground ^ outside.has_non_foreground:', inside.has_non_foreground ^ outside.has_non_foreground,
          end='\n\n'
          )
    return f'{outside.open()}{text}{outside.reset()}'
    if not inside.has_non_foreground ^ outside.has_non_foreground:
        # either:
        # (a)
        # text had no colors, in which case,
        # just open and reset the given colors around it; or
        # (b)
        # text HAD some colors, but either:
        #   I. no background/formatting colors in either inside or outside, or
        #   II. both have background/formatting colors
        # which means the colors can live together peacefully,
        # and there's no need to alter the reset strings of the text.
        return f'{outside.open()}{text}{outside.reset()}'
    
    ## text includes some colors ##
    # TODO (performance): don't replace substrings if not needed
    # TODO: middle_already_formatted
    
    if inside.has_non_foreground:
        # replace existing inside reset codes with
        # the inside's colors' matching reset codes
        
        if outside.has_non_foreground:
            inner_reset_codes.extend(reopen_these_outer_open_codes)
        proper_inner_reset = convert.to_boundary(*inner_reset_codes)
        text = text.replace(inner_reset.group(), proper_inner_reset, 1)
    
    else:
        if outer_has_non_foreground:
            text = text.replace(inner_reset.group(), convert.to_boundary('reset fg'), 1)
        else:
            # replace inner reset with outer open
            text = text.replace(inner_reset.group(), start, 1)
    
    reset = convert.to_boundary(0)
    try:
        ret = f'{start}{text}{reset}'
    except UnboundLocalError as e:
        
        start = convert.to_boundary(*outer_open_codes)
        ret = f'{start}{text}{reset}'
    return ret


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
    if not text:
        return ''
    outside = ColorScope(*colors)
    text = str(text)
    inside = Inside.from_text(text)
    if not inside:
        outside_open = outside.open()
        outside_reset = outside.reset()
        return f'{outside_open}{text}{outside_reset}'
    
    # outer_open_codes = []
    # outer_reset_codes = []
    # outer_reset_2_open = dict()
    # outer_has_non_foreground = False
    # for color in filter(lambda c: c is not None, colors):
    #     # if on_color is None by default in cprint()
    #     open_code = convert.to_code(color)
    #     # TODO: complexity
    #     if open_code in outer_open_codes:
    #         continue
    #     outer_open_codes.append(open_code)
    #     reset_code = convert.to_reset_code(open_code)
    #     # TODO: this probably fails when open colors are bold,dark!
    #     outer_reset_2_open[reset_code] = open_code
    #     outer_reset_codes.append(reset_code)
    #     if not outer_has_non_foreground and _is_non_foreground(open_code):
    #         outer_has_non_foreground = True
    
    try:
        # TODO (performance): don't replace substrings if not needed
        # inner_open, *inner_middle_matches, inner_reset = re.finditer(COLOR_BOUNDARY_RE, text)
        
        # inner_open_codes = []
        # inner_has_non_foreground = False
        # inner_reset_codes = []
        # reopen_these_outer_open_codes = []
        same_reset_color_pairs = get_same_reset_color_pairs(outside, inside)
        if not same_reset_color_pairs:
            outside_open = outside.open()
            outside_reset = outside.reset()
            return f'{outside_open}{text}{outside_reset}'
        
        # for inner_open_code in inner_open.groups():
        #     # build:
        #     # (1) inner_open_codes
        #     # (2) inner_reset_codes
        #     # (3) reopen_these_outer_open_codes
        #     if not inner_open_code:
        #         continue
        #     inner_open_codes.append(inner_open_code)
        #     inner_reset_code = convert.to_reset_code(inner_open_code)
        #     inner_reset_codes.append(inner_reset_code)
        #     for outer_reset_code in outer_reset_codes:
        #         if inner_reset_code == outer_reset_code:
        #             inner_and_outer_share_reset_code = True
        #             outer_open_code = outer_reset_2_open[outer_reset_code]
        #             reopen_these_outer_open_codes.append(outer_open_code)
        #     if not inner_has_non_foreground and _is_non_foreground(inner_open_code):
        #         inner_has_non_foreground = True
        
        # start = convert.to_boundary(*outer_open_codes)
        rebuilt_chars = []
        i = 0
        for out_color, in_color in same_reset_color_pairs:
            while i < in_color.text_start_i:
                char = text[i]
                rebuilt_chars.append(char)
                i += 1
            rebuilt_chars.extend(out_color.code)
            i += in_color.text_end_i - in_color.text_start_i
        rebuilt_text = ''.join(rebuilt_chars) + text[i:]
        outside_open = outside.open()
        outside_reset = outside.reset()
        return f'{outside_open}{rebuilt_text}{outside_reset}'
        print(f'inner_has_non_foreground: ', inner_has_non_foreground,
              '\nouter_has_non_foreground: ', outer_has_non_foreground,
              f'\ninner_and_outer_share_reset_code:', inner_and_outer_share_reset_code,
              f'\ninner_reset.group(): {repr(inner_reset.group())}',
              )
        if inner_has_non_foreground:
            
            if outer_has_non_foreground:
                # replace existing inner reset codes with
                # the the outer open codes that have the same reset codes as
                # any of the inner open codes
                print(f'reopening outer: {reopen_these_outer_open_codes}\n')
                # boundary = convert.to_boundary(*reopen_these_outer_open_codes)
                # text = text.replace(inner_reset.group(), boundary, 1)
                inner_reset_codes.extend(reopen_these_outer_open_codes)
            else:
                print(f'just replacing inner reset with proper reset ({re.escape(convert.to_boundary(*inner_reset_codes))})\n')
            proper_inner_reset = convert.to_boundary(*inner_reset_codes)
            if inner_reset.group() != proper_inner_reset and not outer_has_non_foreground:
                print()
            text = text.replace(inner_reset.group(), proper_inner_reset, 1)
        
        else:
            if outer_has_non_foreground:
                print(f'replacing inner reset with general reset foreground (39)\n')
                text = text.replace(inner_reset.group(), convert.to_boundary('reset fg'), 1)
            else:
                # replace inner reset with outer open
                print(f'replacing inner reset with outer open ({re.escape(start)})\n')
                text = text.replace(inner_reset.group(), start, 1)
    except ValueError as e:
        # not enough values to unpack (COLOR_BOUNDARY_RE did not match)
        pass
    # reset = convert.to_boundary(0)
    reset = outside.reset()
    try:
        ret = f'{start}{text}{reset}'
    except UnboundLocalError as e:
        
        start = convert.to_boundary(*outer_open_codes)
        ret = f'{start}{text}{reset}'
    return ret


def cprint(text, color=None, on_color=None, attrs=(), *colors, **kwargs):
    """Print colorized text.
    
    Can be used instead of the original termcolor's cprint() and would work exactly the same,
    but also allows for passing any extra colors, or skipping the awkward signature altogether, e.g.:
    ::
        # old style
        cprint('Hello, World!', 'red', 'on_cyan', attrs=['reverse'])
        
        # is equivalent to:
        cprint('Hello, World!', 'red', 'on cyan', 'reverse')
    
    
    It accepts kw-arguments of print function.
    """
    if on_color:
        if on_color.startswith('on_'):
            on_color = f'on {on_color[3:]}'
        # match = ON_COLOR_RE.match(on_color)
        # if match:
        #     actual_color = match.groups()[0]
        #     on_color = f'on {actual_color}'
        else:
            colors += (on_color,)
    if isinstance(attrs, (str, int)):
        print((colored(text, color, on_color, attrs, *colors)), **kwargs)
    else:
        print((colored(text, color, on_color, *attrs, *colors)), **kwargs)


__all__ = [
    'colored',
    'cprint'
    ]
