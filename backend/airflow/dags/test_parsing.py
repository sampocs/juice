import re
import constants as c
import pbp_parser 
from typing import List

PLAYER_EXAMPLES = [
    'First Last', 
    'First Middle Last', 
    'First Last-Last', 
    'First L"Last', 
    "First L'Last"
]

DISTANCE_EXAMPLES = [
    'no gain',
    '1 yard',
    '2 yards', 
    '-1 yards',
    '-10 yards',
    '20 yards'
]

TACKLER_EXAMPLES = [
    '', # no tackler
    *[f'(tackle by {player})' for player in PLAYER_EXAMPLES],
    *[f'(tackle by {player} and {player})' for player in PLAYER_EXAMPLES]
]

DEFENDER_EXAMPLES = [
    '', # no defender
    *[f'(defended by {player}' for player in PLAYER_EXAMPLES]
]

TOUCHDOWN_EXAMPLES = [
    '', # no touchdown
    ', touchdown'
]

def get_example_run_plays() -> List[str]:
    """
    Gets a list of example RUN plays by iterating through different 
    example permutations

    Ex: David Montgomery right tackle for 10 yards, touchdown 
    """
    return [
        f'{player} {direction} for {distance}{tackler}'
        for player in PLAYER_EXAMPLES
        for direction in c.RUN_DIRECTIONS
        for distance in DISTANCE_EXAMPLES
        for tackler in TACKLER_EXAMPLES
    ]


def get_example_completed_pass_plays() -> List[str]:
    """
    Gets a list of example COMPLETED PASS plays by iterating through different 
    example permutations

    Ex: Justin Fields pass complete deep right to Allen Robinson for 45 yards, touchdown
    """
    return [
        f'{player} pass complete {direction} to {player} for {distance}{tackler}{touchdown}'
        for player in PLAYER_EXAMPLES
        for direction in c.PASS_DIRECTIONS
        for distance in DISTANCE_EXAMPLES
        for tackler in TACKLER_EXAMPLES
        for touchdown in TOUCHDOWN_EXAMPLES
    ]


def get_example_incomplete_pass_plays() -> List[str]:
    """
    Gets a list of example INCOMPLETE PASS plays by iterating through different 
    example permutations

    Ex: Aaron Rodgers pass incomplete short right intended for Davante Adams, defended by Jaylon Johnson
    """
    return [
        f'{player} pass incomplete {direction} intended for {player}{defender}'
        for player in PLAYER_EXAMPLES
        for direction in c.PASS_DIRECTIONS
        for defender in DEFENDER_EXAMPLES
    ]


def get_example_kickoff_touchback_plays() -> List[str]:
    """
    Gets a list of example KICKOFF TOUCHBACK plays 

    Ex: Robbie Gould kicks off 65 yards, touchback
    """
    return [
        f'{player} kicks off {distance}, touchback'
        for player in PLAYER_EXAMPLES
        for distance in DISTANCE_EXAMPLES
    ]


def get_example_kickoff_returned_plays() -> List[str]:
    """
    Gets a list of example KICKOFF RETURNED plays 

    Ex: Robbie Gould kicks off 65 yards, returned by returned by Cordarrelle Patterson for 54 yards
    """
    return [
        f'{kicker} kicks off {kick_distance}, returned by {returner} for {return_distance}{tackler}'
        for kicker in PLAYER_EXAMPLES
        for kick_distance in DISTANCE_EXAMPLES
        for returner in PLAYER_EXAMPLES
        for return_distance in DISTANCE_EXAMPLES
        for tackler in TACKLER_EXAMPLES
    ]


