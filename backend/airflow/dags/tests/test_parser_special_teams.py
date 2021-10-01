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

    def test_punt_out_of_bounds_all_examples(self):
        """
        Test that the PUNT_OUT_OF_BOUNDS play parser matches out of bounds punts
        """
        play_examples.check_across_all_examples('PUNT_OUT_OF_BOUNDS', pbp_parser.parse_punt_out)


    def test_punt_downed_all_examples(self):
        """
        Test that the PUNT_DOWNED play parser matches downed punts
        """
        play_examples.check_across_all_examples('PUNT_DOWNED', pbp_parser.parse_punt_downed)


    def test_punt_fair_catch_all_examples(self):
        """
        Test that the PUNT_FAIR_CATCH play parser matches fair catches
        """
        play_examples.check_across_all_examples('PUNT_FAIR_CATCH', pbp_parser.parse_punt_fair_catch)


    def test_punt_returned_all_examples(self):
        """
        Test that the PUNT_RETURNED play parser matches returned punts
        """
        play_examples.check_across_all_examples('PUNT_RETURNED', pbp_parser.parse_punt_returned)


    def test_punt_recovered_all_examples(self):
        """
        Test that the PUNT_RECOVERED play parser matches recovered punts
        """
        play_examples.check_across_all_examples('PUNT_RECOVERED', pbp_parser.parse_punt_recovered)

    
    def test_punt_touchback_all_examples(self):
        """
        Test that the PUNT_TOUCHBACK play parser matches touchback punts
        """
        play_examples.check_across_all_examples('PUNT_TOUCHBACK', pbp_parser.parse_punt_touchback)

    
    def test_punt_blocked_all_examples(self):
        """
        Test that the PUNT_BLOCKED play parser matches blocked punts
        """
        play_examples.check_across_all_examples('PUNT_BLOCKED', pbp_parser.parse_punt_blocked)


    def test_punt_out_of_bounds(self):
        """
        Test match dict from punt out of bounds
        """
        description = "Pat O'Donnell punts 45 yards out of bounds"
        expected = {
            'punter': "Pat O'Donnell",
            'distance': '45 yards'
        }
        match = pbp_parser.parse_punt_out(description)
        assert match and (match.groupdict() == expected)


    def test_punt_downed(self):
        """
        Test match dict from punt downed
        """
        description = "Pat O'Donnell punts 45 yards downed by Cordarrelle Patterson"
        expected = {
            'punter': "Pat O'Donnell",
            'distance': '45 yards',
            'downer': 'Cordarrelle Patterson'
        }
        match = pbp_parser.parse_punt_downed(description)
        assert match and (match.groupdict() == expected)

    
    def test_punt_fair_catch(self):
        """
        Test match dict from punt fair caught
        """
        description = "Pat O'Donnell punts 45 yards, fair catch by Cordarrelle Patterson at DET-10"
        expected = {
            'punter': "Pat O'Donnell",
            'punt_distance': '45 yards',
            'returner': 'Cordarrelle Patterson',
            'yardage': 'DET-10'
        }
        match = pbp_parser.parse_punt_fair_catch(description)
        assert match and (match.groupdict() == expected)

    
    def test_punt_returned(self):
        """
        Test match dict from punt returned
        """
        description = "Pat O'Donnell punts 45 yards, returned by Cordarrelle Patterson for 27 yards"
        expected = {
            'punter': "Pat O'Donnell", 
            'punt_distance': '45 yards',
            'returner': 'Cordarrelle Patterson',
            'return_distance': '27 yards',
            'tackler': None
        }
        match = pbp_parser.parse_punt_returned(description)
        assert match and (match.groupdict() == expected)


    def test_punt_returned_with_tackle(self):
        """
        Test match dict from punt returned with tackle
        """
        description = "Pat O'Donnell punts 45 yards, returned by Cordarrelle Patterson for 27 yards (tackle by Pat O'Donnell)"
        expected = {
            'punter': "Pat O'Donnell", 
            'punt_distance': '45 yards',
            'returner': 'Cordarrelle Patterson',
            'return_distance': '27 yards',
            'tackler': "Pat O'Donnell"
        }
        match = pbp_parser.parse_punt_returned(description)
        assert match and (match.groupdict() == expected)


    def test_punt_recovered(self):
        """
        Test match dict from punt recovered 
        """
        description = "Pat O'Donnell punts 45 yards, recovered by Cordarrelle Patterson at CHI-10"
        expected = {
            'punter': "Pat O'Donnell", 
            'punt_distance': '45 yards',
            'recoverer': 'Cordarrelle Patterson',
            'yardage': 'CHI-10',
        }
        match = pbp_parser.parse_punt_recovered(description)
        assert match and (match.groupdict() == expected)


    def test_punt_touchback(self):
        """
        Test match dict from punt touchback 
        """
        description = "Pat O'Donnell punts 45 yards, touchback"
        expected = {
            'punter': "Pat O'Donnell", 
            'punt_distance': '45 yards'
        }
        match = pbp_parser.parse_punt_touchback(description)
        assert match and (match.groupdict() == expected)


    def test_punt_blocked(self):
        """
        Test match dict from punt blocked 
        """
        description = "Pat O'Donnell punts blocked by Miles Killebrew"
        expected = {
            'punter': "Pat O'Donnell", 
            'blocker': 'Miles Killebrew'
        }
        match = pbp_parser.parse_punt_blocked(description)
        assert match and (match.groupdict() == expected)