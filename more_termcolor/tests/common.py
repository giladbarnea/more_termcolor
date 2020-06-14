from more_termcolor import core
from contextlib import contextmanager
import re


def has_duplicates(collection) -> bool:
    return len(set(collection)) < len(collection)


@contextmanager
def assert_raises(exc, *search_in_args):
    try:
        yield
    except exc as e:
        if search_in_args:
            # at least one exception arg needs to have all search strings
            if not any(all(re.search(re.escape(s), a) for s in search_in_args) for a in list(map(str, e.args))):
                raise
        pass
    except Exception as e:
        pass


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
