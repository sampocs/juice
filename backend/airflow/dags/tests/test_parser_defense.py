import re
import parser.play_components as pc
import play_examples 
from parser import defense 

class TestParseSack:

    def test_sack_full_all_examples(self):
        """
        Test that the SACK_FULL play parser matches penalties
        """
        play_examples.check_across_all_examples('SACK_FULL', defense.parse_sack_full)


    def test_sack_half_all_examples(self):
        """
        Test that the SACK_HALF play parser matches penalties
        """
        play_examples.check_across_all_examples('SACK_HALF', defense.parse_sack_half)


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
        match = defense.parse_sack_full(description)
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
        match = defense.parse_sack_half(description)
        assert match and (match.groupdict() == expected)


class TestParseInterception:

    def test_interception_all_examples(self):
        """
        Test that the INTERCEPTION play parser matches interceptions
        """
        play_examples.check_across_all_examples('INTERCEPTION', defense.parse_interception)


    def test_interception(self):
        """
        Test match dict from interception
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10 and returned for 45 yards (tackle by Davante Adams)'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'pass_defended_by': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': '45 yards',
            'tackler': 'Davante Adams'
        }
        match = defense.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_tackle(self):
        """
        Test match dict from interception with no tackle
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10 and returned for 45 yards'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'pass_defended_by': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': '45 yards',
            'tackler': None
        }
        match = defense.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_return(self):
        """
        Test match dict from interception with no return
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) intended for Davante Adams is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'pass_defended_by': 'Jaylon Johnson',
            'receiver': 'Davante Adams',
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': None,
            'tackler': None
        }
        match = defense.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_receiver(self):
        """
         Test match dict from interception with no reciever
        """
        description = 'Aaron Rodgers pass short right (defended by Jaylon Johnson) is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'pass_defended_by': 'Jaylon Johnson',
            'receiver': None,
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': None,
            'tackler': None
        }
        match = defense.parse_interception(description)
        assert match and (match.groupdict() == expected)


    def test_interception_no_defender(self):
        """
        Test match dict from interception with no defender
        """
        description = 'Aaron Rodgers pass short right intended for Davante Adams is intercepted by Eddie Jackson at CHI-10'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'pass_defended_by': None,
            'receiver': 'Davante Adams',
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': None,
            'tackler': None
        }
        match = defense.parse_interception(description)
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
            'pass_direction': None,
            'pass_defended_by': None,
            'receiver': None,
            'intercepted_by': 'Eddie Jackson',
            'yardage': 'CHI-10',
            'interception_return_distance': None,
            'tackler': None
        }
        match = defense.parse_interception(description)
        assert match and (match.groupdict() == expected)


class TestParseFumble:

    def test_fumble_all_examples(self):
        """
        Test that the FUMBLE play parser matches penalties
        """
        play_examples.check_across_all_examples('FUMBLE', defense.parse_fumble)


    def test_fumble(self):
        """
        Test match dict from a fumble
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10 and returned for -10 yards (tackle by Davante Adams)'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'fumble_forced_by': 'Khalil Mack',
            'fumble_recovered_by': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'fumble_return_distance': '-10 yards',
            'tackler': 'Davante Adams'
        }
        match = defense.parse_fumble(description)
        assert match and (match.groupdict() == expected)

    
    def test_fumble_no_return_tackle(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10 and returned for -10 yards'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'fumble_forced_by': 'Khalil Mack',
            'fumble_recovered_by': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'fumble_return_distance': '-10 yards',
            'tackler': None
        }
        match = defense.parse_fumble(description)
        assert match and (match.groupdict() == expected)


    def test_fumble_no_return(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles (forced by Khalil Mack), recovered by Akiem Hicks at CHI-10'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'fumble_forced_by': 'Khalil Mack',
            'fumble_recovered_by': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'fumble_return_distance': None,
            'tackler': None
        }
        match = defense.parse_fumble(description)
        assert match and (match.groupdict() == expected)


    def test_fumble_no_force(self):
        """
        Test match dict from a fumble with a return but no tackle
        """
        description = 'Aaron Rodgers fumbles, recovered by Akiem Hicks at CHI-10'
        expected = {
            'fumbler': 'Aaron Rodgers',
            'fumble_forced_by': None,
            'fumble_recovered_by': 'Akiem Hicks',
            'yardage': 'CHI-10',
            'fumble_return_distance': None,
            'tackler': None
        }
        match = defense.parse_fumble(description)
        assert match and (match.groupdict() == expected)
