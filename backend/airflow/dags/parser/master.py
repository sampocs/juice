from . import run, pass_, special_teams, defense, misc
import pandas as pd

class PlayTypes:
    RUN = 'RUN'
    PASS = 'PASS'
    KICKOFF = 'KICKOFF'
    PUNT = 'PUNT'
    FIELD_GOAL = 'FIELD_GOAL'
    EXTRA_POINT = 'EXTRA_POINT'
    GAME_MANAGEMENT = 'GAME_MANAGEMENT'
    PENALTY = 'PENALTY'

class KickTypes:
    RETURNED = 'RETURNED'
    OUT_OF_BOUNDS = 'OUT_OF_BOUNDS'
    TOUCHBACK = 'TOUCHBACK'
    ONSIDE = 'ONSIDE'

class PuntTypes:
    RETURNED = 'RETURNED'
    OUT_OF_BOUNDS = 'OUT_OF_BOUNDS'
    TOUCHBACK = 'TOUCHBACK'
    DOWNED = 'DOWNED'
    FAIR_CAUGHT = 'FAIR_CAUGHT'
    BLOCKED = 'BLOCKED'
    RECOVERED = 'RECOVERED'

RUN_KEYS = [
    'running_back',
    'run_direction',
    'run_distance',
    'tackler'
]

PASS_KEYS = [
    'quarterback',
    'pass_complete',
    'pass'
]

FUMBLE_KEYS = [
    'fumbler',
    'fumble_forced_by',
    'fumble_recovered_by',
    'fumble_return_distance',
    'fumble_'
]

def run_direction_mapping(direction: str) -> str:
   return {
        'up the middle': 'MIDDLE',
        'left guard': 'LEFT_GUARD',
        'right guard': 'RIGHT_GUARD',
        'left tackle': 'LEFT_TACKLE',
        'right tackle': 'RIGHT_TACKLE',
        'left end': 'LEFT_END',
        'right end': 'RIGHT_END',
        'scrambles': 'SCRAMBLES',
        'unknown': 'UNKNOWN'
    }[direction]


def pass_direction_mapping(direction: str) -> str:
   return {
        'short left': 'SHORT_LEFT',
        'short middle': 'SHORT_MIDDLE',
        'short right': 'SHORT_RIGHT',
        'deep left': 'DEEP_LEFT',
        'deep middle': 'DEEP_MIDDLE',
        'deep right': 'DEEP_RIGHT',
        'unknown': 'UNKNOWN'
    }[direction]


def distance_mapping(distance: str) -> int:
    if distance == 'no gain':
        return 0
    return int(distance.split()[0])


