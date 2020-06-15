from more_termcolor import colored, cprint
from more_termcolor.tests import common
from more_termcolor.tests.common import actualprint, expectedprint
import io


#########################################
# compatibility with original termcolor #
#########################################
def test__cprint_sanity():
    cprint('Grey color', 'grey')
    cprint('Red color', 'red')
    cprint('Green color', 'green')
    cprint('Yellow color', 'yellow')
    cprint('Blue color', 'blue')
    cprint('Magenta color', 'magenta')
    cprint('Cyan color', 'cyan')
    cprint('White color', 'white')
    
    cprint('On grey color', on_color='on_grey')
    cprint('On red color', on_color='on_red')
    cprint('On green color', on_color='on_green')
    cprint('On yellow color', on_color='on_yellow')
    cprint('On blue color', on_color='on_blue')
    cprint('On magenta color', on_color='on_magenta')
    cprint('On cyan color', on_color='on_cyan')
    cprint('On white color', color='grey', on_color='on_white')
    
    cprint('Bold grey color', 'grey', attrs=['bold'])
    cprint('Dark red color', 'red', attrs=['dark'])
    cprint('Underline green color', 'green', attrs=['underline'])
    cprint('Blink yellow color', 'yellow', attrs=['blink'])
    cprint('Reversed blue color', 'blue', attrs=['reverse'])
    cprint('Concealed Magenta color', 'magenta', attrs=['concealed'])
    cprint('Bold underline reverse cyan color', 'cyan', attrs=['bold', 'underline', 'reverse'])
    cprint('Dark blink concealed white color', 'white', attrs=['dark', 'blink', 'concealed'])
    
    cprint('Underline red on grey color', 'red', 'on_grey', ['underline'])
    cprint('Reversed green on red color', 'green', 'on_red', ['reverse'])
    
    cprint('Underline red on grey color', 'red', on_color='on_grey', attrs=['underline'])
    cprint('Reversed green on red color', color='green', on_color='on_red', attrs=['reverse'])


def test__cprint():
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on_red', attrs=['bold'], file=f)
    s = f.getvalue()
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on red', 'bold', file=f)
    assert f.getvalue() == s
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])


def test__cprint2():
    cprint(f'\n\n{test__cprint2.__name__}', 'bold', 'bright white')


def test__cprint3():
    cprint('foo', 'bright white', on_color='black')
    with common.assert_raises(KeyError, reg=r'^bold$'):
        cprint('foo', 'bright white', 'on_bold')
