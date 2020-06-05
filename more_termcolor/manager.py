from dataclasses import dataclass, asdict
from pprint import pprint as pp

# ResetKey = Literal['normal', 'italic', 'underline', 'inverse', 'strike']

# https://docs.python.org/3/library/typing.html#typing.TypedDict
# class Point2D(TypedDict):  # this works with PyCharm
#     x: int
#     y: int
#     label: str


# Point2D = TypedDict('Point2D', dict(x=int, y=int, label=str)) # this misses bad types
# Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})  # this misses good types
# a: Point2D = {'x': 1, 'y': 2, 'label': 'hi'}  # OK


# b: Point2D = {'z': 3, 'label': 'bad'}  # NOT OK


# COLOR_CODES = ColorCodes()
from typing import TypedDict, Literal

# class Reset(TypedDict):
#     normal: Literal[0]
#     italic: Literal[23]
#     underline: Literal[24]
#     inverse: Literal[27]
#     strike: Literal[29]
#
#
# class SatBG(TypedDict):
#     faint: Literal[100]
#     red: Literal[101]
#     green: Literal[102]
#     yellow: Literal[103]
#     blue: Literal[104]
#     purple: Literal[105]
#     turquoise: Literal[106]
#     white: Literal[107]
#
#
# class Sat(TypedDict):
#     red: Literal[91]
#     green: Literal[92]
#     yellow: Literal[93]
#     blue: Literal[94]
#     purple: Literal[95]
#     turquoise: Literal[96]
#     white: Literal[97]
#     bg: SatBG
#
#
# class BG(TypedDict):
#     faint: Literal[40]
#     red: Literal[41]
#     green: Literal[42]
#     yellow: Literal[43]
#     blue: Literal[44]
#     purple: Literal[45]
#     turquoise: Literal[46]
#     white: Literal[47]
#
#
# class ColorCodes(TypedDict):
#     bold: Literal[1]
#     faint: Literal[2]
#     italic: Literal[3]
#     ul: Literal[4]
#     inverse: Literal[7]
#     strike: Literal[9]
#     reset: Reset
#     doubleul: Literal[21]
#     red: Literal[31]
#     green: Literal[32]
#     yellow: Literal[33]
#     blue: Literal[34]
#     purple: Literal[35]
#     turquoise: Literal[36]
#     white: Literal[37]
#     bg: BG
#     sat: Sat
#     darkgrey: Literal[90]

# TODO:
# @dataclass
# class Indexable:
#     def __getitem__(self, item):
#         t = asdict(self)
#         try:
#             return t[item]
#         except KeyError:
#             pp(t)
#             if item == 'normal':
#                 return 0
#
#
# @dataclass
# class Reset(Indexable):
#     normal = 0
#     italic = 23
#     underline = 24
#     inverse = 27
#     strike = 29
#
#
# @dataclass
# class SatBG(Indexable):
#     faint = 100
#     red = 101
#     green = 102
#     yellow = 103
#     blue = 104
#     purple = 105
#     turquoise = 106
#     white = 107
#
#
# @dataclass
# class Sat(Indexable):
#     bg: SatBG = SatBG()
#     red = 91
#     green = 92
#     yellow = 93
#     blue = 94
#     purple = 95
#     turquoise = 96
#     white = 97
#
#
# @dataclass
# class BG(Indexable):
#     faint = 40
#     red = 41
#     green = 42
#     yellow = 43
#     blue = 44
#     purple = 45
#     turquoise = 46
#     white = 47
#
#
# @dataclass
# class ColorCodes(Indexable):
#     bg: BG = BG()
#     sat: Sat = Sat()
#     reset: Reset = Reset()
#     bold = 1
#     faint = 2
#     italic = 3
#     ul = 4
#     inverse = 7
#     strike = 9
#     doubleul = 21
#     red = 31
#     green = 32
#     yellow = 33
#     blue = 34
#     purple = 35
#     turquoise = 36
#     white = 37
#     lightgrey = 90
# *** 8-bit (256 colors):
# * fg: 38:5:<c>m
# * bg: 48:5:<c>m
# 0-7 std equiv: 30–37
# 8-15 std equiv: 90–97
# 16-213 is 6x6 cube (216 colors)
# 232-255 is grayscale (24 steps)

# *** rgb ('true color'):
# * fg: 38;2;<r>;<g>;<b>m
# * bg: 38;2;<r>;<g>;<b>m

COLOR_CODES = dict(
        bold=1,
        faint=2,
        italic=3,
        ul=4,
        blink=5,
        fastblink=6,
        inverse=7,
        conceal=8,
        strike=9,
        default=10,
        # 16-231 → fg 38:5:<c>, bg 48:5:<c>
        fraktur=20,  # ?
        doubleul=21,
        reset=dict(all=0,
                   bold=22,
                   faint=22,
                   italic=23,
                   ul=24,
                   doubleul=24,
                   blink=25,
                   inverse=27,
                   conceal=28,
                   strike=29,
                   # 37 also resets non-sat colors (keeps sat)
                   fg=39,
                   bg=49,
                   frame=54,
                   circle=54,
                   ol=55,
                   ),
        black=30,
        red=31,
        green=32,
        yellow=33,
        blue=34,
        magenta=35,
        cyan=36,
        white=37,
        # 38;5 for 8bit, 38;2 for rgb
        bg=dict(black=40,
                red=41,
                green=42,
                yellow=43,
                blue=44,
                magenta=45,
                cyan=46,
                white=47,
                # 48;5 for 8bit, 48;2 for rgb
                ),
        frame=51,  # ?
        circle=52,  # ?
        ol=53,  # overline
        sat=dict(black=90,
                 red=91,
                 green=92,
                 yellow=93,
                 blue=94,
                 magenta=95,
                 cyan=96,
                 white=97,
                 bg=dict(black=100,
                         red=101,
                         green=102,
                         yellow=103,
                         blue=104,
                         magenta=105,
                         cyan=106,
                         white=107)
                 ),
        
        )
