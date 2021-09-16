import re
import play_components as pc
from play_examples import *
import pbp_parser 


class TestParseCore:
    
    def test_wrap_expressions(self):
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

    
    def test_distance_regex(self):
        """
        Test that the distance regex's are working
        """
        all_distance_pattern = r"|".join(DISTANCE_EXAMPLES)
        for distance in DISTANCE_EXAMPLES:
            assert re.match(all_distance_pattern, distance), \
                f'Example distance ({distance}) did not match distance regex'


    def test_player_regex(self):
        """
        Test that the player regex is working properly
        """
        for player in PLAYER_EXAMPLES:
            assert re.match(pc.PLAYER, player), \
                f'Example player ({player}) did not match Player regex'

