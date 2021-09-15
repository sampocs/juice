import re
import constants as c
import pbp_parser 
from typing import List, Callable

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

# Ex: (tackle by Khalil Mack)
TACKLER_EXAMPLES = [
    '', # no tackler
    *[f'(tackle by {player})' for player in PLAYER_EXAMPLES],
    *[f'(tackle by {player} and {player})' for player in PLAYER_EXAMPLES]
]

# Ex: (defended by Eddie Jackson)
DEFENDER_EXAMPLES = [
    '', # no defender
    *[f'(defended by {player}' for player in PLAYER_EXAMPLES]
]

TOUCHDOWN_EXAMPLES = [
    '', # no touchdown
    ', touchdown'
]

# Ex: David Montgomery right tackle for 10 yards, touchdown 
RUN_EXAMPLES = [
    f'{player} {direction} for {distance}{tackler}'
    for player in PLAYER_EXAMPLES
    for direction in c.RUN_DIRECTIONS
    for distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
]

# Ex: Justin Fields pass complete deep right to Allen Robinson for 45 yards, touchdown
PASS_COMPLETE_EXAMPLES = [
     f'{player} pass complete {direction} to {player} for {distance}{tackler}{touchdown}'
    for player in PLAYER_EXAMPLES
    for direction in c.PASS_DIRECTIONS
    for distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
    for touchdown in TOUCHDOWN_EXAMPLES
]

# Ex: Aaron Rodgers pass incomplete short right intended for Davante Adams, defended by Jaylon Johnson
PASS_INCOMPLETE_EXAMPLES = [
    f'{player} pass incomplete {direction} intended for {player}{defender}'
    for player in PLAYER_EXAMPLES
    for direction in c.PASS_DIRECTIONS
    for defender in DEFENDER_EXAMPLES    
]

# Ex: Robbie Gould kicks off 65 yards, touchback
KICKOFF_TOUCHBACK_EXAMPLES = [
    f'{player} kicks off {distance}, touchback'
    for player in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
]

# Ex: Robbie Gould kicks off 65 yards, returned by returned by Cordarrelle Patterson for 54 yards
KICKOFF_RETURNED_EXAMPLES = [
    f'{kicker} kicks off {kick_distance}, returned by {returner} for {return_distance}{tackler}'
    for kicker in PLAYER_EXAMPLES
    for kick_distance in DISTANCE_EXAMPLES
    for returner in PLAYER_EXAMPLES
    for return_distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
]

ALL_PLAY_EXAMPLES = {
    'RUN': RUN_EXAMPLES,
    'PASS_COMPLETE': PASS_COMPLETE_EXAMPLES,
    'PASS_INCOMPLETE': PASS_INCOMPLETE_EXAMPLES,
    'KICKOFF_TOUCHBACK': KICKOFF_TOUCHBACK_EXAMPLES,
    'KICKOFF_RETURNED': KICKOFF_RETURNED_EXAMPLES
}
ALL_PLAY_TYPES = list(ALL_PLAY_EXAMPLES.keys())


def check_across_all_examples(tested_play_type: str, parser_function: Callable):
    """
    Helper function to test the regex parser methods
    Loops through all examples and tests that the example either matches
      or doesn't match the proper pattern for that play type

    Ex: tested_play_type of RUN and parser function pbp_parser.parse_run_play
      will make sure all RUN examples are successfully parsed, and all other 
      play types are not

    :param tested_play_type: Play type of the current test (e.g. RUN)
    :param parser_function: Function to call that parses that specific play type 
        (e.g. pbp_parser.parse_run_play)
        The function should return a Match object if the parse was successful,
        or None otherwise
    """
    assert tested_play_type in ALL_PLAY_TYPES, \
        f'Invalid play type ({tested_play_type}). Must be one of: {ALL_PLAY_TYPES}'

    for (example_play_type, examples) in ALL_PLAY_EXAMPLES.items():
        for example_string in examples:
            # If the example play type and the tested play type are the same,
            # the parser function should return a Match object
            if example_play_type == tested_play_type:
                assert parser_function(example_string), \
                    f'No match with {tested_play_type} regex: "{example_string}"'

            # If the example play type and the tested play type are different, 
            # the parser should return None
            else:
                assert parser_function(example_string) is None, \
                    f'Test string not a {tested_play_type} regex: "{example_string}"'


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
    check_across_all_examples('RUN', pbp_parser.parse_run_play)


def test_pass_complete_parsing():
    """
    Test that the PASS_COMPLETE play parser matches only completed pass plays
    """
    check_across_all_examples('PASS_COMPLETE', pbp_parser.parse_pass_complete_play)


def test_incomplete_pass_parsing():
    """
    Test that the PASS_INCOMPLETE play parser matches only incomplete pass plays
    """
    check_across_all_examples('PASS_INCOMPLETE', pbp_parser.parse_pass_incomplete_play)


def test_kickoff_touchback_parsing():
    """
    Test that the KICKOFF_TOUCHBACK play parser matches kickoff touchbacks
    """
    check_across_all_examples('KICKOFF_TOUCHBACK', pbp_parser.parse_kickoff_touchback)

def test_kickoff_returned_parsing():
    """
    Test that the KICKOFF_RETURNED play parser matches only kickoffs returned
    """
    check_across_all_examples('KICKOFF_RETURNED', pbp_parser.parse_kickoff_returned)
