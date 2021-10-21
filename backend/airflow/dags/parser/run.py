import re
from . import play_components as pc
from . import core 

def parse_run_play(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a RUN play,
    returns the regex match re.Matchionary for each piece of information in the description
    Otherwise, returns None

    RUN plays should be of the form:
        {Player Name} {direction} for {distance} [(tackle by {tackler})]

    Example: 
        play_description = "David Montgomery right tackle for 15 yards
        returns: {
            "runner": "David Montgomery", 
            "direction": "right tackle", 
            "distance": "15 yards", 
            "tackler": None
        }
    """

    expressions = {
        'runner': pc.PLAYER,
        'direction': r"|".join(pc.RUN_DIRECTIONS),
        'distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }

    # Make tackler optional
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"%(runner)s %(direction)s for %(distance)s%(tackler)s" % expressions
    return re.search(pattern, play_description)


def parse_run_no_direction_play(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a RUN_NO_DIRECTION play,
    returns the regex match re.Matchionary for each piece of information in the description
    Otherwise, returns None

    RUN plays should be of the form:
        {Player Name} for {distance} [(tackle by {tackler})]

    Example: 
        play_description = "David Montgomery for 15 yards
        returns: {
            "runner": "David Montgomery", 
            "distance": "15 yards", 
            "tackler": None
        }
    """

    expressions = {
        'runner': pc.STRICT_PLAYER,
        'distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }

    # Make tackler optional
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"^%(runner)s for %(distance)s%(tackler)s" % expressions
    return re.search(pattern, play_description)