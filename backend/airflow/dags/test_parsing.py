import re
import constants as c
import pbp_parser 

players = ['First Last', 'First Middle Last', 'First Last-Last', 'First L"Last', "First L'Last"]

distances = [
    'no gain',
    '1 yard',
    '2 yards', 
    '-1 yards',
    '-10 yards',
    '20 yards'
]

tacklers = [
    '',
    *[f'(tackle by {player})' for player in players],
    *[f'(tackle by {player} and {player})' for player in players]
]

defenders = [
    '', 
    *[f'(defended by {player}' for player in players]
]

touchdowns = [
    '',
    ', touchdown'
]

def test_regex_wrapper():
    assert pbp_parser.regex_wrapper({'key1': r"value"}) == {'key1': r"(?P<key1>value)"}

    examples = {
        'key1': r"value",
        'key2': r"\d+",
        'key3': r"[+-]?\d+\.\d\d"
    }
    test_string = 'value 12345 +30.02'
    test_regex = r"%(key1)s %(key2)s %(key3)s" % pbp_parser.regex_wrapper(examples)
    expected_matching = {
        'key1': 'value',
        'key2': '12345',
        'key3': '+30.02'
    }
    assert re.match(test_regex, test_string).groupdict() == expected_matching

def get_run_plays():
    return [
        f'{player} {direction} for {distance}{tackler}'
        for player in players
        for direction in c.RUN_DIRECTIONS
        for distance in distances
        for tackler in tacklers
    ]

def get_complete_pass_plays():
    return [
        f'{player} pass complete {direction} to {player} for {distance}{tackler}{touchdown}'
        for player in players
        for direction in c.PASS_DIRECTIONS
        for distance in distances
        for tackler in tacklers
        for touchdown in touchdowns
    ]

def get_incomplete_pass_plays():
    return [
        f'{player} pass incomplete {direction} intended for {player}{defender}'
        for player in players
        for direction in c.PASS_DIRECTIONS
        for defender in defenders
    ]

def test_run_parsing():
    for test_string in get_run_plays():
        assert pbp_parser.run_play(test_string), f'No match with run play regex: {test_string}'

    for test_string in get_complete_pass_plays() + get_incomplete_pass_plays():
        assert pbp_parser.run_play(test_string) is None, f'Test string not a run play but matched regex: "{test_string}"'

def test_complete_pass_parsing():
    for test_string in get_complete_pass_plays():
        assert pbp_parser.complete_pass(test_string), f'No match with completed pass regex: "{test_string}"'
    
    for test_string in get_run_plays() + get_incomplete_pass_plays():
        assert pbp_parser.complete_pass(test_string) is None, f'Test string not a completed pass play but matched regex: "{test_string}"'

def test_incomplete_pass_parsing():
    for test_string in get_incomplete_pass_plays():
        assert pbp_parser.incomplete_pass(test_string), f'No match with incomplete pass regex: "{test_string}"'
    
    for test_string in get_run_plays() + get_complete_pass_plays():
        assert pbp_parser.incomplete_pass(test_string) is None, f'Test string not an incompleted pass play but matched regex: "{test_string}"'