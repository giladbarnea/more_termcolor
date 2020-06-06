def confirm(prompt='continue?') -> bool:
    return (answer := input(f'{prompt} y/n\t').lower()) == 'y' or answer == 'yes'
