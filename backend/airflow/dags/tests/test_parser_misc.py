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
            'response': None,
            'no_play': None
        }
        match = pbp_parser.parse_penalty(description)
        assert match and (match.groupdict() == expected)


    def test_penalty_response(self):
        """
        Test match dict with penalty response
        """
        description = 'Penalty on Ndamukong Suh: Unnecessary Roughness, 15 yards (accepted)'
        expected = {
            'player': 'Ndamukong Suh',
            'penalty': 'Unnecessary Roughness',
            'distance': '15 yards',
            'response': 'accepted',
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
            'response': None,
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
            'response': None,
            'no_play': None
        }
        match = pbp_parser.parse_penalty(description)
        assert match and (match.groupdict() == expected)


class TestParseBigDefensivePlay:
    def test_sack_all_examples(self):
        pass

    def test_sack(self):
        pass

    def test_interception_all_examples(self):
        pass

    def test_interception(self):
        pass

    def test_interception_with_tackle(self):
        pass

    def test_fumble_all_examples(self):
        pass

    def test_fumble(self):
        pass

class TestParseMisc:

    def test_timeout_all_examples(self):
        """
        Test that the TIMEOUT matches 
        """
        play_examples.check_across_all_examples('TIMEOUT', pbp_parser.parse_timeout)


    def test_timeout(self):
        """
        Test match dict from timeout
        """
        description = 'Timeout #1 by Chicago Bears'
        expected = {
            'timeout_number': '#1',
            'team': 'Chicago Bears',
        }
        match = pbp_parser.parse_timeout(description)
        assert match and (match.groupdict() == expected)


    def test_spike_all_examples(self):
        """
        Test that the SPIKE matches 
        """
        play_examples.check_across_all_examples('SPIKE', pbp_parser.parse_spike)
    

    def test_spike(self):
        """
        Test match dict from spike
        """
        description = 'Justin Fields spiked the ball'
        expected = {
            'player': 'Justin Fields',
        }
        match = pbp_parser.parse_spike(description)
        assert match and (match.groupdict() == expected)


    def test_kneel_all_examples(self):
        """
        Test that KNEELs match
        """
        play_examples.check_across_all_examples('KNEEL', pbp_parser.parse_kneel)


    def test_kneel(self):
        """
        Test match dict from kneel
        """
        description = 'Justin Fields kneels for -1 yards'
        expected = {
            'player': 'Justin Fields',
        }
        match = pbp_parser.parse_kneel(description)
        assert match and (match.groupdict() == expected)