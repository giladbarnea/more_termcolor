import re
from pprint import pformat
from typing import Union

from more_termcolor import convert, settings, core
from more_termcolor.util import spacyprint, Singleton

COLOR_CODES_RE = r'(\d{,3})(?:;)?(\d{,3})?(?:;)?(\d{,3})?'
COLOR_BOUNDARY_RE = re.compile(fr'\033\[{COLOR_CODES_RE}m')


# NESTED_RE = re.compile(fr'(?P<outer_open>{COLOR_BOUNDARY_RE})'
#                        r'(?P<outer_content_a>[^\033]*)'
#                        fr'(?P<inner_open>{COLOR_BOUNDARY_RE})'
#                        r'(?P<inner_content>[^\033]*)'
#                        fr'(?P<inner_close>{COLOR_BOUNDARY_RE})'
#                        r'(?P<outer_content_b>[^\033]*)'
#                        fr'(?P<outer_close>{COLOR_BOUNDARY_RE})'
#                        )


def fix_nested_colors(m: re.Match):
    dct = m.groupdict()
    outer_open = dct['outer_open']
    outer_close = dct['outer_close']
    outer_content_a = dct['outer_content_a']
    outer_content_b = dct['outer_content_b']
    inner_content = dct['inner_content']
    inner_open = dct['inner_open']
    inner_close = dct['inner_close']
    ret = f'{outer_open}{outer_content_a}{outer_close}{inner_open}{inner_content}{inner_close}{outer_open}{outer_content_b}{outer_close}'
    if settings.debug:
        print('\nfix_nested_colors()', f'ret: ', ret, repr(ret), pformat(dct), sep='\n', end='\n')
    return ret


# def yellow(text: any):
#     # 33
#     return paint(text, 'yellow')
#
#
# def red(text: any):
#     # text = re.sub(r'(?<=\033)(.*)(\[\d{,3}m)', lambda m: m.groups()[0] + '[31m', text)
#     # 31
#     return paint(text, 'red')
#
#
# def green(text: any):
#     # 32
#     return paint(text, 'green')
#
#
# def bold(text: any):
#     return paint(text, 'bold')
#
#
# def faint(text: any):
#     return paint(text, 'faint')
#
#
# def satblack(text: any):
#     return paint(text, 'sat black')
#
#
# def satwhite(text: any):
#     return paint(text, 'sat white')
#
#
# def white(text: any):
#     return paint(text, 'white')
#
#
# def ul(text):
#     return paint(text, 'ul')
#
#
# def italic(text):
#     return paint(text, 'italic')


class Paint(Singleton):
    def __call__(self, text: str, *colors: Union[str, int]):
        if settings.debug:
            spacyprint(f'text: {text}', f'colors: {colors}')
        outer_open_codes = [convert.to_code(c) for c in colors]
        start = f'\033[{";".join(map(str, outer_open_codes))}m'
        if settings.debug:
            spacyprint(f'outer_open_codes:', outer_open_codes, f'colors:', colors)
        # TODO:
        #  if nested is fmt:
        #       reset nested
        #       if outer is fmt and outer.reset == nested.reset:
        #           also re-open outer
        #  else:
        #       if outer is fmt:
        #           reset fg
        #       else:
        #           re-open outer
        try:
            # match = COLOR_BOUNDARY_RE.search(text)
            # nested_codes = [g for g in match.groups() if g]
            
            # if more than one open/reset pairs exist in text,
            # ignore them (*_) because they'd been recursively
            # taken care of.
            nested_open, *_, nested_reset = re.finditer(COLOR_BOUNDARY_RE, text)
            nested_open_codes = [int(c) for c in nested_open.groups() if c]
            outer_has_formatting = any(c in core.FORMATTING_CODES for c in outer_open_codes)
            nested_has_formatting = any(c in core.FORMATTING_CODES for c in nested_open_codes)
            nested_reset_codes = [int(rc) for rc in nested_reset.groups() if rc]
            if settings.debug:
                spacyprint(f'nested_open: {nested_open}',
                           f'nested_reset: {nested_reset}',
                           f'nested_open_codes: {nested_open_codes}',
                           f'outer_has_formatting: {outer_has_formatting}',
                           f'nested_has_formatting: {nested_has_formatting}',
                           f'nested_reset_codes: {nested_reset_codes}')
            if nested_has_formatting:
                proper_nested_reset_codes = [convert.to_reset_code(c) for c in nested_open_codes]
                if outer_has_formatting:
                    outer_reset_codes = [convert.to_reset_code(c) for c in outer_open_codes]
                    if any(oc in proper_nested_reset_codes for oc in outer_reset_codes):
                        proper_nested_reset_codes.extend(outer_open_codes)
                proper_nested_reset = f'\033[{";".join(map(str, proper_nested_reset_codes))}m'
                if settings.debug:
                    spacyprint(f'replacing nested reset with proper nested reset. before: ', repr(text), text)
                text = text.replace(nested_reset.group(), proper_nested_reset, 1)
                if settings.debug:
                    spacyprint(f'after: ', repr(text), text)
            
            else:
                if outer_has_formatting:
                    # reset fg
                    if settings.debug:
                        spacyprint(f'replacing nested reset with fg reset. before: ', repr(text), text)
                    text = text.replace(nested_reset.group(), '\033[39m', 1)
                    if settings.debug:
                        spacyprint(f'after: ', repr(text), text)
                else:
                    # replace nested reset with outer open
                    if settings.debug:
                        spacyprint(f'replacing nested reset with outer open. before: ', repr(text), text)
                    text = text.replace(nested_reset.group(), start, 1)
                    if settings.debug:
                        spacyprint(f'after: ', repr(text), text)
        except ValueError as e:  # not enough values to unpack (COLOR_BOUNDARY_RE did not match)
            pass
        # reset = f'\033[{";".join(map(str, map(convert.to_reset_code, colors)))}m'
        reset = f'\033[0m'
        painted = f'{start}{text}{reset}'
        if settings.debug:
            spacyprint(f'returning painted: {repr(painted)}', painted)
        if settings.print:
            print(painted)
        return painted
    
    def __init__(self):
        super().__init__()
        # paint.red('...')
        for color, code in core.FG_COLOR_CODES.items():
            setattr(self, color, lambda text, c=code: self(text, code))
        
        exclude = ('all', 'fg', 'bg')
        # paint.bold('...')
        for color, code in core.FORMATTING_COLOR_CODES.items():
            if color in exclude:
                continue
            setattr(self, color, lambda text, c=code: self(text, code))
        
        # paint.sat_red('...')
        for color, code in core.SAT_BG_COLOR_CODES.items():
            setattr(self, f'sat_{color}', lambda text, c=code: self(text, code))
        
        # paint.bg_red('...')
        for color, code in core.BG_COLOR_CODES.items():
            setattr(self, f'bg_{color}', lambda text, c=code: self(text, code))
        
        # paint.sat_bg_red('...')
        for color, code in core.SAT_BG_COLOR_CODES.items():
            setattr(self, f'sat_bg_{color}', lambda text, c=code: self(text, code))


paint = Paint()
# __all__ = ['yellow',
#            'red',
#            'green',
#            'bold',
#            'faint',
#            'satblack',
#            'satwhite',
#            'ul',
#            'italic',
#            'paint']
# if __name__ == '__main__':
#     _termcolors()
