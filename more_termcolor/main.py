import re
from abc import ABC, abstractmethod
from collections import OrderedDict
from contextlib import suppress
from typing import Union, List, Tuple, overload, OrderedDict as TOrderedDict, Iterator, Dict

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
    cluster: 'OpenCluster'
    
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
    """A list of colors which represents the str content beginning with '\x1b[' and ending with 'm' (i.e. 'cluster').
    Holds:
    
    - `OpenCluster`'s bounding indices;
    - `code2color` dict for containment evaluation in O(1);
    - `openers` dict that holds only ColorOpeners;
    - `rogue_openers` and `rogue_resetters` - colors whose match wasn't found yet
    """
    start_idx: int  # where the \x1b char is
    end_idx: int  # where the m char is
    code2color: Dict[str, Color]
    openers: TOrderedDict[str, ColorOpener]  # key = code
    rogue_openers: TOrderedDict[str, ColorOpener]
    rogue_resetters: TOrderedDict[str, ColorResetter]
    
    def __init__(self, *names_or_codes: Union[str, int], start_idx=None) -> None:
        super().__init__()
        self.start_idx = start_idx
        self.end_idx = None
        self.code2color = dict()
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
        return f'OpenCluster ({len(self)} {description}) [{self.start_idx}:{self.end_idx}] | {str(id(self))[-4:]}'
    
    # @classmethod
    # def from_colors(cls, *colors: Color, trymatch=False) -> 'OpenCluster':
    #     """Does NOT convert `colors` to codes and builds new colors from them,
    #     but instead wraps `colors` by ref.
    #     Does not popuplate other self dicts besides `code2color`.
    #     """
    #     cluster = cls()
    #     for color in filter(lambda x: x is not None, colors):
    #         super(cls, cluster).append(color)
    #         cluster.code2color[color.code] = color
    #     return cluster
    
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
                # Can happen when appending a color (or is it a bug?)
                del self.rogue_openers[opener.code]
        else:
            del opener.cluster.rogue_openers[opener.code]
        return matching_resetter
    
    def _find_matching_opener(self, resetter: ColorResetter) -> ColorOpener:
        is_in_cluster = self.code2color.get(resetter.code) == resetter
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
                # Can happen when appending a color (or is it a bug?)
                del self.rogue_resetters[resetter.code]
        else:
            del resetter.cluster.rogue_resetters[resetter.code]
        return matching_opener
    
    @overload
    def match(self, color: ColorOpener) -> ColorResetter:
        ...
    
    @overload
    def match(self, color: ColorResetter) -> ColorOpener:
        ...
    
    def match(self, color):
        """- Tries to find an internal matching Opener/Resetter to passed `color` (and set `color.resetter`);
        - Sets `color.cluster` to `self` if indeed `color` belongs to this cluster;
        - Updates `self.openers` and `self.rogue_` dicts as needed
        - Returns `match` if found, else `None`"""
        
        if isinstance(color, ColorOpener):
            return self._find_matching_resetter(color)
        return self._find_matching_opener(color)
    
    def append(self, code_or_color: Union[str, TColor], *, trymatch: bool = True) -> Tuple[TColor, TColor]:
        """- Constructs a `color` from `code` if needed
        - Appends `color` to `self`
        - Updates `self.code2color`
        - Tries to match `color` internally
        - Returns `(color, match)`"""
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
        if trymatch:
            match = self.match(color)
        else:
            match = None
        return color, match
    
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
    
    def unique_opener_resetcodes(self) -> List[str]:
        if not self.openers:
            return []
        resetcodes = []
        resetcodes_set = set()
        for resetcode in map(lambda opener: opener.resetcode, self.openers.values()):
            if resetcode in resetcodes_set:
                continue
            resetcodes_set.add(resetcode)
            resetcodes.append(resetcode)
        return resetcodes
    
    def finalize(self) -> str:
        # TODO: this can return with duplicates?
        """Uses all colors (agnostic to color type)"""
        if not self:
            return ''
        return f'\x1b[{";".join(self.codes())}m'
    
    def open(self) -> str:
        """Opener codes"""
        if not self.openers:
            return ''
        return f'\x1b[{";".join(self.openers)}m'
    
    def reset(self) -> str:
        """OPENER reset codes"""
        unique_opener_resetcodes = self.unique_opener_resetcodes()
        if not unique_opener_resetcodes:
            return ''
        return f'\x1b[{";".join(unique_opener_resetcodes)}m'


class OpenCluster(Cluster):
    resetter: Cluster
    
    def __init__(self, *names_or_codes: Union[str, int], start_idx=None) -> None:
        super().__init__(*names_or_codes, start_idx=start_idx)
        self.resetter = Cluster()


