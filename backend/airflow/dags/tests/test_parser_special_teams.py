import pbp_parser 
import play_examples


class TestParseKickoff:

    def test_kickoff_touchback_parsing_all_examples(self):
        """
        Test that the KICKOFF_TOUCHBACK play parser matches kickoff touchbacks
        """
        play_examples.check_across_all_examples('KICKOFF_TOUCHBACK', pbp_parser.parse_kickoff_touchback)


    def test_kickoff_returned_parsing_all_examples(self):
        """
        Test that the KICKOFF_RETURNED play parser matches only kickoffs returned
        """
        play_examples.check_across_all_examples('KICKOFF_RETURNED', pbp_parser.parse_kickoff_returned)


    def test_kickoff_touchback(self):
        """
        Test match dict from kickoff with touchback
        """
        description = 'Robbie Gould kicks off 65 yards, touchback'
        expected = {
            'kicker': 'Robbie Gould',
            'distance': '65 yards',
        }
        match = pbp_parser.parse_kickoff_touchback(description)
        assert match and (match.groupdict() == expected)


    def test_kickoff_returned(self):
        """
        Test match dict from kickoff with return
        """
        description = 'Robbie Gould kicks off 65 yards, returned by Cordarrelle Patterson for 54 yards'
        expected = {
            'kicker': 'Robbie Gould',
            'kick_distance': '65 yards',
            'returner': 'Cordarrelle Patterson',
            'return_distance': '54 yards',
            'tackler': None
        }
        match = pbp_parser.parse_kickoff_returned(description)
        assert match and (match.groupdict() == expected)


    def test_kickoff_returned_with_tackle(self):
        """
        Test match dict from kickoff with return and tackle
        """
        description = 'Robbie Gould kicks off 65 yards, returned by Cordarrelle Patterson for 54 yards (tackle by Robbie Gould)'
        expected = {
            'kicker': 'Robbie Gould',
            'kick_distance': '65 yards',
            'returner': 'Cordarrelle Patterson',
            'return_distance': '54 yards',
            'tackler': 'Robbie Gould'
        }
        match = pbp_parser.parse_kickoff_returned(description)
        assert match and (match.groupdict() == expected)


class TestFieldGoal:

    def test_field_goal_all_examples(self):
        """
        Test that the FIELD_GOAL play parser matches field goals
        """
        play_examples.check_across_all_examples('FIELD_GOAL', pbp_parser.parse_field_goal)


    def test_field_goal_good(self):
        """
        Test match dict from field goal (good)
        """
        description = 'Robbie Gould 43 yard field goal good'
        expected = {
            'kicker': 'Robbie Gould',
            'distance': '43 yard',
            'status': 'good'
        }
        match = pbp_parser.parse_field_goal(description)
        assert match and (match.groupdict() == expected)


    def test_field_goal_no_good(self):
        """
        Test match dict from field goal (no good)
        """
        description = 'Robbie Gould 43 yard field goal no good'
        expected = {
            'kicker': 'Robbie Gould',
            'distance': '43 yard',
            'status': 'no good'
        }
        match = pbp_parser.parse_field_goal(description)
        assert match and (match.groupdict() == expected)


class TestExtraPoint:

    def test_extra_point_all_examples(self):
        """
        Test that the EXTRA_POINT play parser matches field goals
        """
        play_examples.check_across_all_examples('EXTRA_POINT', pbp_parser.parse_extra_point)


    def test_extra_point_good(self):
        """
        Test match dict from extra point (good)
        """
        description = 'Robbie Gould kicks extra point good'
        expected = {
            'kicker': 'Robbie Gould',
            'status': 'good'
        }
        match = pbp_parser.parse_extra_point(description)
        assert match and (match.groupdict() == expected)


    def test_extra_point_no_good(self):
        """
        Test match dict from extra point (no good)
        """
        description = 'Robbie Gould kicks extra point no good'
        expected = {
            'kicker': 'Robbie Gould',
            'status': 'no good'
        }
        match = pbp_parser.parse_extra_point(description)
        assert match and (match.groupdict() == expected)


class TestPunt:
    pass



