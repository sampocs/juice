import play_examples
from parser import pass_

class TestParsePassComplete:

    def test_pass_complete_parsing_all_examples(self):
        """
        Test that the PASS_COMPLETE play parser matches only completed pass plays
        """
        play_examples.check_across_all_examples('PASS_COMPLETE', pass_.parse_pass_complete_play)


    def test_pass_complete(self):
        """
        Test match dict for a completed pass play
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards'
        expected = {
            'quarterback': 'Justin Fields',
            'pass_direction': 'deep right',
            'receiver': 'Allen Robinson',
            'pass_distance': '45 yards',
            'tackler': None
        }
        match = pass_.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_no_direction(self):
        """
        Test match dict for a completed pass play without a direction
        """
        description = 'Justin Fields pass complete to Allen Robinson for 45 yards'
        expected = {
            'quarterback': 'Justin Fields',
            'pass_direction': None,
            'receiver': 'Allen Robinson',
            'pass_distance': '45 yards',
            'tackler': None
        }
        match = pass_.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_with_tackle(self):
        """
        Test match dict for a completed pass play with a tackle
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards (tackle by Jalen Ramsey)'
        expected = {
            'quarterback': 'Justin Fields',
            'pass_direction': 'deep right',
            'receiver': 'Allen Robinson',
            'pass_distance': '45 yards',
            'tackler': 'Jalen Ramsey'
        }
        match = pass_.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_with_touchdown(self):
        """
        Test match dict for a completed pass play with a touchdown
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards, touchdown'
        expected = {
            'quarterback': 'Justin Fields',
            'pass_direction': 'deep right',
            'receiver': 'Allen Robinson',
            'pass_distance': '45 yards',
            'tackler': None
        }
        match = pass_.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)


class TestParsePassIncomplete:

    def test_pass_incomplete_parsing_all_examples(self):
        """
        Test that the PASS_INCOMPLETE play parser matches only incomplete pass plays
        """
        play_examples.check_across_all_examples('PASS_INCOMPLETE', pass_.parse_pass_incomplete_play)


    def test_pass_incomplete(self):
        """
        Test match dict for a incompleted pass play 
        """
        description = 'Aaron Rodgers pass incomplete short right intended for Davante Adams'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'receiver': 'Davante Adams',
            'pass_defended_by': None
        }
        match = pass_.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_incomplete_no_direction(self):
        """
        Test match dict for a incompleted pass play without a direction
        """
        description = 'Aaron Rodgers pass incomplete intended for Davante Adams'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': None,
            'receiver': 'Davante Adams',
            'pass_defended_by': None
        }
        match = pass_.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)


    def test_pass_incomplete_no_intended_for(self):
        """
        Test match dict for a incompleted pass play without a reciever
        """
        description1 = 'Aaron Rodgers pass incomplete short right'
        expected1 = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'receiver': None,
            'pass_defended_by': None
        }

        description2 = 'Aaron Rodgers pass incomplete'
        expected2 = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': None,
            'receiver': None,
            'pass_defended_by': None
        }

        match1 = pass_.parse_pass_incomplete_play(description1)
        match2 = pass_.parse_pass_incomplete_play(description2)

        assert match1 and (match1.groupdict() == expected1)  
        assert match2 and (match2.groupdict() == expected2)  


    def test_pass_incomplete_with_defender(self):
        """
        Test match dict for a incompleted pass play with a defender
        """
        description = 'Aaron Rodgers pass incomplete short right intended for Davante Adams (defended by Jaylon Johnson)'
        expected = {
            'quarterback': 'Aaron Rodgers',
            'pass_direction': 'short right',
            'receiver': 'Davante Adams',
            'pass_defended_by': 'Jaylon Johnson'
        }
        match = pass_.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)
