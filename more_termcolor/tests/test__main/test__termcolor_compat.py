from more_termcolor import colored, cprint
from more_termcolor.tests.common import _actualprint, _expectedprint
import io


#########################################
# compatibility with original termcolor #
#########################################
def test__cprint():
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on_red', attrs=['bold'], file=f)
    s = f.getvalue()
    f = io.StringIO()
    cprint('Hello, World!', 'green', 'on red', 'bold', file=f)
    assert f.getvalue() == s
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
