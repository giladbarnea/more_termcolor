from more_termcolor import paint

faint = paint('faint', 'faint')


def test__nested_colors__simple():
    print('\n' + faint)
    red = paint('red', 'red')
    red_faint_red = paint(f'red{faint}red', 'red')
    print(red_faint_red)
    assert red_faint_red == '\x1b[31mred\x1b[0m\x1b[2mfaint\x1b[0m\x1b[31mred\x1b[0m'
    assert red_faint_red == f'{red}{faint}{red}'
    bold = paint('bold', 'bold')
    
    bold_faint_bold = paint(f'bold{faint}bold', 'bold')
    print(bold_faint_bold)
    assert bold_faint_bold == f'{bold}{faint}{bold}'


def test__nested_colors__advanced():
    # '\x1b[1;97mbold_satwhite\x1b[0m'
    bold_satwhite = paint('bold_satwhite', 'bold', 'sat white')
    
    # '\x1b[1;97mbold_satwhite\x1b[2mfaint\x1b[0mbold_satwhite\x1b[0m'
    bold_satwhite__faint__bold_satwhite = paint(f'bold_satwhite{faint}bold_satwhite', 'bold', 'sat white')
    
    # print('\nPRINTING!!!', bold_satwhite__faint__bold_satwhite, sep='\n', end='\n')
    # '\x1b[1;97mbold_satwhite\x1b[0m\x1b[2mfaint\x1b[0m\x1b[1;97mbold_satwhite\x1b[0m'
    expected = f'{bold_satwhite}{faint}{bold_satwhite}'
    # needs to happen:
    # '\x1b[1;97mbold_satwhite\033[0;2mfaint\x1b[0;1;97mbold_satwhite\x1b[0m'
    assert bold_satwhite__faint__bold_satwhite == expected
    
    # {c(f'pass a str {i("args", False)}. like running {i("/bin/sh -c ...", False)}')}
    # {c(f'-s {i("strategy", False)} --strategy={i("strategy", False)}')}
