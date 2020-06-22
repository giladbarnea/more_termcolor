import re
from abc import ABC, abstractmethod
from itertools import chain
from typing import Union, List, Tuple, Set, Dict, Generator, Deque, Optional, overload, Iterable, OrderedDict as TOrderedDict
from ipdb import set_trace
import inspect
from collections import deque, OrderedDict
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
    
    # start_idx: int  # the index where the color code started (where the first digit is is)
    # end_idx: int  # the index where the color code ended (where the last digit is + 1)
    
    def __init__(self, code: str):
        self.code = code
        # self.start_idx = None
        # self.end_idx = None
    
    # def __hash__(self) -> int:
    # frozen = frozenset(map(lambda x: x is not None, (self.end_idx, self.start_idx, self.code)))
    # return hash(frozen)
    
    @abstractmethod
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}: "{self.code}"/{convert.to_name(self.code)}'
    
    def _shortid(self) -> str:
        rpr = super().__repr__()
        return f'0x...{SHORT_ID_RE.search(rpr).group()}'
    
    def softeq(self, other: 'Color') -> bool:
        """Compares code"""
        return self.code == other.code


class ColorOpener(Color):
    resetcode: str
    resetter: 'ColorResetter'
    
    def __init__(self, code: str, resetcode: str):
        super().__init__(code)
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
        """Compares code (and resetcode if `other` is a ColorOpener)"""
        supersofteq = super().softeq(other)
        if not supersofteq:
            return False
        if isinstance(other, ColorOpener):
            return self.resetcode == other.resetcode
        return True


class ColorResetter(Color):
    cluster: 'Cluster'
    
    def __repr__(self) -> str:
        superrepr = super().__repr__()
        shortid = self._shortid()
        return f'{superrepr} | {shortid}'


TColor = Union[ColorOpener, ColorResetter]


def colorfactory(code: str) -> TColor:
    # name = convert.to_name(name_or_code)
    resetcode = convert.to_reset_code(code)
    if code == resetcode:
        return ColorResetter(code)
    else:
        return ColorOpener(code, resetcode)


