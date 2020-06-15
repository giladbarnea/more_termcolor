import functools

from more_termcolor import core, util, cprint
from contextlib import contextmanager
from typing import overload, Union, Any
import re


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
    util.spacyprint(f'{description}:', string, repr(string))


def actualprint(string):
    _print('actual', string)


def expectedprint(string):
    _print('expected', string)


def print_and_compare(fn):
    @functools.wraps(fn)
    def wrap():
        actual, expected = fn()
        cprint(f'\n\n{fn.__name__}', 'bold', 'bright white')
        actualprint(actual)
        expectedprint(expected)
        assert actual == expected
    
    return wrap


def print_and_compare_methods(cls: type):
    """
    Spares boilerplate by printing what's expected and what's actual,
    asserting equality and printing test name.
    ::
    @print_and_compare_methods
    class Foo:
        @staticmethod
        def test__bar():
            actual = 1 + 1
            expected = 2
            return actual, expected
    """
    
    class Monkey(cls):
        
        def __getattribute__(self, name: str) -> Any:
            attr = super().__getattribute__(name)
            if name.startswith('test__'):
                decorated = print_and_compare(attr)
                return decorated
            return attr
    
    return Monkey