def get_example_plays_except(excluded_play_type: str) -> List[str]:
    """
    Get's a list of all the play types, except the one specified as a parameter
    This is for checking that the regex does not match
    """
    assert excluded_play_type in ['run', 'completed_pass', 'incomplete_pass', 'kickoff_touchback', 'kickoff_returned'], \
        f'Invalid play type: {excluded_play_type}'

    all_play_types = []
    if excluded_play_type != 'run':
        all_play_types += get_example_run_plays()

    if excluded_play_type != 'completed_pass':
        all_play_types += get_example_completed_pass_plays()

    if excluded_play_type != 'incomplete_pass':
        all_play_types += get_example_incomplete_pass_plays()

    if excluded_play_type != 'kickoff_touchback':
        all_play_types += get_example_kickoff_touchback_plays()

    if excluded_play_type != 'kickoff_returned':
        all_play_types += get_example_kickoff_returned_plays()

    return all_play_types


def test_wrap_expressions():
    """
    Tests the wrapper to help match variables to regex patterns
    """
    expressions = {
        'year': r"[\d]{4}",
        'month': r"[\d]{2}"
    }
    wrapped_expressions = {
        'year': r"(?P<year>[\d]{4})",
        'month': r"(?P<month>[\d]{2})"
    }
    assert pbp_parser.wrap_expressions(expressions) == wrapped_expressions

    test_string = '2019 01'
    test_regex = r"%(year)s %(month)s" % pbp_parser.wrap_expressions(expressions)
    expected_matching = {
        'year': '2019',
        'month': '01'
    }
    assert re.match(test_regex, test_string).groupdict() == expected_matching


def test_run_parsing():
    """
    Test that the RUN play parser matches only run plays
    """
    for test_string in get_example_run_plays():
        assert pbp_parser.parse_run_play(test_string), \
            f'No match with run play regex: {test_string}'

    for test_string in get_example_plays_except('run'):
        assert pbp_parser.parse_run_play(test_string) is None, \
            f'Test string not a run play but matched regex: "{test_string}"'


def test_completed_pass_parsing():
    """
    Test that the COMPLETED PASS play parser matches only completed pass plays
    """
    for test_string in get_example_completed_pass_plays():
        assert pbp_parser.parse_completed_pass_play(test_string), \
            f'No match with completed pass regex: "{test_string}"'
    
    for test_string in get_example_plays_except('completed_pass'):
        assert pbp_parser.parse_completed_pass_play(test_string) is None, \
            f'Test string not a completed pass play but matched regex: "{test_string}"'


def test_incomplete_pass_parsing():
    """
    Test that the INCOMPLETE PASS play parser matches only incomplete pass plays
    """
    for test_string in get_example_incomplete_pass_plays():
        assert pbp_parser.parse_incomplete_pass_play(test_string), \
            f'No match with incomplete pass regex: "{test_string}"'
    
    for test_string in get_example_plays_except('incomplete_pass'):
        assert pbp_parser.parse_incomplete_pass_play(test_string) is None, \
            f'Test string not an incompleted pass play but matched regex: "{test_string}"'


def test_kickoff_touchback_parsing():
    """
    Test that the KICKOFF TOUCHBACK play parser matches kickoff touchbacks
    """
    for test_string in get_example_kickoff_touchback_plays():
        assert pbp_parser.parse_kickoff_touchback(test_string), \
            f'No match with kickoff touchback regex: "{test_string}"'
    
    for test_string in get_example_plays_except('kickoff_touchback'):
        assert pbp_parser.parse_kickoff_touchback(test_string) is None, \
            f'Test string not a kickoff touchback but matched regex: "{test_string}"'


def test_kickoff_returned_parsing():
    """
    Test that the KICKOFF RETURNED play parser matches only kickoffs returned
    """
    for test_string in get_example_kickoff_returned_plays():
        assert pbp_parser.parse_kickoff_returned(test_string), \
            f'No match with kickoff touchback regex: "{test_string}"'
    
    for test_string in get_example_plays_except('kickoff_returned'):
        assert pbp_parser.parse_kickoff_returned(test_string) is None, \
            f'Test string not a kickoff touchback but matched regex: "{test_string}"'