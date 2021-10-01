import pbp_parser 
import play_examples


class TestParsePassComplete:

    def test_pass_complete_parsing_all_examples(self):
        """
        Test that the PASS_COMPLETE play parser matches only completed pass plays
        """
        play_examples.check_across_all_examples('PASS_COMPLETE', pbp_parser.parse_pass_complete_play)


    def test_pass_complete(self):
        """
        Test match dict for a completed pass play
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards'
        expected = {
            'passer': 'Justin Fields',
            'direction': 'deep right',
            'receiver': 'Allen Robinson',
            'distance': '45 yards',
            'tackler': None
        }
        match = pbp_parser.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_no_direction(self):
        """
        Test match dict for a completed pass play without a direction
        """
        description = 'Justin Fields pass complete to Allen Robinson for 45 yards'
        expected = {
            'passer': 'Justin Fields',
            'direction': None,
            'receiver': 'Allen Robinson',
            'distance': '45 yards',
            'tackler': None
        }
        match = pbp_parser.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_with_tackle(self):
        """
        Test match dict for a completed pass play with a tackle
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards (tackle by Jalen Ramsey)'
        expected = {
            'passer': 'Justin Fields',
            'direction': 'deep right',
            'receiver': 'Allen Robinson',
            'distance': '45 yards',
            'tackler': 'Jalen Ramsey'
        }
        match = pbp_parser.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_complete_with_touchdown(self):
        """
        Test match dict for a completed pass play with a touchdown
        """
        description = 'Justin Fields pass complete deep right to Allen Robinson for 45 yards, touchdown'
        expected = {
            'passer': 'Justin Fields',
            'direction': 'deep right',
            'receiver': 'Allen Robinson',
            'distance': '45 yards',
            'tackler': None
        }
        match = pbp_parser.parse_pass_complete_play(description)
        assert match and (match.groupdict() == expected)


class TestParsePassIncomplete:

    def test_pass_incomplete_parsing_all_examples(self):
        """
        Test that the PASS_INCOMPLETE play parser matches only incomplete pass plays
        """
        play_examples.check_across_all_examples('PASS_INCOMPLETE', pbp_parser.parse_pass_incomplete_play)


    def test_pass_incomplete(self):
        """
        Test match dict for a incompleted pass play 
        """
        description = 'Aaron Rodgers pass incomplete short right intended for Davante Adams'
        expected = {
            'passer': 'Aaron Rodgers',
            'direction': 'short right',
            'receiver': 'Davante Adams',
            'defender': None
        }
        match = pbp_parser.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)

    
    def test_pass_incomplete_no_direction(self):
        """
        Test match dict for a incompleted pass play without a direction
        """
        description = 'Aaron Rodgers pass incomplete intended for Davante Adams'
        expected = {
            'passer': 'Aaron Rodgers',
            'direction': None,
            'receiver': 'Davante Adams',
            'defender': None
        }
        match = pbp_parser.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)


    def test_pass_incomplete_no_intended_for(self):
        """
        Test match dict for a incompleted pass play without a reciever
        """
        description1 = 'Aaron Rodgers pass incomplete short right'
        expected1 = {
            'passer': 'Aaron Rodgers',
            'direction': 'short right',
            'receiver': None,
            'defender': None
        }

        description2 = 'Aaron Rodgers pass incomplete'
        expected2 = {
            'passer': 'Aaron Rodgers',
            'direction': None,
            'receiver': None,
            'defender': None
        }

        match1 = pbp_parser.parse_pass_incomplete_play(description1)
        match2 = pbp_parser.parse_pass_incomplete_play(description2)

        assert match1 and (match1.groupdict() == expected1)  
        assert match2 and (match2.groupdict() == expected2)  


    def test_pass_incomplete_with_defender(self):
        """
        Test match dict for a incompleted pass play with a defender
        """
        description = 'Aaron Rodgers pass incomplete short right intended for Davante Adams (defended by Jaylon Johnson)'
        expected = {
            'passer': 'Aaron Rodgers',
            'direction': 'short right',
            'receiver': 'Davante Adams',
            'defender': 'Jaylon Johnson'
        }
        match = pbp_parser.parse_pass_incomplete_play(description)
        assert match and (match.groupdict() == expected)