class ColorScope(List[OpenCluster]):
    def __init__(self, text: str):
        super().__init__()
        clusters = self.clusters_from_text(text)
        for cluster in clusters:
            print(f'{repr(self)} appending {repr(cluster)}')
            self.append(cluster)
    
    def __bool__(self):
        return any(bool(cluster) for cluster in self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__} ({len(self)} clusters) | {str(id(self))[-4:]}'
    
    @staticmethod
    def clusters_from_text(text: str) -> List[OpenCluster]:
        # TODO:
        #  1) test if faster with for loop
        #  2) handle broken clusters ('\x1b1mTEXT', '\x1b[1TEXT', ...)
        #  3) explore the possibility to represent resetters' cluster as a prop of OpenCluster, and not as a sep cluster
        open_clusters = []
        i = 0
        while True:
            try:
                char = text[i]
                
                if char == '\x1b':
                    open_cluster = OpenCluster(start_idx=i)
                    j = i + 2  # skip [
                    
                    code_digits = []
                    while True:
                        jchar = text[j]
                        if jchar.isdigit():
                            code_digits.append(jchar)
                        else:
                            # ; or m
                            
                            code = ''.join(code_digits)
                            open_cluster.append(code)
                            if jchar == 'm':
                                i = j
                                open_clusters.append(open_cluster)
                                open_cluster.end_idx = j
                                break
                            # jchar is ';'
                            code_digits = []
                        j += 1
                i += 1
            except IndexError as e:
                return open_clusters
    
    def match(self, cluster: OpenCluster):
        """Tries to find all matches between all of this scope's OpenClusters."""
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
                if matching_opener:
                    assert matching_opener.resetter is rogue_resetter
                    assert matching_opener.cluster is other_cluster
                
                # if matching_opener:
                #     cluster.match(matching_opener)
    
    def append(self, cluster: OpenCluster, *, trymatch=True) -> None:
        if not cluster:
            return
        if trymatch:
            self.match(cluster)
        
        super().append(cluster)
    
    def make_self_transparent_to(self, surrounding_cluster: OpenCluster):
        """Modifies `self` such that:
         
         - The colors of the `surrounding_cluster` will be in effect after this scope's end
         - The colors of the `surrounding_cluster` will add-up to this scope's colors as much as possible
         
         Formatting-colors can add-up to each other, so if the `surrounding cluster` contains `italic`,
         and this scope contains `bold` - the text inside this scope will be both `italic` and `bold`,
         but any text beyond this scope (and within the `surrounding cluster`) will remain only `italic`.
         
         In case this scope contains colors that cancel-out `surrounding_cluster`'s colors,
         (e.g. `surrounding` is `green` and `self` is `red`), this scope's colors are eventually reset and
         `surrounding_cluster`'s colors are re-opened.
         """
        # TODO:
        #  1) complexity
        #  2) modify all self clusters
        inside_cluster = self[0]
        inside_1_cluster = self[1]
        if inside_cluster.start_idx == 0:
            # there's no text before inside_cluster → merge color openers
            for inside_opener in list(inside_cluster.openers.values()):
                surrounding_cluster.append(inside_opener)
                inside_cluster.remove(inside_opener)
        
        # remove redundant inside colors (already opened from the outside)
        for inside_opener in list(inside_cluster.openers.values()):
            for outside_opener in surrounding_cluster.openers.values():
                # both fg / bg / formatting
                if inside_opener.code == outside_opener.code:
                    inside_resetter_cluster = inside_opener.resetter.cluster
                    # same exact color
                    # remove.append(inside_opener)
                    inside_cluster.remove(inside_opener)
                    inside_resetter_cluster.remove(inside_opener.resetter)
        
        # then either swap between inside reset color and outside open color if fg/bg
        # or just append outside open color if formatting
        for inside_opener in inside_cluster.openers.values():
            for outside_opener in surrounding_cluster.openers.values():
                if inside_opener.resetcode == outside_opener.resetcode:
                    # print(f'\ninside_opener: ', inside_opener,
                    #       '\noutside_opener: ', outside_opener,
                    #       '\ninside_opener.resetter: ', inside_opener.resetter)
                    # both fg / bg / formatting
                    inside_resetter_cluster = inside_opener.resetter.cluster
                    if inside_opener.code in core.FORMATTING_CODES:
                        # neccessarily: outside_opener.code in core.FORMATTING_CODES as well
                        # print('formatting; appending outside_opener to inside_resetter_cluster')
                        inside_resetter_cluster.append(outside_opener)
                    else:
                        # print('incompat; replacing inside_opener.resetter with outside_opener')
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
    outside_cluster = OpenCluster(*colors)
    text = str(text)
    inside = ColorScope(text)
    if not inside:
        outside_open = outside_cluster.open()
        outside_reset = outside_cluster.reset()
        return f'{outside_open}{text}{outside_reset}'
    
    inside.make_self_transparent_to(outside_cluster)
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
