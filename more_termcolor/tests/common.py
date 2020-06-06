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


background_colors = list(core.BG_COLOR_CODES.keys())
foreground_colors = list(core.FG_COLOR_CODES.keys())
saturated_fg_colors = list(core.SAT_FG_COLOR_CODES.keys())
saturated_bg_colors = list(core.SAT_BG_COLOR_CODES.keys())
