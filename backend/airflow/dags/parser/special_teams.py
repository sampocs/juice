import re
from . import play_components as pc
from . import core

def parse_kickoff_touchback(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a KICKOFF TOUCHBACK,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    KICKOFF TOUCHBACKS should be of the form:
        {Player Name} kicks off {distance}, touchback.

    Example: 
        play_description = "Robbie Gould kicks off 65 yards, touchback"
        returns: {
            "kicker": "Robbie Gould", 
            "kick_distance": "65 yards"
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES)
    }

    pattern = r"%(kicker)s kicks off %(distance)s, touchback" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_kickoff_returned(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a KICKOFF RETURNED,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    KICKOFF RETURNED should be of the form:
        {Player Name} kicks off {distance}, returned by {Player Name} for {distance} [(tackle by {tackler})]

    Example: 
        play_description = "Robbie Gould kicks off 73 yards, returned by Cordarrelle Patterson for 54 yards"
        returns: {
            "kicker": "Robbie Gould", 
            "kick_distance": "73 yards", 
            "returner": "Cordarrelle Patterson",
            "return_distance": "54 yards",
            "tackler": None
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'kick_distance': r"|".join(pc.DISTANCES),
        'returner': pc.PLAYER,
        'return_distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"%(kicker)s kicks off %(kick_distance)s, returned by %(returner)s for %(return_distance)s%(tackler)s" % expressions

    return re.search(pattern, play_description)


def parse_kickoff_out_of_bounds(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a KICKOFF OUT OF BOUNDS,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    KICKOFF OUT OF BOUNDS should be of the form:
        {Player Name} kicks off {distance}, out of bounds

    Example: 
        play_description = "Robbie Gould kicks off 73 yards, out of bounds"
        returns: {
            "kicker": "Robbie Gould", 
            "kick_distance": "73 yards"
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'kick_distance': r"|".join(pc.DISTANCES)
    }

    pattern = r"%(kicker)s kicks off %(kick_distance)s, out of bounds" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_field_goal(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a FIELD_GOAL,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    FIELD_GOAL should be of the form:
        {Player Name} {distance} field goal {good | no good}

    Example: 
        play_description = "Robbie Gould 43 yard field goal good"
        returns: {
            "kicker": "Robbie Gould", 
            "distance": "43 yards", 
            "status": "good"
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES),
        'status': r"|".join(pc.FIELD_GOAL_STATUSES)
    }

    pattern = r"%(kicker)s %(distance)s field goal %(status)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_extra_point(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a EXTRA_POINT,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    EXTRA_POINT should be of the form:
        {Player Name} kicks extra point {good | no good}

    Example: 
        play_description = "Robbie Gould kicks extra point good"
        returns: {
            "kicker": "Robbie Gould", 
            "status": "good"
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'status': r"|".join(pc.FIELD_GOAL_STATUSES)
    }

    pattern = r"%(kicker)s kicks extra point %(status)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_out_of_bounds(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_OUT_OF_BOUNDS,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_OUT_OF_BOUNDS should be of the form:
        {Player Name} punts {distance} out of bounds

    Example: 
        play_description = "Pat O'Donnell punts 45 yards out of bounds"
        returns: {
            "punter": "Pat O'Donnell", 
            "distance": "45 yards"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES)
    }

    pattern = r"%(punter)s punts %(distance)s out of bounds" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_downed(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_DOWNED,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_DOWNED should be of the form:
        {Player Name} punts {distance} downed by {Player Name}

    Example: 
        play_description = "Pat O'Donnell punts 45 yards downed by Cordarrelle Patterson"
        returns: {
            "punter": "Pat O'Donnell", 
            "distance": "45 yards",
            "downer": "Cordarrelle Patterson"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'distance': r"|".join(pc.DISTANCES),
        'downer': pc.PLAYER
    }

    pattern = r"%(punter)s punts %(distance)s downed by %(downer)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_fair_catch(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_FAIR_CATCH,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_FAIR_CATCH should be of the form:
        {Player Name} punts {distance}, fair catch by {Player Name} at {yardage}

    Example: 
        play_description = "Pat O'Donnell punts 45 yards, fair catch by Cordarrelle Patterson at DET-10"
        returns: {
            "punter": "Pat O'Donnell", 
            "punt_distance": "45 yards",
            "returner": "Cordarrelle Patterson",
            "yardage": "DET-10"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'punt_distance': r"|".join(pc.DISTANCES),
        'returner': pc.PLAYER,
        'yardage': pc.YARDAGE
    }

    pattern = r"%(punter)s punts %(punt_distance)s, fair catch by %(returner)s at %(yardage)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_returned(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_RETURNED,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_RETURNED should be of the form:
        {Player Name} punts {distance}, returned by {Player Name} for {distance} [(tackle by {tackler})]

    Example: 
        play_description = "Pat O'Donnell punts 45 yards, returned by Cordarrelle Patterson for 27 yards"
        returns: {
            "punter": "Pat O'Donnell", 
            "punt_distance": "45 yards",
            "returner": "Cordarrelle Patterson",
            "return_distance": "27 yards",
            "tackler": None
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'punt_distance': r"|".join(pc.DISTANCES),
        'returner': pc.PLAYER,
        'return_distance': r"|".join(pc.DISTANCES),
        'tackler': pc.PLAYER
    }
    expressions = core.wrap_expressions(expressions)
    expressions = core.replace_tackler_with_tackle_event(expressions)

    pattern = r"%(punter)s punts %(punt_distance)s, returned by %(returner)s for %(return_distance)s%(tackler)s" % expressions

    return re.search(pattern, play_description)


def parse_punt_recovered(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_RECOVERED,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_RECOVERED should be of the form:
        {Player Name} punts {distance}, recovered by {Player Name} at {yardage}

    Example: 
        play_description = "Pat O'Donnell punts 45 yards, recovered by Cordarrelle Patterson at CHI-10"
        returns: {
            "punter": "Pat O'Donnell", 
            "punt_distance": "45 yards",
            "recoverer": "Cordarrelle Patterson",
            "yardage": "CHI-10"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'punt_distance': r"|".join(pc.DISTANCES),
        'recoverer': pc.PLAYER,
        'yardage': pc.YARDAGE
    }

    pattern = r"%(punter)s punts %(punt_distance)s, recovered by %(recoverer)s at %(yardage)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_touchback(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_TOUCHBACK,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_TOUCHBACK should be of the form:
        {Player Name} punts {distance}, touchback

    Example: 
        play_description = "Pat O'Donnell punts 45 yards, touchback"
        returns: {
            "punter": "Pat O'Donnell", 
            "punt_distance": "45 yards"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'punt_distance': r"|".join(pc.DISTANCES)
    }

    pattern = r"%(punter)s punts %(punt_distance)s, touchback" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_blocked(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PUNT_BLOCKED,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PUNT_BLOCKED should be of the form:
        {Player Name} punts blocked by {Player Name}

    Example: 
        play_description = "Pat O'Donnell punts blocked by Miles Killebrew"
        returns: {
            "punter": "Pat O'Donnell", 
            "blocker": "Miles Killebrew"
        }
    """
    expressions = {
        'punter': pc.PLAYER,
        'blocker': pc.PLAYER
    }

    pattern = r"%(punter)s punts blocked by %(blocker)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_onside_kick(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a ONSIDE_KICK,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    ONSIDE_KICK should be of the form:
        {Player Name} kicks onside {distance}, returned by {Player Name} for {distance}

    Example: 
        play_description = "Robbie Gould kicks onside 9 yards, returned by Cordarrelle Patterson for 5 yards"
        returns: {
            "kicker": "Robbie Gould",
            "kick_distance": "9 yards"
        }
    """
    expressions = {
        'kicker': pc.PLAYER,
        'kick_distance': r"|".join(pc.DISTANCES)
    }

    pattern = r"%(kicker)s kicks onside %(kick_distance)s" % core.wrap_expressions(expressions)

    return re.search(pattern, play_description)