class Cluster(List[Color]):
    start_idx: int  # where the \x1b char is
    end_idx: int  # where the m char is
    code2color: TOrderedDict[str, Color]
    openers: TOrderedDict[str, ColorOpener]  # key = code
    rogue_openers: TOrderedDict[str, ColorOpener]  # key = code
    rogue_resetters: TOrderedDict[str, ColorResetter]  # key = code
    matched_openers: TOrderedDict[str, ColorOpener]  # key = code
    matched_resetters: TOrderedDict[str, ColorResetter]  # key = code
    
    def __init__(self, *names_or_codes: Union[str, int], start_idx=None) -> None:
        super().__init__()
        self.start_idx = start_idx
        self.end_idx = None
        self.code2color = OrderedDict()
        self.openers = OrderedDict()
        self.rogue_openers = OrderedDict()
        self.rogue_resetters = OrderedDict()
        self.matched_openers = OrderedDict()
        self.matched_resetters = OrderedDict()
        for code in map(convert.to_code, filter(lambda x: x is not None, names_or_codes)):
            self.append(code)
    
    def __repr__(self) -> str:
        all_openers = True
        all_resetters = True
        for color in self:
            if isinstance(color, ColorOpener):
                all_resetters = False
            elif isinstance(color, ColorResetter):
                all_openers = False
        if all_openers:
            description = 'openers'
        elif all_resetters:
            description = 'resetters'
        else:
            description = 'mixed colors'
        return f'Cluster ({len(self)} {description}) i:{self.start_idx} | {str(id(self))[-4:]}'
    
    @classmethod
    def from_colors(cls, *colors: Color, trymatch=False) -> 'Cluster':
        """Does NOT convert `colors` to codes and builds new colors from them,
        but instead wraps `colors` by ref.
        Does not popuplate other self dicts besides `code2color`.
        """
        cluster = cls()
        for color in filter(lambda x: x is not None, colors):
            super(cls, cluster).append(color)
            cluster.code2color[color.code] = color
        return cluster
    
    def last_rogue_opener(self, by_resetcode: str) -> ColorOpener:
        for code, opener in reversed(self.rogue_openers.items()):
            assert opener.resetter is None
            if opener.resetcode == by_resetcode:
                return opener
        return None
    
    def first_rogue_resetter(self, by_resetcode: str) -> ColorResetter:
        for code, resetter in self.rogue_resetters.items():
            if resetter.code == by_resetcode:
                return resetter
        return None
    
    def _find_matching_resetter(self, opener: ColorOpener) -> ColorResetter:
        is_in_cluster = self.code2color.get(opener.code) == opener
        # checks if `color` belongs to this cluster
        # `match(color)` can be called externally with a foreign color
        if is_in_cluster:
            self.openers[opener.code] = opener
        matching_resetter = self.first_rogue_resetter(opener.resetcode)
        if matching_resetter is None:
            if is_in_cluster:
                self.rogue_openers[opener.code] = opener
            return None
        
        opener.resetter = matching_resetter
        del self.rogue_resetters[matching_resetter.code]
        self.matched_resetters[matching_resetter.code] = matching_resetter
        if is_in_cluster:
            del self.rogue_openers[opener.code]
            self.matched_openers[opener.code] = opener
        return matching_resetter
    
    def _find_matching_opener(self, resetter: ColorResetter) -> ColorOpener:
        
        is_in_cluster = self.code2color.get(resetter.code) == resetter
        # checks if `color` belongs to this cluster
        # `match(color)` can be called externally with a foreign color
        if is_in_cluster:
            resetter.cluster = self
        matching_opener = self.last_rogue_opener(resetter.code)
        if matching_opener is None:
            if is_in_cluster:
                self.rogue_resetters[resetter.code] = resetter
            return None
        
        matching_opener.resetter = resetter
        del self.rogue_openers[matching_opener.code]
        self.matched_openers[matching_opener.code] = matching_opener
        if is_in_cluster:
            del self.rogue_resetters[resetter.code]
            self.matched_resetters[resetter.code] = resetter
        return matching_opener
    
    @overload
    def match(self, color: ColorOpener) -> ColorResetter:
        ...
    
    @overload
    def match(self, color: ColorResetter) -> ColorOpener:
        ...
    
    def match(self, color):
        """Tries to find a matching Opener/Resetter to passed `color`, among this cluster's rogue colors.
        
        If found a match, sets `color.resetter` and returns the match.
        
        If no match is found, returns None.
        
        Updates `self.[rogue|matched]_` dicts as needed.
        
        Note: it's possible that `color` does not belong to this cluster."""
        
        if isinstance(color, ColorOpener):
            return self._find_matching_resetter(color)
        return self._find_matching_opener(color)
    
    @overload
    def append(self, code: str) -> Tuple[ColorOpener, ColorResetter]:
        ...
    
    @overload
    def append(self, code: str) -> Tuple[ColorResetter, ColorOpener]:
        ...
    
    def append(self, code):
        """Inits and appends color, updates `self.code2color`, tries to match it, sets `color.cluster=self` if Resetter, and returns (Color, match)"""
        if code is None:
            return None, None
        if code in self.code2color:
            return None, None
        color = colorfactory(code)
        super().append(color)
        self.code2color[color.code] = color
        if isinstance(color, ColorOpener):
            matching_resetter = self._find_matching_resetter(color)
            return color, matching_resetter
        else:
            # TODO: this may be redundant, because happens in _find_matching_opener()
            #  (and if so, just call self.match() instead of if/else)
            color.cluster = self
            matching_opener = self._find_matching_opener(color)
            return color, matching_opener
    
    def finalize(self):
        """Uses all colors (agnostic to color type)"""
        return f'\x1b[{";".join(map(lambda color: color.code, self))}m'
    
    def open(self):
        """Opener codes"""
        return f'\x1b[{";".join(self.openers)}m'
    
    def reset(self):
        """Opener RESET codes"""
        return f'\x1b[{";".join(map(lambda opener: opener.resetcode, self.openers.values()))}m'


class ColorScope(List[Cluster]):
    def __init__(self, *clusters: Cluster):
        
        super().__init__()
        if not clusters:
            return
        for cluster in clusters:
            self.append(cluster, trymatch=False)
    
    def __bool__(self):
        return any(bool(cluster) for cluster in self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__} ({len(self)} clusters) | {str(id(self))[-4:]}'
    
    def match(self, cluster: Cluster):
        """Tries to find all matches between all of this scope's Clusters."""
        for opencode, rogue_opener in cluster.rogue_openers.items():
            for other_cluster in self:
                matching_resetter = other_cluster.match(rogue_opener)
                if matching_resetter:
                    assert matching_resetter.cluster is other_cluster
                    # cluster.match(matching_resetter)
        for resetcode, rogue_resetter in cluster.rogue_resetters.items():
            assert rogue_resetter.cluster is cluster
            for other_cluster in self:
                matching_opener = other_cluster.match(rogue_resetter)
                assert matching_opener.resetter is rogue_resetter
                # if matching_opener:
                #     cluster.match(matching_opener)
    
    def append(self, cluster: Cluster, *, trymatch=True) -> None:
        if not cluster:
            return
        if trymatch:
            self.match(cluster)
        
        super().append(cluster)


