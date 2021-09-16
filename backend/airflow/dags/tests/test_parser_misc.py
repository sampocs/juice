import pbp_parser 
import play_examples


class TestParsePenalty:

    def test_penalty_all_examples(self):
        """
        Test that the PENALTY play parser matches penalties
        """
        play_examples.check_across_all_examples('PENALTY', pbp_parser.parse_penalty)


    def test_penalty(self):
        """
        Test match dict from penalty
        """
        description = 'Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards'
        expected = {
            'player': 'Ndamukong Suh',
            'penalty': 'Unnecessary Roughness',
            'distance': '15 yards',
            'no_play': None
        }
        match = pbp_parser.parse_penalty(description)
        assert match and (match.groupdict() == expected)


    def test_penalty_no_play(self):
        """
        Test match dict from penalty with (no play)
        """
        description = 'Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards (no play)'
        expected = {
            'player': 'Ndamukong Suh',
            'penalty': 'Unnecessary Roughness',
            'distance': '15 yards',
            'no_play': 'no play'
        }
        match = pbp_parser.parse_penalty(description)
        assert match and (match.groupdict() == expected)


    def test_penalty_facemask(self):
        """
        Test match dict from penalty with 15 yard facemask
        """
        description = 'Penalty on Ndamukong Suh: Face Mask (15 yards), 15 yards'
        expected = {
            'player': 'Ndamukong Suh',
            'penalty': 'Face Mask (15 yards)',
            'distance': '15 yards',
            'no_play': None
        }
        match = pbp_parser.parse_penalty(description)
        assert match and (match.groupdict() == expected)

    # Timeout
    # Spike
    # Penalty
    # Sack
    # Fumble
    # Interception
