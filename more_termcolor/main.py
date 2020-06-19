import re
from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Set, Dict, Generator, Deque
from ipdb import set_trace
import inspect
from collections import deque
from snoop import snoop

from more_termcolor import convert, core

COLOR_CODES_RE = r'(\d{,3})(?:;)?' * 6
"""
first, *_ = re.finditer(COLOR_BOUNDARY_RE, '\x1b[31;1mFOO\x1b[0m')
first.group() → '\x1b[31;1m'
first.groups() → ('31', '1', '', '', '', '')
"""

COLOR_BOUNDARY_RE = re.compile(fr'\x1b\[{COLOR_CODES_RE}m')
# COLOR_BOUNDARY_RE2 = re.compile(fr'\x1b\[{COLOR_CODES_RE}m([^\x1b]+)*')
# ON_COLOR_RE = re.compile(fr'on[_ ]({"|".join(core.COLORS)})')
SHORT_ID_RE = re.compile(r'(?<=0x[\w\d]{8})([\w\d]{4})')  # last 4 digits


class Color(ABC):
    code: str
    text_start_i: int  # the index where the color code started (where the first digit is is)
    text_end_i: int  # the index where the color code ended (where the last digit is + 1)
    
    @abstractmethod
    def __init__(self, code: str, name: str):
        self.code = code
        self.text_start_i = None
        self.text_end_i = None
        self._name = name  # for repr; DONT use for lookups
    
    # def __hash__(self) -> int:
    # frozen = frozenset(map(lambda x: x is not None, (self.text_end_i, self.text_start_i, self.code)))
    # return hash(frozen)
    
    @abstractmethod
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}: "{self.code}"/{self._name}'
    
    def _shortid(self) -> str:
        rpr = super().__repr__()
        return f'0x...{SHORT_ID_RE.search(rpr).group()}'
    
    def softeq(self, other: 'Color') -> bool:
        return self.code == other.code and self._name == other._name


class ColorOpener(Color):
    resetcode: str
    resetter: 'ColorResetter'
    
    def __init__(self, code: str, name: str, resetcode: str):
        super().__init__(code, name)
        self.resetcode = resetcode
        self.resetter = None
    
    def __repr__(self) -> str:
        superrepr = super().__repr__()
        shortid = self._shortid()
        if self.resetter:
            return f'{superrepr} (ColorResetter: "{self.resetter.code}" | {self.resetter._shortid()}) | {shortid}'
        else:
            return f'{superrepr} (resetcode="{self.resetcode}") | {shortid}'
    
    def softeq(self, other: 'Color') -> bool:
        supersofteq = super().softeq(other)
        if isinstance(other, ColorOpener):
            return supersofteq and self.resetcode == other.resetcode and self.resetter == other.resetter
        return supersofteq


class ColorResetter(Color):
    # opencode: str
    
    # open: ColorOpener
    
    def __init__(self, code: str, name: str):
        super().__init__(code, name)
        # self.opencode = None  # TODO: any use for this besides repr?
        # self.open = None
    
    def __repr__(self) -> str:
        superrepr = super().__repr__()
        shortid = self._shortid()
        return f'{superrepr} | {shortid}'
        # if self.open:
        #     return f'{superrepr} (ColorOpen: "{self.open.code}" | {self.open._shortid()}) | {shortid}'
        # else:
        #     return f'{superrepr} (opencode="{self.opencode}") | {shortid}'


# @snoop
def colorfactory(name_or_code: Union[str, int]) -> Union[ColorOpener, ColorResetter]:
    name = convert.to_color(name_or_code)
    code = convert.to_code(name)
    resetcode = convert.to_reset_code(name)
    if code == resetcode:
        return ColorResetter(code, name)
    else:
        return ColorOpener(code, name, resetcode)


