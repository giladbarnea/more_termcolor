from more_termcolor import colored


#####################
# Formatting (some) #
#####################

def bold(text, *colors, **kwargs):
    return colored(text, 'bold', *colors, **kwargs)


def dark(text, *colors, **kwargs):
    return colored(text, 'dark', *colors, **kwargs)


def italic(text, *colors, **kwargs):
    return colored(text, 'italic', *colors, **kwargs)


ita = italic


def underline(text, *colors, **kwargs):
    return colored(text, 'ul', *colors, **kwargs)


ul = underline


def reverse(text, *colors, **kwargs):
    return colored(text, 'reverse', *colors, **kwargs)


######################
# Foreground (30-37) #
######################
def black(text, *colors, **kwargs):
    return colored(text, 'black', *colors, **kwargs)


grey = black


def red(text, *colors, **kwargs):
    return colored(text, 'red', *colors, **kwargs)


def green(text, *colors, **kwargs):
    return colored(text, 'green', *colors, **kwargs)


def yellow(text, *colors, **kwargs):
    return colored(text, 'yellow', *colors, **kwargs)


def blue(text, *colors, **kwargs):
    return colored(text, 'blue', *colors, **kwargs)


def magenta(text, *colors, **kwargs):
    return colored(text, 'magenta', *colors, **kwargs)


def cyan(text, *colors, **kwargs):
    return colored(text, 'cyan', *colors, **kwargs)


def white(text, *colors, **kwargs):
    return colored(text, 'white', *colors, **kwargs)


###############################
# Bright foreground (100-107) #
###############################
def brightblack(text, *colors, **kwargs):
    return colored(text, 'bright black', *colors, **kwargs)


brightgrey = brightblack


def brightred(text, *colors, **kwargs):
    return colored(text, 'bright red', *colors, **kwargs)


def brightgreen(text, *colors, **kwargs):
    return colored(text, 'bright green', *colors, **kwargs)


def brightyellow(text, *colors, **kwargs):
    return colored(text, 'bright yellow', *colors, **kwargs)


def brightblue(text, *colors, **kwargs):
    return colored(text, 'bright blue', *colors, **kwargs)


def brightmagenta(text, *colors, **kwargs):
    return colored(text, 'bright magenta', *colors, **kwargs)


def brightcyan(text, *colors, **kwargs):
    return colored(text, 'bright cyan', *colors, **kwargs)


def brightwhite(text, *colors, **kwargs):
    return colored(text, 'bright white', *colors, **kwargs)


######################
# Background (40-47) #
######################
def on_black(text, *colors, **kwargs):
    return colored(text, 'on black', *colors, **kwargs)


on_grey = on_black


def on_red(text, *colors, **kwargs):
    return colored(text, 'on red', *colors, **kwargs)


def on_green(text, *colors, **kwargs):
    return colored(text, 'on green', *colors, **kwargs)


def on_yellow(text, *colors, **kwargs):
    return colored(text, 'on yellow', *colors, **kwargs)


def on_blue(text, *colors, **kwargs):
    return colored(text, 'on blue', *colors, **kwargs)


def on_magenta(text, *colors, **kwargs):
    return colored(text, 'on magenta', *colors, **kwargs)


def on_cyan(text, *colors, **kwargs):
    return colored(text, 'on cyan', *colors, **kwargs)


def on_white(text, *colors, **kwargs):
    return colored(text, 'on white', *colors, **kwargs)


__all__ = [
    'bold',
    'dark',
    'italic',
    'ita',
    'underline',
    'ul',
    'reverse',
    'black',
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'brightblack',
    'brightgrey',
    'brightwhite',
    'brightred',
    'brightgreen',
    'brightyellow',
    'brightblue',
    'brightcyan',
    'brightmagenta',
    'on_black',
    'on_grey',
    'on_white',
    'on_red',
    'on_green',
    'on_yellow',
    'on_blue',
    'on_cyan',
    'on_magenta',
    ]
