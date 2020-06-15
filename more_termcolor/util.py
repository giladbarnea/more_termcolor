def confirm(prompt='continue?') -> bool:
    answer = input(f'{prompt} y/n/q\t').lower()
    if answer == 'q':
        import sys
        sys.exit()
    return answer == 'y' or answer == 'yes'
