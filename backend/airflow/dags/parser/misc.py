import re
from . import play_components as pc
from . import core
from typing import List


def parse_penalty(play_description: str) -> List[re.Match]:
    """
    Given a play by play description, if it's a PENALTY,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PENALTY should be of the form:
        Penalty on {Player Name}: {penalty}, {distance} ({response}) [(no play)]

    Example: 
        play_description = "Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards (accepted)"
        returns: {
            "penalty_on": "Ndamukong Suh", 
            "penalty_type": "Unnecessary Roughness",
            "penalty_distance": "15 yards",
            "penalty_response": "accepted",
            "no_play": None
        }
    """
    expressions = {
        'penalty_on': pc.PLAYER,
        'penalty_type': pc.PENALTY,
        'penalty_distance': r"|".join(pc.DISTANCES),
        'penalty_response': r"|".join(pc.PENALTY_RESPONSES),
        'no_play': pc.NO_PLAY
    }
    expressions = core.wrap_expressions(expressions)
    expressions['penalty_response'] = core.make_optional(r"\(%s\)" % expressions['penalty_response'])
    expressions['no_play'] = core.make_optional(r"\(%s\)" % expressions['no_play'])

    pattern = r"Penalty on %(penalty_on)s: %(penalty_type)s, %(penalty_distance)s%(penalty_response)s%(no_play)s" % expressions

    return list(re.finditer(pattern, play_description))


def parse_timeout(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a TIMEOUT,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    TIMEOUT should be of the form:
        Timeout {number} by {Team}

    Example: 
        play_description = "Timeout #1 by Chicago Bears"
        returns: {
            "timeout_number": "#1", 
            "team": "Chicago Bears"
        }
    """
    expressions = {
        'timeout_number': r"#[\d]",
        'team': pc.TEAM_NAME
    }

    pattern = r"Timeout %(timeout_number)s by %(team)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_spike(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a SPIKE,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    SPIKE should be of the form:
        {Player Name} spiked the ball

    Example: 
        play_description = "Justin Fields spiked the ball"
        returns: {
            "player": "Justin Fields"
        }
    """
    expressions = {
        'player': pc.PLAYER
    }

    pattern = r"%(player)s spiked the ball" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_kneel(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a KNEEL,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    KNEEL should be of the form:
        {Player Name} knees for {distance}

    Example: 
        play_description = "Justin Fields kneels for -1 yards"
        returns: {
            "player": "Justin Fields"
        }
    """
    expressions = {
        'player': pc.PLAYER
    }
    pattern = r"%(player)s kneels" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)
