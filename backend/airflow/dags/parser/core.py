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


def replace_forcer_with_forced_event(expressions: dict) -> dict:
    """
    Given a dict with the regex for a forced fumble, replaces the expression with the full optional
    string that indicates a forced fumble event
    This means adding the full "forced by" string and making the whole string optional

    Ex: {'forcer': r"(P?<forcer>{forcer_regex}"}
        => {'forcer': r"( (forced by (P?<forcer>{forcer_regex}))?"}
    """
    assert 'forcer' in expressions.keys(), \
        'Must supply the regex for the forcer. "forcer" key must be present in expressions dict'

    forcer_regex = r"\(forced by %s\)" % expressions['forcer']
    expressions['forcer'] = make_optional(forcer_regex)

    return expressions


def replace_return_distance_with_return_event(expressions: dict) -> dict:
    """
    Given a dict with the regex for a returned fumble distance, replaces the expression with the full optional
    string that indicates a returned event
    This means adding the full "returned for" string and making the whole string optional

    Ex: {'return_distance': r"(P?<return_distance>{distance_regex}"}
        => {'return_distance': r"( and returned for (P?<return_distance>{distance_regex})?"}
    """
    assert 'return_distance' in expressions.keys(), \
        'Must supply the regex for the return distance. "return_distance" key must be present in expressions dict'

    distance_regex = r"and returned for (%s)" % expressions['return_distance']
    expressions['return_distance'] = make_optional(distance_regex)

    return expressions