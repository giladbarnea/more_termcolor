import functools
import inspect

from more_termcolor import core, util, cprint, colored
from more_termcolor.colors import ul
from contextlib import contextmanager
from typing import overload, Union, Any, Callable, Tuple
import re
from pathlib import Path


def has_duplicates(collection) -> bool:
    return len(set(collection)) < len(collection)


@overload
def assert_raises(exc, *search_in_args: str):
    ...


@overload
def assert_raises(exc, reg: Union[str, re.Pattern] = None):
    ...


@contextmanager
def assert_raises(exc, *search_in_args, reg=None):
    """at least one exception arg needs to have all search strings, or fullmatch `reg` (whichever is passed)"""
    try:
        yield
    except exc as e:
        if not search_in_args and not reg:
            return
        if reg:
            reg = re.compile(reg)
            for a in list(map(str, e.args)):
                if reg.fullmatch(a):
                    return True
            raise
        for a in list(map(str, e.args)):
            for s in search_in_args:
                if not re.search(re.escape(s), a):
                    break
            else:
                return True
        raise
    except Exception as e:
        raise
    else:
        raise AssertionError(f"assert_raises({exc.__qualname__}): {exc.__qualname__} was NOT raised")


@contextmanager
def assert_doesnt_raise(exc):
    try:
        yield
    except exc:
        raise


background_colors = list(core.STANDARD_BACKGROUND_COLOR_CODES.keys())
foreground_colors = list(core.FOREGROUND_COLOR_CODES.keys())
bright_fg_colors = list(core.BRIGHT_FOREGROUND_COLOR_CODES.keys())
bright_bg_colors = list(core.BRIGHT_BACKGROUND_COLOR_CODES.keys())


def _print(description, string):
    util.spacyprint(f'{ul(description)}:', string, repr(string))


def actualprint(string):
    _print('actual', string)


def expectedprint(string):
    _print('expected', string)


def print_and_compare(fn_or_cls):
    """
    Examples:
        ::
         
         # function decorator:
         
         @print_and_compare
         def test__foo():
             actual = 1 + 1
             expected = 2
             return actual, expected
             
         
         # class decorator:
         
         @print_and_compare
         class Foo:
             def test__foo(self):
                 actual = 1 + 1
                 expected = 2
                 return actual, expected
    """
    
    @functools.wraps(fn_or_cls)
    def wrap():
        actual, expected = fn_or_cls()
        
        where = colored(f'{Path(inspect.getsourcefile(fn_or_cls)).name}:{inspect.getsourcelines(fn_or_cls)[1]}', 'dark')
        cprint(f'\n\n{fn_or_cls.__name__}    {where}', 'bold', 'bright white', 'on black')
        actualprint(actual)
        expectedprint(expected)
        assert actual == expected
        cprint('OK', 'green')
    
    if isinstance(fn_or_cls, type):
        class Monkey(fn_or_cls):
            
            def __getattribute__(self, name: str) -> Any:
                attr = super().__getattribute__(name)
                if name.startswith('test__'):
                    decorated = print_and_compare(attr)
                    return decorated
                return attr
        
        return Monkey
    return wrap