class ColorScope:
    colors: List[ColorOpener]
    _colors_set: Set[ColorOpener]
    # _unreset_colors: Deque[ColorOpener]
    
    reset2color: Dict[str, ColorOpener]
    
    # has_non_foreground: bool  # value is set in self.addcolor()
    
    def __init__(self, *names_or_codes: Union[str, int]):
        self.colors = []
        self._colors_set = set()  # allows checking for duplicates in O(1) while keeping order
        self.reset2color = dict()
        # self.has_non_foreground = None
        for name_or_code in names_or_codes:
            self.addcolor(name_or_code)
        
        # if self.has_non_foreground is None:
        #     # self.has_non_foreground remained None,
        #     # because none of the colors was color.is_non_foreground == True
        #     self.has_non_foreground = False
    
    def __bool__(self):
        return bool(self.colors)
    
    def _shortid(self) -> str:
        rpr = super().__repr__()
        return f'0x...{SHORT_ID_RE.search(rpr).group()}'
    
    def __repr__(self) -> str:
        return f'ColorScope ({len(self.colors)} colors) | {self._shortid()}'
    
    def get_last_unreset_color(self, resetcode) -> ColorOpener:
        for c in reversed(self.colors):
            if c.resetcode == resetcode and c.resetter is None:
                return c
        # for err msg
        colors_len = len(self.colors)
        # color_openers = [c for c in self.colors if isinstance(c, ColorOpener)]
        # color_opener_count = len(color_openers)
        unreset_color_openers_count = len([c for c in self.colors if c.resetter is None])
        errmsg = [f"Failed finding a color with no reset whose resetcode == {resetcode}.",
                  f'colors_len: {colors_len}',
                  f'unreset_color_openers_count: {unreset_color_openers_count}'
                  ]
        raise ValueError('\n\t'.join(errmsg))
    
    def addcolor(self, name_or_code: Union[str, int]) -> ColorOpener:
        if name_or_code is None:
            return None
        color = colorfactory(name_or_code)
        
        if color in self._colors_set:  # TODO: does this ever happen? (hash)
            set_trace(inspect.currentframe(), context=30)
            return None
        if isinstance(color, ColorResetter):
            color_opener = self.get_last_unreset_color(color.code)
            color_opener.resetter = color
            # self._unreset_colors.remove(color_opener)
            # color.open = color_opener
        else:
            if color.resetter is not None:  # bug?
                set_trace(inspect.currentframe(), context=30)
            self._colors_set.add(color)
            # self._unreset_colors.append(color)
            self.colors.append(color)
        
        # if color.is_reset:
        #     print()
        # else:
        #     self.reset2color[color.resetcode] = color
        
        # # check whether color.is_non_foreground only if needed
        # if self.has_non_foreground is None and color.is_non_foreground:
        #     self.has_non_foreground = True
        
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
        return convert.to_boundary(*map(lambda color: color.resetcode, self.colors))


class Inside(ColorScope):
    # has_reset_all: bool = None
    
    def __repr__(self) -> str:
        shortid = super()._shortid()
        return f'Inside ({len(self.colors)} colors) | {shortid}'
    
    def addcolor(self, name_or_code: Union[str, int], text_start_i: int, text_end_i: int) -> ColorOpener:
        color = super().addcolor(name_or_code)
        color.text_start_i = text_start_i  # by ref
        color.text_end_i = text_end_i
        
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


def colors_with_same_reset_code(outside: ColorScope, inside: Inside) -> List[Tuple[ColorOpener, ColorOpener]]:
    """[ ( out, in ), ( out, in ), ... ]
    
    <bold> A [ <red;dark> B </fg;dark> ] C </bold>
    (bold, dark)
    <bold> A [ <red;dark> B </fg;dark><bold> ] C </bold>
    
    <bold> A <dark> B [ <red;dark> C </fg;dark> ] D </bold>
    (bold, dark)
    <bold> A <dark> B [ <red> C </fg> ] D </bold>
    
    <bold> A <green> B [ <red;dark> C </fg;dark> ] D </bold;fg>
    (green, red), (bold, dark)
    <bold> A <green> B [ <red;dark> C </dark><green;bold> ] D </bold;fg>
    
    <bold> A [ <red;bold> B </fg;bold> ] C </bold>
    (bold, bold)
    <bold> A [ <red> B </fg> ] C </bold>
    
    
    """
    # TODO: complexity
    pairs: List[Tuple[ColorOpener, ColorOpener]] = []
    matched = set()
    for inside_color in inside.colors:
        for outside_color in filter(lambda c: c not in matched, outside.colors):
            if outside_color.resetcode == inside_color.resetcode:
                pairs.append((outside_color, inside_color))
                matched.add(outside_color)
                break
    
    return pairs


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
        same_reset_color_pairs = colors_with_same_reset_code(outside, inside)
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
        rebuilt_chars = [*outside.open()]
        i = 0
        for out_color, in_color in same_reset_color_pairs:
            assert in_color.resetter is not None
            reset_inside_color = out_color.code in core.FORMATTING_CODES
            
            # Usually colors that share a reset code are incompatible;
            # for example, 'green', 'red' → both reset by '39', one cancels out the other.
            # That means we can skip resetting the inside color, and just re-open the outside color instead.
            # An exception is formatting colors, which are compatible:
            # something can be both 'bold' and 'dark', even though '22' resets them both.
            # In those cases, do reset the inside color, but re-open the outside code immediately after.
            
            while i < in_color.resetter.text_start_i:
                # until the boundary starts
                char = text[i]
                rebuilt_chars.append(char)
                i += 1
            if reset_inside_color:
                rebuilt_chars.extend(in_color.resetcode)
                rebuilt_chars.append(';')
            rebuilt_chars.extend(out_color.code)
            i += in_color.resetter.text_end_i - in_color.resetter.text_start_i
            rebuilt_chars.extend(text[i:] + f'\x1b[{out_color.resetcode}m')
        rebuilt_text = ''.join(rebuilt_chars)
        # outside_open = outside.open()
        # outside_reset = outside.reset()
        return rebuilt_text
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


__all__ = [
    'colored',
    'cprint'
    ]
