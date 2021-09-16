import pbp_parser 
import play_examples


class TestKickoff:

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


class TestPunt:
    pass


class TestFieldGoal:
    pass


class TestExtraPoint:
    pass