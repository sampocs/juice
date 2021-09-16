from typing import Callable
import play_components as pc

PLAYER_EXAMPLES = [
    'First Last', 
    'First Middle Last', 
    'First Last-Last', 
    'First St. Last', 
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
    for direction in pc.RUN_DIRECTIONS
    for distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
]

# Ex: Justin Fields pass complete deep right to Allen Robinson for 45 yards, touchdown
PASS_COMPLETE_EXAMPLES = [
     f'{player} pass complete {direction} to {player} for {distance}{tackler}{touchdown}'
    for player in PLAYER_EXAMPLES
    for direction in pc.PASS_DIRECTIONS
    for distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
    for touchdown in TOUCHDOWN_EXAMPLES
]

# Ex: Aaron Rodgers pass incomplete short right intended for Davante Adams (defended by Jaylon Johnson)
PASS_INCOMPLETE_EXAMPLES = [
    f'{player} pass incomplete {direction} intended for {player}{defender}'
    for player in PLAYER_EXAMPLES
    for direction in pc.PASS_DIRECTIONS
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