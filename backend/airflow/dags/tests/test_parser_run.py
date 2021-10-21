import pbp_parser 
import play_examples


class TestParseRun:

    def test_run_parsing_all_examples(self):
        """
        Test that the RUN play parser matches only run plays
        """
        play_examples.check_across_all_examples('RUN', pbp_parser.parse_run_play)


    def test_run_no_direction_parsing_all_examples(self):
        """
        Test that the RUN_NO_DIRECTION play parser matches only run plays
        """
        play_examples.check_across_all_examples('RUN_NO_DIRECTION', pbp_parser.parse_run_no_direction_play)


    def test_run_play(self):
        """
        Test match dict from normal run play
        """
        description = 'David Montgomery right tackle for 10 yards'
        expected = {
            'runner': 'David Montgomery',
            'direction': 'right tackle',
            'distance': '10 yards',
            'tackler': None
        }
        match = pbp_parser.parse_run_play(description)
        assert match and (match.groupdict() == expected)


    def test_run_play_no_gain(self):
        """
        Test match dict from run play with no gain
        """
        description = 'David Montgomery right guard for no gain'
        expected = {
            'runner': 'David Montgomery',
            'direction': 'right guard',
            'distance': 'no gain',
            'tackler': None
        }
        match = pbp_parser.parse_run_play(description)
        assert match and (match.groupdict() == expected)


    def test_run_play_with_tackle(self):
        """
        Test match dict from run play with a tackle
        """
        description1 = "David Montgomery up the middle for 30 yards (tackle by Aaron Donald)"
        description2 = "David Montgomery right end for 1 yard (tackle by Aaron Donald and Jalen Ramsey)"
        expected1 = {
            'runner': 'David Montgomery',
            'direction': 'up the middle',
            'distance': '30 yards',
            'tackler': 'Aaron Donald'
        }
        expected2 = {
            'runner': 'David Montgomery',
            'direction': 'right end',
            'distance': '1 yard',
            'tackler': 'Aaron Donald and Jalen Ramsey'
        }
        match1 = pbp_parser.parse_run_play(description1)
        match2 = pbp_parser.parse_run_play(description2)

        assert match1 and (match1.groupdict() == expected1)
        assert match2 and (match2.groupdict() == expected2)


    def test_run_play_with_touchdown(self):
        """
        Test match dict run play with a touchdown
        """
        description = "David Montgomery left end for 30 yards, touchdown"
        expected = {
            'runner': 'David Montgomery',
            'direction': 'left end',
            'distance': '30 yards',
            'tackler': None
        }
        match = pbp_parser.parse_run_play(description)
        assert match and (match.groupdict() == expected)


    def test_run_no_direction_play(self):
        """
        Test match dict run play with no direction
        """
        description = "David Montgomery for 30 yards"
        expected = {
            'runner': 'David Montgomery',
            'distance': '30 yards',
            'tackler': None
        }
        match = pbp_parser.parse_run_no_direction_play(description)
        assert match and (match.groupdict() == expected)

