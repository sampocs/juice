import re
import constants as c


def regex_wrapper(regex_dict):
    return {var: r"(?P<%s>%s)" % (var, regex) for (var, regex) in regex_dict.items()}

def run_play(string):

    regex_components = {
        'runner': c.PLAYER,
        'direction': r"|".join(c.RUN_DIRECTIONS),
        'distance': r"|".join(c.DISTANCES),
        'tackler': c.PLAYER
    }

    pattern = r"%(runner)s %(direction)s for %(distance)s( \(tackle by %(tackler)s\))?" % regex_wrapper(regex_components)
    return re.match(pattern, string)


def complete_pass(string):
    regex_components = {
        'passer': c.PLAYER,
        'direction': r"|".join(c.PASS_DIRECTIONS),
        'reciever': c.PLAYER,
        'distance': r"|".join(c.DISTANCES),
        'tackler': c.PLAYER
    }

    pattern = r"%(passer)s pass complete %(direction)s to %(reciever)s for %(distance)s( \(tackle by %(tackler)s\))?" % regex_wrapper(regex_components)

    return re.match(pattern, string)


def incomplete_pass(string):
    regex_components = {
        'passer': c.PLAYER,
        'direction': r"|".join(c.PASS_DIRECTIONS),
        'reciever': c.PLAYER,
        'defender': c.PLAYER
    }

    pattern = r"%(passer)s pass incomplete %(direction)s intended for %(reciever)s( \(defended by %(defender)s\))?" % regex_wrapper(regex_components)

    return re.match(pattern, string)
