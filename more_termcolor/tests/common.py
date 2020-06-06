from more_termcolor import core


def has_duplicates(collection) -> bool:
    return len(set(collection)) < len(collection)


background_colors = list(core.BG_COLOR_CODES.keys())
foreground_colors = list(core.FG_COLOR_CODES.keys())
saturated_fg_colors = list(core.SAT_FG_COLOR_CODES.keys())
saturated_bg_colors = list(core.SAT_BG_COLOR_CODES.keys())
