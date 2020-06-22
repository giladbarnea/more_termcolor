import re
from abc import ABC, abstractmethod
from collections import OrderedDict
from contextlib import suppress
from typing import Union, List, Tuple, overload, OrderedDict as TOrderedDict, Iterator

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
    cluster: 'Cluster'
    
    def __init__(self, code: str):
        self.code = code
        self.cluster = None
    
    # def __hash__(self) -> int:
    # frozen = frozenset(map(lambda x: x is not None, (self.end_idx, self.start_idx, self.code)))
    # return hash(frozen)
    
    @abstractmethod
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}: "{self.code}"/{convert.to_name(self.code)}'
    
    def _shortid(self) -> str:
        rpr = super().__repr__()
        return f'{SHORT_ID_RE.search(rpr).group()}'
    
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
    
    def compatwith(self, other: 'ColorOpener') -> bool:
        """If two colors are compatible, opening them consecutively doesn't cancel out the first"""
        if self.code in core.FORMATTING_CODES or other.code in core.FORMATTING_CODES:
            # formatting colors are compatible with all other colors (including formatting)
            return True
        return self.resetcode != other.resetcode


class ColorResetter(Color):
    
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
    rogue_openers: TOrderedDict[str, ColorOpener]
    rogue_resetters: TOrderedDict[str, ColorResetter]
    
    def __init__(self, *names_or_codes: Union[str, int], start_idx=None) -> None:
        super().__init__()
        self.start_idx = start_idx
        self.end_idx = None
        self.code2color = OrderedDict()
        self.openers = OrderedDict()
        self.rogue_openers = OrderedDict()
        self.rogue_resetters = OrderedDict()
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
        return f'Cluster ({len(self)} {description}) [{self.start_idx}:{self.end_idx}] | {str(id(self))[-4:]}'
    
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
            opener.cluster = self
            self.openers[opener.code] = opener
        matching_resetter = self.first_rogue_resetter(opener.resetcode)
        if matching_resetter is None:
            if is_in_cluster:
                self.rogue_openers[opener.code] = opener
            return None
        
        opener.resetter = matching_resetter
        del self.rogue_resetters[matching_resetter.code]
        if is_in_cluster:
            with suppress(KeyError):
                # Can happen when appending a color
                del self.rogue_openers[opener.code]
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
        if is_in_cluster:
            with suppress(KeyError):
                # Can happen when appending a color
                del self.rogue_resetters[resetter.code]
        
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
    def append(self, code_or_color: Union[str, Color]) -> Tuple[ColorOpener, ColorResetter]:
        ...
    
    @overload
    def append(self, code_or_color: Union[str, Color]) -> Tuple[ColorResetter, ColorOpener]:
        ...
    
    def append(self, code_or_color):
        """Inits and appends color, updates `self.code2color`, tries to match it, sets `color.cluster=self` if Resetter, and returns (Color, match)"""
        if code_or_color is None:
            return None, None
        is_color = isinstance(code_or_color, Color)
        if is_color:
            if code_or_color.code in self.code2color:
                return None, None
        elif code_or_color in self.code2color:
            return None, None
        if is_color:
            color = code_or_color
        else:
            color = colorfactory(code_or_color)
        super().append(color)
        self.code2color[color.code] = color
        return color, self.match(color)
    
    def remove(self, color: TColor) -> None:
        # NOTE: this doesn't nullify start_idx and end_idx (colored() assumes that it doesn't)
        super().remove(color)
        del self.code2color[color.code]
        color.cluster = None
        if isinstance(color, ColorOpener):
            # might be a resetter
            del self.openers[color.code]
            with suppress(KeyError):
                del self.rogue_openers[color.code]
        else:
            with suppress(KeyError):
                del self.rogue_resetters[color.code]
    
    def codes(self) -> Iterator[str]:
        # TODO: this can return with duplicates?
        return map(lambda color: color.code, self)
    
    def unique_opener_resetcodes(self):
        resetcodes = []
        resetcodes_set = set()
        for resetcode in map(lambda opener: opener.resetcode, self.openers.values()):
            if resetcode in resetcodes_set:
                continue
            resetcodes_set.add(resetcode)
            resetcodes.append(resetcode)
        return resetcodes
    
    def finalize(self):
        # TODO: this can return with duplicates?
        """Uses all colors (agnostic to color type)"""
        return f'\x1b[{";".join(self.codes())}m'
    
    def open(self):
        """Opener codes"""
        return f'\x1b[{";".join(self.openers)}m'
    
    def reset(self):
        """OPENER reset codes"""
        unique_opener_resetcodes = self.unique_opener_resetcodes()
        return f'\x1b[{";".join(unique_opener_resetcodes)}m'


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
    
    def match(self, cluster: Cluster):
        """Tries to find all matches between all of this scope's Clusters."""
        for opencode, rogue_opener in cluster.rogue_openers.items():
            assert rogue_opener.cluster is cluster
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
                assert matching_opener.cluster is other_cluster
                
                # if matching_opener:
                #     cluster.match(matching_opener)
    
    def append(self, cluster: Cluster, *, trymatch=True) -> None:
        if not cluster:
            return
        if trymatch:
            self.match(cluster)
        
        super().append(cluster)


def openers_with_same_reset_code(outside_cluster: Cluster, inside: ColorScope) -> List[Tuple[ColorOpener, ColorOpener]]:
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
    inside_openers = dict()
    for inside_cluster in inside:
        for code, inside_opener in inside_cluster.openers.items():
            inside_openers[inside_opener.resetcode] = inside_opener
    paired_inside_openers = set()
    for code, outside_opener in outside_cluster.openers.items():
        inside_opener = inside_openers.get(outside_opener.resetcode)
        if inside_opener is not None and inside_opener not in paired_inside_openers:
            pairs.append((outside_opener, inside_opener))
            paired_inside_openers.add(inside_opener)
    
    return pairs


