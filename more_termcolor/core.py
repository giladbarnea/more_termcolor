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
    'dark',  # 2 (brighter than brightblack 90)
    'italic',  # 3,
    'ul',  # 4,
    'underline',  # termcolor compat
    'blink',  # 5,
    'fastblink',  # 6,
    'reverse',  # 7,
    'conceal',  # 8,
    'concealed',  # termcolor compat
    'strike',  # 9,
    # 'default',  # 10,
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
    # '10',
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
                         fg='39',  # resets standard and bright
                         on='49',
                         frame='54',
                         circle='54',
                         ol='55',
                         overline='55',
                         )
COLORS = (
    'black',
    'grey',  # termcolor compat
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    )
FOREGROUND_CODES = (
    '30',  # black
    '30',  # grey # termcolor compat
    '31',  # red
    '32',  # green
    '33',  # yellow
    '34',  # blue
    '35',  # magenta
    '36',  # cyan
    '37',  # white
    # 38;5 for 8bit, 38;2 for rgb
    )
FOREGROUND_COLOR_CODES = dict(zip(COLORS, FOREGROUND_CODES))
BRIGHT_BACKGROUND_CODES = (
    '100',  # black
    '100',  # grey # termcolor compat
    '101',  # red
    '102',  # green
    '103',  # yellow
    '104',  # blue
    '105',  # magenta
    '106',  # cyan
    '107',  # white
    )
BRIGHT_BACKGROUND_COLOR_CODES = dict(zip(COLORS, BRIGHT_BACKGROUND_CODES))
STANDARD_BACKGROUND_CODES = (
    '40',  # black
    '40',  # grey # termcolor compat
    '41',  # red
    '42',  # green
    '43',  # yellow
    '44',  # blue
    '45',  # magenta
    '46',  # cyan
    '47',  # white
    # 48;5 for 8bit, 48;2 for rgb
    )
STANDARD_BACKGROUND_COLOR_CODES = dict(zip(COLORS, STANDARD_BACKGROUND_CODES))
BACKGROUND_COLOR_CODES = dict(**STANDARD_BACKGROUND_COLOR_CODES,
                              bright=BRIGHT_BACKGROUND_COLOR_CODES,
                              )
BRIGHT_FOREGROUND_CODES = (
    '90',  # black
    '90',  # grey # termcolor compat
    '91',  # red
    '92',  # green
    '93',  # yellow
    '94',  # blue
    '95',  # magenta
    '96',  # cyan
    '97',  # white
    )
BRIGHT_FOREGROUND_COLOR_CODES = dict(zip(COLORS, BRIGHT_FOREGROUND_CODES))

COLOR_CODES = dict(
        **FORMATTING_COLOR_CODES,  # 1:10, 20, 21, 51:53
        reset=RESET_COLOR_CODES,  # 0, 22:29, 39, 49, 54, 55
        **FOREGROUND_COLOR_CODES,  # 30-37
        on=BACKGROUND_COLOR_CODES,  # 40:47, 100:107
        bright=BRIGHT_FOREGROUND_COLOR_CODES,  # 90:97
        )