def parse_pbp(df: pd.DataFrame) -> pd.DataFrame:
    play = df['detail']
    remaining_description = play

    if misc.parse_timeout(play):
        df['play_type'] = PlayTypes.GAME_MANAGEMENT
        df['timeout'] = True
        df['spike'] = False
        df['kneel'] = False
        
    elif misc.parse_spike(play):
        df['play_type'] = PlayTypes.GAME_MANAGEMENT
        df['timeout'] = False
        df['spike'] = True
        df['kneel'] = False

    elif misc.parse_kneel(play):
        df['play_type'] = PlayTypes.GAME_MANAGEMENT
        df['timeout'] = False
        df['spike'] = False
        df['kneel'] = True

    else:
        df['timeout'] = False
        df['spike'] = False
        df['kneel'] = False


    if run.parse_run_play(play):
        match = run.parse_run_play(play).groupdict()
        df['play_type'] = PlayTypes.RUN
        df['running_back'] = match['running_back']
        df['run_direction'] = run_direction_mapping(match['run_direction'])
        df['run_distance'] = distance_mapping(match['run_distance'])
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        remaining_description = play[run.parse_run_play(play).end():]

    elif run.parse_run_no_direction_play(play):
        match = run.parse_run_no_direction_play(play).groupdict()
        df['play_type'] = PlayTypes.RUN
        df['running_back'] = match['running_back']
        df['run_direction'] = run_direction_mapping('unknown')
        df['run_distance'] = distance_mapping(match['run_distance'])
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        remaining_description = play[run.parse_run_no_direction_play(play).end():]

    elif pass_.parse_pass_complete_play(play):
        match = pass_.parse_pass_complete_play(play).groupdict()
        df['play_type'] = PlayTypes.PASS
        df['quarterback'] = match['quarterback']
        df['receiver'] = match['receiver']
        df['pass_complete'] = True
        df['pass_direction'] = pass_direction_mapping(match['pass_direction'] if match['pass_direction'] else 'unknown')
        df['pass_distance'] = distance_mapping(match['pass_distance'])
        df['pass_defended_by'] = None
        df['intercepted'] = False
        df['intercepted_by'] = None
        df['sacked'] = False
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        remaining_description = play[pass_.parse_pass_complete_play(play).end():]

    elif pass_.parse_pass_incomplete_play(play):
        match = pass_.parse_pass_incomplete_play(play).groupdict()
        df['play_type'] = PlayTypes.PASS
        df['quarterback'] = match['quarterback']
        df['receiver'] = match['receiver']
        df['pass_complete'] = False
        df['pass_direction'] = None
        df['pass_distance'] = None
        df['pass_defended_by'] = match['pass_defended_by']
        df['intercepted'] = False
        df['intercepted_by'] = None
        df['sacked'] = False
        df['tackler'] = None
        remaining_description = play[pass_.parse_pass_incomplete_play(play).end():]

    elif defense.parse_interception(play):
        match = defense.parse_interception(play).groupdict()
        df['play_type'] = PlayTypes.PASS
        df['quarterback'] = match['quarterback']
        df['receiver'] = match['receiver']
        df['pass_complete'] = False
        df['pass_direction'] = match['pass_direction']
        df['pass_distance'] = None
        df['pass_defended_by'] = match['pass_defended_by']
        df['intercepted'] = True
        df['intercepted_by'] = match['intercepted_by']
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        df['sacked'] = False
        remaining_description = play[defense.parse_interception(play).end():]

    elif defense.parse_sack_full(play):
        match = defense.parse_sack_full(play).groupdict()
        df['play_type'] = PlayTypes.PASS
        df['quarterback'] = match['quarterback']
        df['receiver'] = None
        df['pass_complete'] = None
        df['pass_direction'] = None
        df['pass_distance'] = None
        df['pass_defended_by'] = None
        df['intercepted'] = False
        df['intercepted_by'] = None
        df['tackler'] = [match['sacker']]
        df['sacked'] = True
        remaining_description = play[defense.parse_sack_full(play).end():]


    elif defense.parse_sack_half(play):
        match = defense.parse_sack_half(play).groupdict()
        df['play_type'] = PlayTypes.PASS
        df['quarterback'] = match['quarterback']
        df['receiver'] = None
        df['pass_complete'] = None
        df['pass_direction'] = None
        df['pass_distance'] = None
        df['pass_defended_by'] = None
        df['intercepted'] = False
        df['intercepted_by'] = None
        df['tackler'] = [match['sacker1'], match['sacker2']]
        df['sacked'] = True
        remaining_description = play[defense.parse_sack_half(play).end():]


    elif special_teams.parse_kickoff_returned(play):
        match = special_teams.parse_kickoff_returned(play)
        df['play_type'] = PlayTypes.KICKOFF
        df['kicker'] = match['kicker']
        df['kick_type'] = KickTypes.RETURNED
        df['kick_distance'] = match['kick_distance']
        df['kick_returner'] = match['kick_returner']
        df['kick_return_distance'] = match['kick_return_distance']
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        remaining_description = play[special_teams.parse_kickoff_returned(play).end():]  

    elif special_teams.parse_kickoff_out_of_bounds(play):
        match = special_teams.parse_kickoff_out_of_bounds(play)
        df['play_type'] = PlayTypes.KICKOFF
        df['kicker'] = match['kicker']
        df['kick_type'] = KickTypes.OUT_OF_BOUNDS
        df['kick_distance'] = match['kick_distance']
        df['kick_returner'] = None
        df['kick_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_kickoff_out_of_bounds(play).end():]  

    elif special_teams.parse_kickoff_touchback(play):
        match = special_teams.parse_kickoff_touchback(play)
        df['play_type'] = PlayTypes.KICKOFF
        df['kicker'] = match['kicker']
        df['kick_type'] = KickTypes.TOUCHBACK
        df['kick_distance'] = match['kick_distance']
        df['kick_returner'] = None
        df['kick_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_kickoff_touchback(play).end():]  

    elif special_teams.parse_onside_kick(play):
        match = special_teams.parse_onside_kick(play)
        df['play_type'] = PlayTypes.KICKOFF
        df['kicker'] = match['kicker']
        df['kick_type'] = KickTypes.ONSIDE
        df['kick_distance'] = match['kick_distance']
        df['kick_returner'] = None
        df['kick_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_onside_kick(play).end():]  

    elif special_teams.parse_field_goal(play):
        match = special_teams.parse_field_goal(play)
        df['play_type'] = PlayTypes.FIELD_GOAL
        df['kicker'] = match['kicker']
        df['field_goal_made'] = (match['status'] == 'good')
        df['field_goal_distance'] = match['field_goal_distance']
        df['field_goal_blocked'] = 'blocked' in play
        remaining_description = play[special_teams.parse_field_goal(play).end():]  

    elif special_teams.parse_extra_point(play):
        match = special_teams.parse_extra_point(play)
        df['play_type'] = PlayTypes.EXTRA_POINT
        df['kicker'] = match['kicker']
        df['extra_point_made'] = (match['status'] == 'good')
        df['extra_point_blocked'] = 'blocked' in play
        remaining_description = play[special_teams.parse_extra_point(play).end():]  

    elif special_teams.parse_punt_returned(play):
        match = special_teams.parse_punt_returned(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.RETURNED
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = match['punt_returner']
        df['punt_return_distance'] = match['punt_return_distance']
        df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []
        remaining_description = play[special_teams.parse_punt_returned(play).end():] 
    
    elif special_teams.parse_punt_downed(play):
        match = special_teams.parse_punt_downed(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.DOWNED
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = None
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_downed(play).end():] 

    elif special_teams.parse_punt_fair_catch(play):
        match = special_teams.parse_punt_fair_catch(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.FAIR_CAUGHT
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = match['punt_returner']
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_fair_catch(play).end():] 

    elif special_teams.parse_punt_touchback(play):
        match = special_teams.parse_punt_touchback(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.TOUCHBACK
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = None
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_touchback(play).end():] 
    
    elif special_teams.parse_punt_out_of_bounds(play):
        match = special_teams.parse_punt_out_of_bounds(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.OUT_OF_BOUNDS
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = None
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_out_of_bounds(play).end():] 

    elif special_teams.parse_punt_blocked(play):
        match = special_teams.parse_punt_blocked(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.BLOCKED
        df['punt_distance'] = None
        df['punt_returner'] = None
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_blocked(play).end():] 

    elif special_teams.parse_punt_recovered(play):
        match = special_teams.parse_punt_recovered(play)
        df['play_type'] = PlayTypes.PUNT
        df['punter'] = match['punter']
        df['punt_type'] = PuntTypes.RECOVERED
        df['punt_distance'] = match['punt_distance']
        df['punt_returner'] = match['recoverer']
        df['punt_return_distance'] = None
        df['tackler'] = None
        remaining_description = play[special_teams.parse_punt_recovered(play).end():] 

    if 'play_type' in df and df['play_type'] != PlayTypes.GAME_MANAGEMENT:
        if defense.parse_fumble(remaining_description):
            match = defense.parse_fumble(remaining_description).groupdict()
            df['fumble'] = True
            df['fumbler'] = match['fumbler']
            df['fumble_forced_by'] = match['fumble_forced_by']
            df['fumble_recovered_by'] = match['fumble_recovered_by']
            df['tackler'] = match['tackler'].split(' and ') if match['tackler'] else []

        else:
            df['fumble'] = False
            df['fumbler'] = None
            df['fumble_forced_by'] = None
            df['fumble_recovered_by'] = None


    df['penalty'] = False
    df['penalty_type'] = []
    df['penalty_on'] = []
    df['penalty_distance'] = None
    df['penalty_response'] = None
    df['no_play'] = False

    for penalty in misc.parse_penalty(remaining_description):
        df['penalty'] = True
        df['penalty_type'].append(penalty['penalty_type'])
        df['penalty_on'].append(penalty['penalty_on'])
        df['penalty_response'] = penalty['penalty_response'].upper()
        df['penalty_distance'] = 0 if df['penalty_response'] == 'OFFSET' else distance_mapping(penalty['penalty_distance'])
        df['no_play'] = (penalty['no_play'] == 'no play')
        if 'play_type' not in df:
            df['play_type'] = PlayTypes.PENALTY

    return df
