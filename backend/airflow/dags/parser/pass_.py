import re
from . import play_components as pc
from . import core

def parse_pass_complete_play(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PASS_COMPLETE play,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PASS_COMPLETE plays should be of the form:
        {Player Name} pass complete [{direction}] to {receiver} for {distance} [(tackle by {tackler})]

    Example: 
        play_description = "Justin Fields pass complete deep right to Allen Robinson for 45 yards (tackle by Jalen Ramsey)"
        returns: {
            "runner": "Justin Fields", 
            "direction": "deep right", 
            "distance": "45 yards", 
            "tackler": Jalen Ramsey
        }
    """
    expressions = {
        'passer': pc.PLAYER,
        'direction': r"|".join(pc.PASS_DIRECTIONS),
        'receiver': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)
    expressions['direction'] = core.make_optional(expressions['direction'])

    pattern = r"%(passer)s pass complete%(direction)s to %(receiver)s for %(distance)s%(tackler)s" % expressions

    return re.search(pattern, play_description)


def parse_pass_incomplete_play(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PASS_INCOMPLETE play,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PASS_INCOMPLETE  plays should be of the form:
        {Player Name} pass incomplete [{direction}] [intended for {receiver}] [(defended by {tackler})]

    Example: 
        play_description = "Aaron Rodgers pass incomplete short right intended for Davante Adams (defended by Jaylon Johnson)"
        returns: {
            "runner": "Justin Fields", 
            "direction": "deep right", 
            "distance": "45 yards", 
            "tackler": "Jalen Ramsey"
        }
    """
    expressions = {
        'passer': pc.PLAYER,
        'direction': r"|".join(pc.PASS_DIRECTIONS),
        'receiver': pc.PLAYER,
        'defender': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_defender_with_defended_event(expressions)
    expressions = core.replace_receiver_with_intended_event(expressions)
    expressions['direction'] = core.make_optional(expressions['direction'])

    pattern = r"%(passer)s pass incomplete%(direction)s%(receiver)s%(defender)s" % expressions

    return re.search(pattern, play_description)