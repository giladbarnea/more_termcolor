"""
incompat
R    G       R
31   32  →   31
outer is std:
    nested is std:
        re-open outer

compat
R    F       /F/B
31   2   →   22
outer is std:
    nested is fmt:
        reset nested

adv_0
I    B       /F/B
3    1   →   22
outer is fmt:
    nested is fmt:
        outer.reset != nested.reset:
            reset nested
            
adv_1
I    R       /FG
3    31  →   39
outer is fmt:
    nested is std:
        reset fg
        
adv_1_b
I    SG      /FG
3    92  →   39
outer is fmt:
    nested is bright:
        reset fg

adv_2
B    I       /I
1    3   →   23
outer is fmt:
    nested is fmt:
        outer.reset != nested.reset:
            reset nested

adv_3
B    F       /F/B B
1    2   →   22;1
outer is fmt:
    nested is fmt:
        outer.reset == nested.reset:
            reset nested
            re-open outer

adv_4
S    F       /F
97   2   →   22
outer is bright:
    nested is fmt:
        reset nested

adv_5
S    R       S
97   31  →   97
outer is bright:
    nested is std:
        re-open outer

compat_and_incompat
S+B  F       /F/B B
1;97 2   →   22;1
outer has fmt:
    nested is fmt:
        outer.fmt.reset == nested.reset:
            reset nested
            re-open outer

"""

from more_termcolor import colored
from more_termcolor.tests.common import print_and_compare


#############
# Bad usage #
#############

# Trivial
#########


@print_and_compare
class Test:
    def test__no_color(self):
        actual = colored('foo')
        expected = 'foo'
        return actual, expected
    
    def test__same_color(self):
        actual = colored('foo', 'red', 'dark', 'red')
        expected = '\x1b[31;2mfoo\x1b[0m'
        return actual, expected
    
    def test__too_many_colors(self):
        actual = colored('foo', "red", "on black", "bold", "dark", "italic", "underline", "blink", "reverse", "strike", "overline")
        expected = '\x1b[31;40;1;2;3;4;5;7;9;53mfoo\x1b[0m'
        return actual, expected
    
    def test__no_text(self):
        actual = colored('', 'red')
        expected = ''
        return actual, expected
