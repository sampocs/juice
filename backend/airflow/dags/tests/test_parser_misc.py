import play_examples
from parser import misc

class TestParsePenalty:

    def test_penalty_all_examples(self):
        """
        Test that the PENALTY play parser matches penalties
        """
        play_examples.check_across_all_examples('PENALTY', misc.parse_penalty)


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
        match = misc.parse_penalty(description)
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
        match = misc.parse_penalty(description)
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
        match = misc.parse_penalty(description)
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
        match = misc.parse_penalty(description)
        assert match and (match.groupdict() == expected)




class TestParseMisc:

    def test_timeout_all_examples(self):
        """
        Test that the TIMEOUT matches 
        """
        play_examples.check_across_all_examples('TIMEOUT', misc.parse_timeout)


    def test_timeout(self):
        """
        Test match dict from timeout
        """
        description = 'Timeout #1 by Chicago Bears'
        expected = {
            'timeout_number': '#1',
            'team': 'Chicago Bears',
        }
        match = misc.parse_timeout(description)
        assert match and (match.groupdict() == expected)


    def test_spike_all_examples(self):
        """
        Test that the SPIKE matches 
        """
        play_examples.check_across_all_examples('SPIKE', misc.parse_spike)
    

    def test_spike(self):
        """
        Test match dict from spike
        """
        description = 'Justin Fields spiked the ball'
        expected = {
            'player': 'Justin Fields',
        }
        match = misc.parse_spike(description)
        assert match and (match.groupdict() == expected)


    def test_kneel_all_examples(self):
        """
        Test that KNEELs match
        """
        play_examples.check_across_all_examples('KNEEL', misc.parse_kneel)


    def test_kneel(self):
        """
        Test match dict from kneel
        """
        description = 'Justin Fields kneels for -1 yards'
        expected = {
            'player': 'Justin Fields',
        }
        match = misc.parse_kneel(description)
        assert match and (match.groupdict() == expected)
