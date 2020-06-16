from more_termcolor import colored


#####################
# Formatting (some) #
#####################

def bold(text, *colors):
    return colored(text, 'bold', *colors)


def dark(text, *colors):
    return colored(text, 'dark', *colors)


def italic(text, *colors):
    return colored(text, 'italic', *colors)


ita = italic


def underline(text, *colors):
    return colored(text, 'ul', *colors)


ul = underline


def reverse(text, *colors):
    return colored(text, 'reverse', *colors)


######################
# Foreground (30-37) #
######################
def black(text, *colors):
    return colored(text, 'black', *colors)


grey = black


def red(text, *colors):
    return colored(text, 'red', *colors)


def green(text, *colors):
    return colored(text, 'green', *colors)


def yellow(text, *colors):
    return colored(text, 'yellow', *colors)


def blue(text, *colors):
    return colored(text, 'blue', *colors)


def magenta(text, *colors):
    return colored(text, 'magenta', *colors)


def cyan(text, *colors):
    return colored(text, 'cyan', *colors)


def white(text, *colors):
    return colored(text, 'white', *colors)


###############################
# Bright foreground (100-107) #
###############################
def brightblack(text, *colors):
    return colored(text, 'bright black', *colors)


brightgrey = brightblack


def brightred(text, *colors):
    return colored(text, 'bright red', *colors)


def brightgreen(text, *colors):
    return colored(text, 'bright green', *colors)


def brightyellow(text, *colors):
    return colored(text, 'bright yellow', *colors)


def brightblue(text, *colors):
    return colored(text, 'bright blue', *colors)


def brightmagenta(text, *colors):
    return colored(text, 'bright magenta', *colors)


def brightcyan(text, *colors):
    return colored(text, 'bright cyan', *colors)


def brightwhite(text, *colors):
    return colored(text, 'bright white', *colors)


######################
# Background (40-47) #
######################
def on_black(text, *colors):
    return colored(text, 'on black', *colors)


on_grey = on_black


def on_red(text, *colors):
    return colored(text, 'on red', *colors)


def on_green(text, *colors):
    return colored(text, 'on green', *colors)


def on_yellow(text, *colors):
    return colored(text, 'on yellow', *colors)


def on_blue(text, *colors):
    return colored(text, 'on blue', *colors)


def on_magenta(text, *colors):
    return colored(text, 'on magenta', *colors)


def on_cyan(text, *colors):
    return colored(text, 'on cyan', *colors)


def on_white(text, *colors):
    return colored(text, 'on white', *colors)


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
