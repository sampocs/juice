import re
from . import play_components as pc
from . import core

def parse_sack_full(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a SACK_FULL,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    SACK_FULL should be of the form:
        {Player Name} sacked by {Player Name} for {distance}

    Example: 
        play_description = "Aaron Rodgers sacked by Khalil Mack for -10 yards"
        returns: {
            "quarterback": "Aaron Rodgers",
            "sacker": "Khalil Mack",
            "distance": "-10 yards"
        }
    """
    expressions = {
        'quarterback': pc.PLAYER,
        'sacker': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES)
    }
    pattern = r"%(quarterback)s sacked by %(sacker)s for %(distance)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_sack_half(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a SACK_HALF,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    SACK_HALF should be of the form:
        {Player Name} sacked by and {Player Name} for {distance} and {Player Name} for {distance}

    Example: 
        play_description = "Aaron Rodgers sacked by and Khalil Mack for -10 yards and Akiem Hicks for -10 yards"
        returns: {
            "quarterback": "Aaron Rodgers",
            "sacker1": "Khalil Mack",
            "sacker2": "Akiem Hicks",
            "distance1": "-10 yards",
            "distance2": "-10 yards"
        }
    """
    expressions = {
        'quarterback': pc.PLAYER,
        'sacker1': pc.PLAYER,
        'sacker2': pc.PLAYER,
        'distance1': r"|".join(pc.DISTANCES),
        'distance2': r"|".join(pc.DISTANCES)
    }
    pattern = r"%(quarterback)s sacked by and %(sacker1)s for %(distance1)s and %(sacker2)s for %(distance2)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_fumble(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a FUMBLE,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    FUMBLE should be of the form:
        {Player Name} fumbles [(forced by {Player Name})], 
        recovered by {Player Name} at {yardage} [and returned for {distance}] [(tackle by {Player Name})]

    Example: 
        play_description = "Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10 and returned for 45 yards"
        returns: {
            "fumbler": "Aaron Rodgers",
            "forcer": "Khalil Mack",
            "recoverer": "Akiem Hicks",
            "yardage": "CHI-10",
            "return_distance": "45 yards",
            "tackler": None
        }
    """
    expressions = {
        'fumbler': pc.PLAYER,
        'forcer': pc.PLAYER,
        'recoverer': pc.PLAYER,
        'yardage': pc.YARDAGE,
        'return_distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_forcer_with_forced_event(expressions)
    expressions = core.replace_return_distance_with_return_event(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"%(fumbler)s fumbles%(forcer)s, recovered by %(recoverer)s at %(yardage)s%(return_distance)s%(tackler)s" % expressions

    return re.search(pattern, play_description)


def parse_interception(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a INTERCEPTION,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    INTERCEPTION should be of the form:
        {Player Name} pass [(defended by {Player Name})] [intended for {Player Name}] 
        is intercepted by {Player Name} at {yardage} and returned for {distance} [(tackle by {Player Name})]

    Example: 
        play_description = "Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams" + \
                            " is intercepted by Eddie Jackson at CHI-10 and returned for 45 yards"
        returns: {
            "quarterback": "Aaron Rodgers",
            "direction": "short right",
            "defender": "Jaylon Johnson",
            "receiver": "Davante Adams",
            "intercepter": "Eddie Jackson",
            "yardage": "CHI-10",
            "return_distance": "45 yards",
            "tackler": None
        }
    """
    expressions = {
        'quarterback': pc.PLAYER,
        'direction': r"|".join(pc.PASS_DIRECTIONS),
        'defender': pc.PLAYER,
        'receiver': pc.PLAYER,
        'intercepter': pc.PLAYER,
        'yardage': pc.YARDAGE,
        'return_distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions['direction'] = core.make_optional(expressions['direction'])
    expressions = core.replace_defender_with_defended_event(expressions)
    expressions = core.replace_receiver_with_intended_event(expressions)
    expressions = core.replace_return_distance_with_return_event(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"%(quarterback)s pass%(direction)s%(defender)s%(receiver)s is intercepted by %(intercepter)s at %(yardage)s%(return_distance)s%(tackler)s" % expressions

    return re.search(pattern, play_description)