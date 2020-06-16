import functools
import inspect
import re
from contextlib import contextmanager
from pathlib import Path
from typing import overload, Union, Any, Generator

from more_termcolor import core
from itertools import permutations as permutations


def memoize(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            return cache[key]
        except KeyError:
            ret = fun(*args, **kwargs)
            cache[key] = ret
            return ret
    
    cache = {}
    return wrapper


def has_duplicates(collection) -> bool:
    return len(set(collection)) < len(collection)


def spacyprint(*values):
    print('', *values, sep='\n', end='\x1b[0m\n')


def codes_perm_re(*values):
    r"""
    >>> assert codes_perm_re(1, 2) == re.compile(r'\x1b\[(1;2|2;1)m')
    """
    perms = f"({'|'.join(map(lambda perm: ';'.join(perm), permutations(map(str, values), len(values))))})"
    return re.compile(fr'\x1b\[{perms}m')


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
    if isinstance(string, str) and '\x1b' in string:
        spacyprint(f'\x1b[4m{description}\x1b[0m:', string, repr(string))
    else:
        spacyprint(f'\x1b[4m{description}\x1b[0m:', string)


def actualprint(string):
    _print('\x1b[21;37mactual\x1b[24;39m', string)


def expectedprint(string):
    _print('expected', string)


@memoize
def getsourcefilename(obj):
    return Path(inspect.getsourcefile(obj)).name


@memoize
def getsourcelineno(obj):
    return inspect.getsourcelines(obj)[1]


def _print_and_compare(_actual, _expected):
    actualprint(_actual)
    expectedprint(_expected)
    if isinstance(_expected, re.Pattern):
        assert _expected.fullmatch(_actual)
    else:
        assert _actual == _expected
    print('\x1b[32mOK\x1b[0m')


def print_and_compare(fn_or_cls):
    """
    Examples:
        ::
         
         # decorate a function that returns a tuple:
         
         @print_and_compare
         def test__foo():
             actual = 1 + 1
             expected = 2
             return actual, expected
             
         
         # decorate a function that yields tuples:
         
         @print_and_compare
         def test__foo():
             actual = 1 + 1
             expected = 2
             yield actual, expected
             
             actual *= 2
             expected *= 2
             yield actual, expected
             
         
         # decorate a class:
         
         @print_and_compare
         class Foo:
             def test__foo(self):
                 actual = 1 + 1
                 expected = 2
                 return actual, expected
    """
    if isinstance(fn_or_cls, type):
        class Monkey(fn_or_cls):
            
            def __getattribute__(self, name: str) -> Any:
                attr = super().__getattribute__(name)
                if name.startswith('test__'):
                    decorated = print_and_compare(attr)
                    return decorated
                return attr
        
        return Monkey
    
    @functools.wraps(fn_or_cls)
    def wrap():
        
        where = f'{getsourcefilename(fn_or_cls)}:{getsourcelineno(fn_or_cls)}'
        
        print(f'\n\n\x1b[1;97;40m{fn_or_cls.__name__}    \x1b[22;2m{where}\n\x1b[0m')
        rv = fn_or_cls()
        if isinstance(rv, tuple):
            actual, expected = rv
            _print_and_compare(actual, expected)
        
        else:  # returned a generator
            rv: Generator
            try:
                for actual, expected in rv:
                    try:
                        _print_and_compare(actual, expected)
                    except AssertionError as e:
                        rv.throw(AssertionError, e)
                    
                    print('\x1b[32mOK\x1b[0m')
            except StopIteration:
                return
    
    return wrap