class Inside(ColorScope):
    
    @classmethod
    def from_text(cls, text: str):
        inside = cls()
        i = 0
        while True:
            try:
                char = text[i]
                
                if char == '\x1b':
                    cluster = Cluster(start_idx=i)
                    j = i + 2  # skip [
                    
                    # boundary_idx = j
                    code_digits = []
                    while True:
                        jchar = text[j]
                        if jchar.isdigit():
                            code_digits.append(jchar)
                        else:
                            # ; or m
                            
                            code = ''.join(code_digits)
                            cluster.append(code)
                            if jchar == 'm':
                                i = j
                                inside.append(cluster)
                                cluster.end_idx = j
                                break
                            # jchar is ';'
                            code_digits = []
                        j += 1
                i += 1
            except IndexError as e:
                return inside


def openers_with_same_reset_code(outside: ColorScope, inside: Inside) -> List[Tuple[Tuple[ColorOpener, Cluster], Tuple[ColorOpener, Cluster]]]:
    """[ ( (out,cluster), (in,cluster) ), ( (out,cluster), (in,cluster) ), ... ]
    
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
    pairs: List[Tuple[Tuple[ColorOpener, Cluster], Tuple[ColorOpener, Cluster]]] = []
    inside_resetcodes = dict()
    for inside_cluster in inside:
        for code, inside_opener in inside_cluster.openers.items():
            inside_resetcodes[inside_opener.resetcode] = (inside_opener, inside_cluster)
    
    for outside_cluster in outside:
        for code, outside_opener in outside_cluster.openers.items():
            inside_opener2cluster = inside_resetcodes.get(outside_opener.resetcode)
            if inside_opener2cluster is not None:
                pairs.append(((outside_opener, outside_cluster), inside_opener2cluster))
    
    return pairs


def colored(text: str, *colors: Union[str, int], **kwargs) -> str:
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
    
    outside = ColorScope(Cluster(*colors))
    text = str(text)
    inside = Inside.from_text(text)
    if not inside:
        outside_open = outside[0].open()
        outside_reset = outside[0].reset()
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
        openers_with_same_reset = openers_with_same_reset_code(outside, inside)
        if not openers_with_same_reset:
            outside_open = outside[0].open()
            outside_reset = outside[0].reset()
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
        # TODO: consider storing strings, not chars
        rebuilt_chars = [outside[0].open()]
        i = 0
        for (outside_opener, outside_cluster), (inside_opener, inside_cluster) in openers_with_same_reset:
            assert inside_opener.resetter is not None
            reset_inside_color = outside_opener.code in core.FORMATTING_CODES
            
            # Usually colors that share a reset code are incompatible;
            # for example, 'green', 'red' → both reset by '39', one cancels out the other.
            # That means we can skip resetting the inside color, and just re-open the outside color instead.
            # An exception is formatting colors, which are compatible:
            # something can be both 'bold' and 'dark', even though '22' resets them both.
            # In those cases, do reset the inside color, but re-open the outside code immediately after.
            # TODO: cluster start_idx instead of color start idx
            rebuilt_chars.append(text[i:inside_opener.resetter.cluster.start_idx])
            # while i < inside_cluster.start_idx:
            #     # until the boundary starts
            #     char = text[i]
            #     rebuilt_chars.append(char)
            #     i += 1
            if reset_inside_color:
                hybrid_cluster = Cluster.from_colors(inside_opener.resetter, outside_opener)
                rebuilt_chars.extend(hybrid_cluster.finalize())
            else:
                rebuilt_chars.extend(outside_cluster.open())
            rebuilt_chars.extend(text[inside_opener.resetter.cluster.end_idx + 1:])
            rebuilt_chars.extend(outside_cluster.reset())
        
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


__all__ = [
    'colored',
    'cprint'
    ]
