import pytest

from more_termcolor import paint


def test__paint_fn__basic():
    assert paint.paint('foo', 'bold') == paint.bold('foo')


@pytest.mark.skip()
def test__replace_reset_code():
    grey = paint.paint('grey', 'grey')
    print('\n' + grey)
    red = paint.paint('red', 'red')
    mix1 = paint.paint(f'red{grey}red', 'red')
    print(mix1)
    assert mix1 == '\x1b[31mred\x1b[0m\x1b[2mgrey\x1b[0m\x1b[31mred\x1b[0m'
    assert mix1 == f'{red}{grey}{red}'
    bold = paint.paint('bold', 'bold')
    
    mix2 = paint.paint(f'bold{grey}bold', 'bold')
    print(mix2)
    assert mix2 == f'{bold}{grey}{bold}'
    
    bold_satwhite = paint.paint('bold_satwhite', 'bold', 'sat white')
    mix3 = paint.paint(f'bold_satwhite{grey}bold_satwhite', 'bold', 'sat white')
    print(mix3)
    print(repr(mix3))
    # needs to happen:
    # '\x1b[1;97mbold_satwhite\033[0;2mgrey\x1b[0;1;97mbold_satwhite\x1b[0m'
    assert mix3 == f'{bold_satwhite}{grey}{bold_satwhite}'
    
    # {c(f'pass a str {i("args", False)}. like running {i("/bin/sh -c ...", False)}')}
    # {c(f'-s {i("strategy", False)} --strategy={i("strategy", False)}')}
