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
    def test_sack_full_all_examples(self):
        """
        Test that the SACK_FULL play parser matches penalties
        """
        play_examples.check_across_all_examples('SACK_FULL', pbp_parser.parse_sack_full)


    def test_sack_half_all_examples(self):
        """
        Test that the SACK_HALF play parser matches penalties
        """
        play_examples.check_across_all_examples('SACK_HALF', pbp_parser.parse_sack_half)


    def test_sack_full(self):
        """
        Test match dict from sack full
        """
        description = 'Aaron Rodgers sacked by Khalil Mack for -10 yards'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'sacker': 'Khalil Mack',
            'distance': '-10 yards'
        }
        match = pbp_parser.parse_sack_full(description)
        assert match and (match.groupdict() == expected)


    def test_sack_half(self):
        """
        Test match dict from sack half
        """
        description = 'Aaron Rodgers sacked by and Khalil Mack for -10 yards and Akiem Hicks for -10 yards'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'sacker1': 'Khalil Mack',
            'sacker2': 'Akiem Hicks',
            'distance1': '-10 yards',
            'distance2': '-10 yards'
        }
        match = pbp_parser.parse_sack_half(description)
        assert match and (match.groupdict() == expected)


    def test_interception_all_examples(self):
        """
        Test that the INTERCEPTION play parser matches interceptions
        """
        play_examples.check_across_all_examples('INTERCEPTION', pbp_parser.parse_interception)


    def test_interception(self):
        """
        Test match dict from interception
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10 and returned for 45 yards (tackle by Davante Adams)'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': 'short right',
            'defender': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': '45 yards',
            'tackler': 'Davante Adams'
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_tackle(self):
        """
        Test match dict from interception with no tackle
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10 and returned for 45 yards'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': 'short right',
            'defender': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': '45 yards',
            'tackler': None
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_return(self):
        """
        Test match dict from interception with no return
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': 'short right',
            'defender': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)

    def test_interception_no_receiver(self):
        """
         Test match dict from interception with no reciever
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': 'short right',
            'defender': 'Jaylon Johnson',
            'receiver': None,
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_defender(self):
        """
        Test match dict from interception with no defender
        """
        description = 'Aaron Rodgers pass short right intended for Davante Adams is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': 'short right',
            'defender': None,
            'receiver': 'Davante Adams',
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_direction(self):
        """
        Test match dict from interception with no direction
        """
        """
        Test match dict from interception with no defender
        """
        description = 'Aaron Rodgers pass is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'direction': None,
            'defender': None,
            'receiver': None,
            'intercepter': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_fumble_all_examples(self):
        """
        Test that the FUMBLE play parser matches penalties
        """
        play_examples.check_across_all_examples('FUMBLE', pbp_parser.parse_fumble)


    def test_fumble(self):
        """
        Test match dict from a fumble
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10 and returned for -10 yards (tackle by Davante Adams)'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'forcer': 'Khalil Mack',
            'recoverer': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'return_distance': '-10 yards',
            'tackler': 'Davante Adams'
        }
        match = pbp_parser.parse_fumble(description)
        assert match and (match.groupdict() == expected)

    
    def test_fumble_no_return_tackle(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10 and returned for -10 yards'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'forcer': 'Khalil Mack',
            'recoverer': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'return_distance': '-10 yards',
            'tackler': None
        }
        match = pbp_parser.parse_fumble(description)
        assert match and (match.groupdict() == expected)


    def test_fumble_no_return(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'forcer': 'Khalil Mack',
            'recoverer': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_fumble(description)
        assert match and (match.groupdict() == expected)


    def test_fumble_no_force(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles, recovered by Akiem Hicks at CHI-10'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'forcer': None,
            'recoverer': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'return_distance': None,
            'tackler': None
        }
        match = pbp_parser.parse_fumble(description)
        assert match and (match.groupdict() == expected)


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
