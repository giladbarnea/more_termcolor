"""This module does not assert anything programmatically. It just prints and describes what you're supposed to see with your eyes."""
from more_termcolor import COLOR_CODES
from more_termcolor.paint import paint


def test__standard_foreground_colors__sanity():
    print(paint('\nforeground colors: sanity', 'bold', 'sat white', 'ul'))
    for color, kode in COLOR_CODES.items():
        if isinstance(kode, dict):
            continue  # skip 'bg', 'sat'
        print(f'\n{color} ({kode})',
              f'\033[{kode}m{color}\033[0m',
              sep='\n', end='\n')


def test__standard_background_colors__sanity():
    print(paint('\nbackground colors: sanity', 'bold', 'sat white', 'ul'))
    for color, kode in COLOR_CODES['bg'].items():
        print(f'\n{color} ({kode})',
              f'\033[{kode}m{color}\033[0m',
              sep='\n', end='\n')


def test__saturated_colors__sanity():
    print(paint('\nsaturated colors: sanity', 'bold', 'sat white', 'ul'))
    for color, kode in COLOR_CODES['sat'].items():
        if isinstance(kode, dict):
            continue  # skip 'bg'
        print(f'\n{color} ({kode})',
              f'\033[{kode}m{color}\033[0m',
              sep='\n', end='\n')
