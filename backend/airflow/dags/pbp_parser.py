import re
import play_components as pc


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
        >>> re.search(pattern, "2021 01").groupdict()
        {"year": "2021", "month": "01"}
    """
    return {var: r"(?P<%s>%s)" % (var, regex) for (var, regex) in expressions.items()}


def make_optional(expression: str, space_prefix: bool = True) -> str:
    """
    Makes a regex expression optional by adding parenthesis and a ?
    """
    prefix = r"( " if space_prefix else r"("
    return prefix + (r"%s)?" % expression)


def replace_tackler_with_tackle_event(expressions: dict) -> dict:
    """
    Given a dict with the regex for a tackler, replaces the expression with the full optional
    string that indicates a tackle event
    This means adding the full "tackle by" string and making the whole string optional

    Ex: {'tackler': r"(P?<tackler>{tackler_regex}"}
        => {'tackler': r"( (tackle by (P?<tackler>{tackler_regex}))?"}
    """
    assert 'tackler' in expressions.keys(), \
        'Must supply the regex for the tackler. "tackler" key must be present in expressions dict'

    tackler_regex = r"\(tackle by %s\)" % expressions['tackler']
    expressions['tackler'] = make_optional(tackler_regex)

    return expressions


def replace_defender_with_defended_event(expressions: dict) -> dict:
    """
    Given a dict with the regex for a defended pass, replaces the expression with the full optional
    string that indicates a defended event
    This means adding the full "defended by" string and making the whole string optional

    Ex: {'defender': r"(P?<defender>{defender_regex}"}
        => {'defender': r"( (defended by (P?<tackler>{defender_regex}))?"}
    """
    assert 'defender' in expressions.keys(), \
        'Must supply the regex for the defender. "defender" key must be present in expressions dict'

    defender_regex = r"\(defended by %s\)" % expressions['defender']
    expressions['defender'] = make_optional(defender_regex)

    return expressions


def replace_receiver_with_intended_event(expressions: dict) -> dict:
    """
    Given a dict with the regex for an intended receiver, replaces the expression with the full optional
    string that indicates a intended event
    This means adding the full "intended for" string and making the whole string optional

    Ex: {'receiver': r"(P?<receiver>{receiver_regex}"}
        => {'receiver': r"( (intended for (P?<receiver>{receiver_regex}))?"}
    """
    assert 'receiver' in expressions.keys(), \
        'Must supply the regex for the receiver. "receiver" key must be present in expressions dict'

    receiver_regex = r"intended for %s" % expressions['receiver']
    expressions['receiver'] = make_optional(receiver_regex)

    return expressions


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
    expressions = wrap_expressions(expressions)
    expressions = replace_tackler_with_tackle_event(expressions)

    pattern = r"%(runner)s %(direction)s for %(distance)s%(tackler)s" % expressions
    return re.search(pattern, play_description)


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
    expressions = wrap_expressions(expressions)
    expressions = replace_tackler_with_tackle_event(expressions)
    expressions['direction'] = make_optional(expressions['direction'])

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
    expressions = wrap_expressions(expressions)
    expressions = replace_defender_with_defended_event(expressions)
    expressions = replace_receiver_with_intended_event(expressions)
    expressions['direction'] = make_optional(expressions['direction'])

    pattern = r"%(passer)s pass incomplete%(direction)s%(receiver)s%(defender)s" % expressions

    return re.search(pattern, play_description)


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

    pattern = r"%(kicker)s kicks off %(distance)s, touchback" % wrap_expressions(expressions)

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
    expressions = wrap_expressions(expressions)
    expressions = replace_tackler_with_tackle_event(expressions)

    pattern = r"%(kicker)s kicks off %(kick_distance)s, returned by %(returner)s for %(return_distance)s%(tackler)s" % expressions

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

    pattern = r"%(kicker)s %(distance)s field goal %(status)s" % wrap_expressions(expressions)

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

    pattern = r"%(kicker)s kicks extra point %(status)s" % wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_punt_out(play_description: str) -> re.Match or None:
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

    pattern = r"%(punter)s punts %(distance)s out of bounds" % wrap_expressions(expressions)

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

    pattern = r"%(punter)s punts %(distance)s downed by %(downer)s" % wrap_expressions(expressions)

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

    pattern = r"%(punter)s punts %(punt_distance)s, fair catch by %(returner)s at %(yardage)s" % wrap_expressions(expressions)

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
    expressions = wrap_expressions(expressions)
    expressions = replace_tackler_with_tackle_event(expressions)

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

    pattern = r"%(punter)s punts %(punt_distance)s, recovered by %(recoverer)s at %(yardage)s" % wrap_expressions(expressions)

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

    pattern = r"%(punter)s punts %(punt_distance)s, touchback" % wrap_expressions(expressions)

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

    pattern = r"%(punter)s punts blocked by %(blocker)s" % wrap_expressions(expressions)

    return re.search(pattern, play_description)


def parse_penalty(play_description: str) -> re.Match or None:
    """
    Given a play by play description, if it's a PENALTY,
    returns the regex match dictionary for each piece of information in the description
    Otherwise, returns None

    PENALTY should be of the form:
        Penalty on {Player Name}: {penalty}, {distance} [(no play)]

    Example: 
        play_description = "Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards"
        returns: {
            "player": "Ndamukong Suh", 
            "penalty": "Unnecessary Roughness",
            "distance": "15 yards",
            "no_play": None
        }
    """
    expressions = {
        'player': pc.PLAYER,
        'penalty': pc.PENALTY,
        'distance': r"|".join(pc.DISTANCES),
        'response': r"|".join(pc.PENALTY_RESPONSES),
        'no_play': pc.NO_PLAY
    }
    expressions = wrap_expressions(expressions)
    expressions['response'] = make_optional(r"\(%s\)" % expressions['response'])
    expressions['no_play'] = make_optional(r"\(%s\)" % expressions['no_play'])

    pattern = r"Penalty on %(player)s: %(penalty)s, %(distance)s%(response)s%(no_play)s" % expressions

    return re.search(pattern, play_description)


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

    pattern = r"Timeout %(timeout_number)s by %(team)s" % wrap_expressions(expressions)

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

    pattern = r"%(player)s spiked the ball" % wrap_expressions(expressions)

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
    pattern = r"%(player)s kneels" % wrap_expressions(expressions)

    return re.search(pattern, play_description)


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
    pattern = r"%(quarterback)s sacked by %(sacker)s for %(distance)s" % wrap_expressions(expressions)

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
    pattern = r"%(quarterback)s sacked by and %(sacker1)s for %(distance1)s and %(sacker2)s for %(distance2)s" % wrap_expressions(expressions)

    return re.search(pattern, play_description)