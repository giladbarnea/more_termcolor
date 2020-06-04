from more_termcolor import COLOR_CODES


def test__normal__sanity():
    """Just print colors that don't require any special reset code (pytest '-s' flag is necessary)"""
    print()
    for color, kode in COLOR_CODES.items():
        if isinstance(kode, dict):
            continue  # skip 'bg', 'sat'
        if color in COLOR_CODES['reset']:
            continue  # skip 'italic', 'ul', ...
        print(f'\ncolor: {color}, code: {kode}',
              f'\033[{kode}m{color}\033[0m',
              sep='\n', end='\n')
