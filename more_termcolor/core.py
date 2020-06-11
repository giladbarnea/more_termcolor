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

FORMATTING_COLORS = (
    'bold',  # 1,
    'dark',  # 2 (aka 'grey'; brighter than satblack 90)
    'italic',  # 3,
    'ul',  # 4,
    'underline',  # termcolor compat
    'blink',  # 5,
    'fastblink',  # 6,
    'reverse',  # 7,
    'conceal',  # 8,
    'concealed',  # termcolor compat
    'strike',  # 9,
    'default',  # 10,
    'fraktur',  # 20 ?
    'doubleul',  # 21,
    'frame',  # 51, ?
    'circle',  # 52, ?
    'ol',  # 53 (overline)
    'overline',  # 53
    )
FORMATTING_CODES = (
    '1',
    '2',
    '3',
    '4',
    '4',  # termcolor compat
    '5',
    '6',
    '7',
    '8',
    '8',  # termcolor compat
    '9',
    '10',
    # 16-231 → fg 38:5:<c>, bg 48:5:<c>
    '20',
    '21',
    '51',
    '52',
    '53',
    '53',
    )
FORMATTING_COLOR_CODES = dict(zip(FORMATTING_COLORS, FORMATTING_CODES))
RESET_COLOR_CODES = dict(all='0',
                         bold='22',
                         dark='22',
                         italic='23',
                         ul='24',
                         underline='24',  # termcolor compat
                         doubleul='24',
                         blink='25',
                         fastblink='25',
                         reverse='27',
                         conceal='28',
                         concealed='28',  # termcolor compat
                         strike='29',
                         fg='39',  # resets std and sat
                         on='49',
                         frame='54',
                         circle='54',
                         ol='55',
                         overline='55',
                         )
FG_COLORS = (
    'black',  # 30
    'red',  # 31
    'green',  # 32
    'yellow',  # 33
    'blue',  # 34
    'magenta',  # 35
    'cyan',  # 36
    'white',  # 37
    )
FG_CODES = (
    '30',
    '31',
    '32',
    '33',
    '34',
    '35',
    '36',
    '37',
    )
FG_COLOR_CODES = dict(zip(FG_COLORS, FG_CODES))
SAT_BG_COLOR_CODES = dict(black='100',
                          red='101',
                          green='102',
                          yellow='103',
                          blue='104',
                          magenta='105',
                          cyan='106',
                          white='107')
STD_BG_COLOR_CODES = dict(black='40',
                          red='41',
                          green='42',
                          yellow='43',
                          blue='44',
                          magenta='45',
                          cyan='46',
                          white='47')
BG_COLOR_CODES = dict(**STD_BG_COLOR_CODES,
                      sat=SAT_BG_COLOR_CODES
                      # 48;5 for 8bit, 48;2 for rgb
                      )

SAT_FG_COLOR_CODES = dict(black='90',  # aka 'lightgrey'; dimmer than dark 2
                          red='91',
                          green='92',
                          yellow='93',
                          blue='94',
                          magenta='95',
                          cyan='96',
                          white='97'  # aka 'white'
                          )
# SAT_FG_COLOR_CODES = dict(**SAT_FG_COLOR_CODES,
#                        on=SAT_BG_COLOR_CODES)
COLOR_CODES = dict(
        **FORMATTING_COLOR_CODES,  # 1:10, 20, 21, 51:53
        reset=RESET_COLOR_CODES,  # 0, 22:29, 39, 49, 54, 55
        **FG_COLOR_CODES,  # 30-37
        # 38;5 for 8bit, 38;2 for rgb
        on=BG_COLOR_CODES,  # 40:47, 100:107
        sat=SAT_FG_COLOR_CODES,  # 90:97
        )
