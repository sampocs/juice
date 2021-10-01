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

YARDAGE_EXAMPLES = [
    'CHI-1',
    'CHI-10',
    'CHI-45',
    'SF-5',
    'SF-14',
    'SF-49'
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

# Ex: (forced by Khalil Mack)
FORCE_EXAMPLES = [
    '',
    *[f' (forced by {player})' for player in PLAYER_EXAMPLES]
]

# Ex: and returned for 35 yards (tackle by Davante Adams)
RETURN_DISTANCE_EXAMPLES = [
    '',
    *[f'and returned for {distance}{tackler}' 
        for distance in DISTANCE_EXAMPLES 
        for tackler in TACKLER_EXAMPLES]
]

TOUCHDOWN_EXAMPLES = [
    '', # no touchdown
    ', touchdown'
]

PENALTY_NAME_EXAMPLES = [
    'Unnecessary Roughness',
    'Offensive Holding',
    'Defensive Holding (Offsetting)',
    'Defensive Pass Interference',
    'Face Mask (15 Yards)',
    'Player Out of Bounds on Kick'
]

PENALTY_RESPONSE_EXAMPLES = [
    '',
    *[f' ({response})' for response in pc.PENALTY_RESPONSES]
]

TEAM_EXAMPLES = [
    'Chicago Bears',
    'Washington Football Team',
    'Las Vegas Raiders'
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
     f'{player} pass complete{direction} to {player} for {distance}{tackler}{touchdown}'
    for player in PLAYER_EXAMPLES
    for direction in [' ' + direction for direction in pc.PASS_DIRECTIONS] + ['']
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

# Ex: Aaron Rodgers sacked by Khalil Mack for -10 yards
SACK_FULL_EXAMPLES = [
    f'{quarterback} sacked by {sacker} for {distance}'
    for quarterback in PLAYER_EXAMPLES
    for sacker in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
]

# Ex: Aaron Rodgers sacked by and Khalil Mack for -10 yards and Akiem Hicks for -10 yards
SACK_HALF_EXAMPLES = [
    f'{quarterback} sacked by and {sacker1} for {distance1} and {sacker2} for {distance2}'
    for quarterback in PLAYER_EXAMPLES
    for sacker1 in PLAYER_EXAMPLES
    for distance1 in DISTANCE_EXAMPLES
    for sacker2 in PLAYER_EXAMPLES
    for distance2 in DISTANCE_EXAMPLES
]

# Ex: Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Khalil Mack and returned for 45 yards
FUMBLE_EXAMPLES = [
    f'{fumbler} fumbles{forcer}, recovered by {recoverer} at {yardage}{return_distance}'
    for fumbler in PLAYER_EXAMPLES
    for forcer in FORCE_EXAMPLES
    for recoverer in PLAYER_EXAMPLES
    for yardage in YARDAGE_EXAMPLES
    for return_distance in RETURN_DISTANCE_EXAMPLES
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

# Ex: Robbie Gould 43 yard field goal good
FIELD_GOAL_EXAMPLES = [
    f'{kicker} {distance} field goal {status}'
    for kicker in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
    for status in pc.FIELD_GOAL_STATUSES
]

# Ex: Robbie Gould kicks extra point good
EXTRA_POINT_EXAMPLES = [
    f'{kicker} kicks extra point {status}'
    for kicker in PLAYER_EXAMPLES
    for status in pc.FIELD_GOAL_STATUSES
]

# Ex: Pat O'Donnell punts 45 yards out of bounds
PUNT_OUT_OF_BOUNDS_EXAMPLES = [
    f'{punter} punts {distance} out of bounds'
    for punter in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
]

# Ex: Pat O'Donnell punts 45 yards downed by Cordarrelle Patterson
PUNT_DOWNED_EXAMPLES = [
    f'{punter} punts {distance} downed by {downer}'
    for punter in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
    for downer in PLAYER_EXAMPLES
]

# Ex: Pat O'Donnell punts 45 yards, fair catch by Cordarrelle Patterson at DET-10
PUNT_FAIR_CATCH_EXAMPLES = [
    f'{punter} punts {distance}, fair catch by {catcher} at {yardage}'
    for punter in PLAYER_EXAMPLES
    for distance in DISTANCE_EXAMPLES
    for catcher in PLAYER_EXAMPLES
    for yardage in YARDAGE_EXAMPLES
]

# Ex: Pat O'Donnell punts 45 yards, returned by Cordarrelle Patterson for 27 yards (tackle by Pat O'Donnell)
PUNT_RETURNED_EXAMPLES = [
    f'{punter} punts {punt_distance}, returned by {returner} for {return_distance}{tackler}'
    for punter in PLAYER_EXAMPLES
    for punt_distance in DISTANCE_EXAMPLES
    for returner in PLAYER_EXAMPLES
    for return_distance in DISTANCE_EXAMPLES
    for tackler in TACKLER_EXAMPLES
]

# Ex: Pat O'Donnell punts 45 yards, recovered by Cordarrelle Patterson at CHI-10
PUNT_RECOVERED_EXAMPLES = [
    f'{punter} punts {punt_distance}, recovered by {recoverer} at {yardage}'
    for punter in PLAYER_EXAMPLES
    for punt_distance in DISTANCE_EXAMPLES
    for recoverer in PLAYER_EXAMPLES
    for yardage in YARDAGE_EXAMPLES
]

# Ex: Pat O'Donnell punts 45 yards, touchback
PUNT_TOUCHBACK_EXAMPLES = [
    f'{punter} punts {punt_distance}, touchback'
    for punter in PLAYER_EXAMPLES
    for punt_distance in DISTANCE_EXAMPLES
]

# Ex: Pat O'Donnell punts blocked by Miles Killebrew
PUNT_BLOCKED_EXAMPLES = [
    f'{punter} punts blocked by {blocker}'
    for punter in PLAYER_EXAMPLES
    for blocker in PLAYER_EXAMPLES
]

# Ex: Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards (no play) 
PENALTY_EXAMPLES = [
    f'Penalty on {player}: {penalty}, {distance}{response}{no_play}'
    for player in PLAYER_EXAMPLES
    for penalty in PENALTY_NAME_EXAMPLES
    for distance in DISTANCE_EXAMPLES
    for response in PENALTY_RESPONSE_EXAMPLES 
    for no_play in [' (no play)', '']
]

TIMEOUT_EXAMPLES = [
    f'Timeout #{i} by {team}'
    for i in range(1, 4)
    for team in TEAM_EXAMPLES
]

SPIKE_EXAMPLES = [
    f'{player} spiked the ball'
    for player in PLAYER_EXAMPLES
]

KNEEL_EXAMPLES = [
    f'{player} kneels for -1 yards'
    for player in PLAYER_EXAMPLES
]

ALL_PLAY_EXAMPLES = {
    'RUN': RUN_EXAMPLES,
    'PASS_COMPLETE': PASS_COMPLETE_EXAMPLES,
    'PASS_INCOMPLETE': PASS_INCOMPLETE_EXAMPLES,
    'SACK_FULL': SACK_FULL_EXAMPLES,
    'SACK_HALF': SACK_HALF_EXAMPLES,
    'FUMBLE': FUMBLE_EXAMPLES,
    'KICKOFF_TOUCHBACK': KICKOFF_TOUCHBACK_EXAMPLES,
    'KICKOFF_RETURNED': KICKOFF_RETURNED_EXAMPLES,
    'FIELD_GOAL': FIELD_GOAL_EXAMPLES,
    'EXTRA_POINT': EXTRA_POINT_EXAMPLES,
    'PUNT_OUT_OF_BOUNDS': PUNT_OUT_OF_BOUNDS_EXAMPLES,
    'PUNT_DOWNED': PUNT_DOWNED_EXAMPLES,
    'PUNT_FAIR_CATCH': PUNT_FAIR_CATCH_EXAMPLES,
    'PUNT_RETURNED': PUNT_RETURNED_EXAMPLES,
    'PUNT_RECOVERED': PUNT_RECOVERED_EXAMPLES,
    'PUNT_TOUCHBACK': PUNT_TOUCHBACK_EXAMPLES,
    'PUNT_BLOCKED': PUNT_BLOCKED_EXAMPLES,
    'PENALTY': PENALTY_EXAMPLES,
    'TIMEOUT': TIMEOUT_EXAMPLES,
    'SPIKE': SPIKE_EXAMPLES,
    'KNEEL': KNEEL_EXAMPLES
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
