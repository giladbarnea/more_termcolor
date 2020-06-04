from more_termcolor import COLOR_CODES


def test__normal__sanity():
    """Just print colors all standard colors (not including saturated or background (pytest '-s' flag is necessary)"""
    print()
    for color, kode in COLOR_CODES.items():
        if isinstance(kode, dict):
            continue  # skip 'bg', 'sat'
        print(f'\n{color} ({kode})',
              f'\033[{kode}m{color}\033[0m',
              sep='\n', end='\n')
