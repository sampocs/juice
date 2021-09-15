import re
import constants as c

def wrap_expressions(expressions: dict) -> dict:
    """
    Given a dictionary mapping variable names to regex patterns,
    returns a new dictionary mapping the same variable name to a new regex 
    expression that will return the variable name in the regex .groupdict() function

    New pattern of the form (?P<variable_name>{regex_expr})

    This allows the formation of cleaner and more readable regex compositions 

    Example: 
    **Note, I've used [d] instead of the proper regex to avoid an invalid escape sequence warning

        Input: {"year": r"[d]{4}"}
        Output: {"year": r"(P?<year>[d]{4})"}

    Example Usage:
        >>> regex_components = {"year": r"[d]{4}", "month": r"[d]{2}"}
        >>> pattern = r"%(year)s %(month)s" % wrap_expressions(regex_components)
        >>> re.match(pattern, "2021 01").groupdict()
        {"year": "2021", "month": "01"}
    """
    return {var: r"(?P<%s>%s)" % (var, regex) for (var, regex) in expressions.items()}


def parse_run_play(play_description: str) -> dict or None:
    """
    Given a play by play description, if it's a RUN play,
    returns the regex match dictionary for each piece of information in the description
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
        'runner': c.PLAYER,
        'direction': r"|".join(c.RUN_DIRECTIONS),
        'distance': r"|".join(c.DISTANCES),
        'tackler': c.PLAYER
    }

    pattern = r"%(runner)s %(direction)s for %(distance)s( \(tackle by %(tackler)s\))?" % wrap_expressions(expressions)
    return re.match(pattern, play_description)


def parse_pass_complete_play(play_description: str) -> dict or None:
    """
    Given a play by play description, if it's a PASS_COMPLETE play,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PASS_COMPLETE plays should be of the form:
        {Player Name} pass complete {direction} to {reciever} for {distance} [(tackle by {tackler})]

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
        'passer': c.PLAYER,
        'direction': r"|".join(c.PASS_DIRECTIONS),
        'reciever': c.PLAYER,
        'distance': r"|".join(c.DISTANCES),
        'tackler': c.PLAYER
    }

    pattern = r"%(passer)s pass complete %(direction)s to %(reciever)s for %(distance)s( \(tackle by %(tackler)s\))?" % wrap_expressions(expressions)

    return re.match(pattern, play_description)


def parse_pass_incomplete_play(play_description: str) -> dict or None:
    """
    Given a play by play description, if it's a PASS_INCOMPLETE play,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PASS_INCOMPLETE  plays should be of the form:
        {Player Name} pass incomplete {direction} intended for {reciever} [(defended by {tackler})]

    Example: 
        play_description = "Aaron Rodgers pass incomplete short right intended for Davante Adams, defended by Jaylon Johnson"
        returns: {
            "runner": "Justin Fields", 
            "direction": "deep right", 
            "distance": "45 yards", 
            "tackler": "Jalen Ramsey"
        }
    """
    expressions = {
        'passer': c.PLAYER,
        'direction': r"|".join(c.PASS_DIRECTIONS),
        'reciever': c.PLAYER,
        'defender': c.PLAYER
    }

    pattern = r"%(passer)s pass incomplete %(direction)s intended for %(reciever)s( \(defended by %(defender)s\))?" % wrap_expressions(expressions)

    return re.match(pattern, play_description)


def parse_kickoff_touchback(play_description: str) -> dict or None:
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
        'kicker': c.PLAYER,
        'distance': r"|".join(c.DISTANCES)
    }

    pattern = r"%(kicker)s kicks off %(distance)s, touchback" % wrap_expressions(expressions)

    return re.match(pattern, play_description)


def parse_kickoff_returned(play_description: str) -> dict or None:
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
        'kicker': c.PLAYER,
        'kick_distance': r"|".join(c.DISTANCES),
        'returner': c.PLAYER,
        'return_distance': r"|".join(c.DISTANCES),
        'tackler': c.PLAYER
    }

    pattern = r"%(kicker)s kicks off %(kick_distance)s, returned by %(returner)s for %(return_distance)s( \(tackle by %(tackler)s\))?" % wrap_expressions(expressions)

    return re.match(pattern, play_description)