def foo(outside_cluster: Cluster, inside_cluster: Cluster):
    remove = []
    # first remove redundant inside colors (already opened from the outside)
    for inside_opener in inside_cluster.openers.values():
        for outside_opener in outside_cluster.openers.values():
            if inside_opener.resetcode == outside_opener.resetcode:
                # both fg / bg / formatting
                if inside_opener.code == outside_opener.code:
                    inside_resetter_cluster = inside_opener.resetter.cluster
                    # same exact color
                    remove.append(inside_opener)
                    inside_resetter_cluster.remove(inside_opener.resetter)
    for inside_opener in remove:
        inside_cluster.remove(inside_opener)
    
    # then either swap between inside reset color and outside open color if fg/bg
    # or just append outside open color if formatting
    for inside_opener in inside_cluster.openers.values():
        for outside_opener in outside_cluster.openers.values():
            if inside_opener.resetcode == outside_opener.resetcode:
                print(f'\ninside_opener: ', inside_opener,
                      '\noutside_opener: ', outside_opener,
                      '\ninside_opener.resetter: ', inside_opener.resetter)
                # both fg / bg / formatting
                inside_resetter_cluster = inside_opener.resetter.cluster
                if inside_opener.code in core.FORMATTING_CODES:
                    print('formatting; appending outside_opener to inside_resetter_cluster')
                    # neccessarily also outside_opener.code in core.FORMATTING_CODES
                    inside_resetter_cluster.append(outside_opener)
                else:
                    print('incompat; replacing inside_opener.resetter with outside_opener')
                    inside_resetter_cluster.remove(inside_opener.resetter)
                    inside_resetter_cluster.append(outside_opener)


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
    outside_cluster = Cluster(*colors)
    text = str(text)
    # TODO: from_text is the only ctor used
    inside = ColorScope.from_text(text)
    if not inside:
        outside_open = outside_cluster.open()
        outside_reset = outside_cluster.reset()
        return f'{outside_open}{text}{outside_reset}'
    
    # TODO (performance): don't replace substrings if not needed
    openers_with_same_reset = openers_with_same_reset_code(outside_cluster, inside)
    if not openers_with_same_reset:
        outside_open = outside_cluster.open()
        outside_reset = outside_cluster.reset()
        return f'{outside_open}{text}{outside_reset}'
    
    foo(outside_cluster, inside[0])
    rebuilt_chars = [outside_cluster.open(),
                     text[:inside[0].start_idx],
                     inside[0].open(),
                     text[inside[0].end_idx + 1:inside[1].start_idx],
                     inside[1].finalize(),
                     text[inside[1].end_idx + 1:],
                     outside_cluster.reset()
                     ]
    rebuilt_text = ''.join(rebuilt_chars)
    return rebuilt_text
    i = 0
    # rebuilt_chars.append(text[:inside[0].start_idx])
    for outside_opener, inside_opener in openers_with_same_reset:
        assert inside_opener.resetter is not None
        # Resetting the inside when it shares reset codes with outside:
        # Usually this is easy, because colors that share a reset code are incompatible;
        # for example, 'green', 'red' are both reset by '39', and one cancels out the other.
        # That means we can skip resetting the inside color altogether, and just re-open the outside color instead.
        # A problem arises with formatting colors, which ARE compatible:
        # something can be both 'bold' and 'dark', even though '22' resets them both.
        # In those cases, do reset the inside color, but re-open the outside code immediately after.
        inside_cluster = inside_opener.cluster
        reset_inside_color = outside_opener.code in core.FORMATTING_CODES
        # TODO: complexity
        is_inside_opener_redundant = any(inside_opener.softeq(color) for color in outside_cluster)
        if is_inside_opener_redundant:
            # Opening the inside when it shares opening codes with outside:
            # inside_opener and outside_opener represent the same exact color;
            # this means outside already opened for inside, and inside opener isn't needed.
            
            rebuilt_chars.append(text[i:inside_cluster.start_idx])  # outside's wrapped text, no colors.
            inside_cluster.remove(inside_opener)  # because already opened outside
            rebuilt_chars.append(inside_cluster.open())  # trimmed
            
            # inside's wrapped text, no colors. NOTE: assumes end_idx doesn't change in cluster.remove()
            rebuilt_chars.append(text[inside_cluster.end_idx + 1:inside_opener.resetter.cluster.start_idx])
        else:
            rebuilt_chars.append(text[i:inside_opener.resetter.cluster.start_idx])
        
        if reset_inside_color:
            # TODO: just map when done debugging
            inside_resetters = list(map(lambda opener: opener.resetter, inside_cluster.openers.values()))
            if is_inside_opener_redundant:
                # If there was no redundancy, we would've reset inside_opener by now,
                # which would mean re-opening the outside (because same reset codes for in/out).
                # But the redundant inside color was removed, which means it hadn't been reset,
                # which means there's no need to re-open the outside.
                hybrid_cluster = Cluster.from_colors(*inside_resetters)
            else:
                hybrid_cluster = Cluster.from_colors(*inside_resetters, outside_opener)
            rebuilt_chars.extend(hybrid_cluster.finalize())
        else:
            rebuilt_chars.extend(outside_cluster.open())
        rebuilt_chars.extend(text[inside_opener.resetter.cluster.end_idx + 1:])
        rebuilt_chars.extend(outside_cluster.reset())
    
    rebuilt_text = ''.join(rebuilt_chars)
    return rebuilt_text


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
