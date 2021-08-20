# Juice
NFL Dashboard <br>
**MVP in progress**

## Pages (Tables)
### Season
* All teams
* Wins/Losses
* PF/PA
* Rank
* Average Statistics 

### Upcoming Games
* Teams
* Opponent or bye
* Home/Away
* Spread
* Team Metrics
* Diffs

### Past Games
* Team
* Opponent
* Games Statistics

### Team
* Aggregate statistics
* Games by week (v1)
* Visualizations (v1)
* Roster (v1)
* Compare to other teams (v1)

## Navigation and DB Calls
![Navigation](/images/navigation.png)

## Backend
### Teams (fact) (static - manual upload)
| Field       | Type |
|-------------|------|
| **team_id** | text |
| org_id      | text |
| city        | text |
| mascot      | text |
| start_year  | int  |
| active      | bool |
| pfr_name    | text |

### Games (fact) 
| Field        | Type     |
|--------------|----------|
| **game_id**  | text     |
| season       | int      |
| week         | int      |
| datetime     | datetime |
| home_team_id | text     |
| away_team_id | text     |
| has_pbp      | bool     |

### PBP (fact)
| Field        | Type |
|--------------|------|
| **game_id**  | text |
| play_number  | int  |
| time         | text |
| down         | int  |
| yards_to_go  | int  |
| pass         | bool |
| run          | bool |
| kickoff      | bool |
| punt         | bool |
| field_goal   | bool |
| yards_gained | int  |
| penalty      | bool |

### Roster (fact) (v1)
| Field         | Type |
|---------------|------|
| **player_id** | text |
| name          | text |
| team_id       | text |
| number        | int  |
| position      | text |

### Lines (fact)
| Field       | Type     |
|-------------|----------|
| **game_id** | text     |
| time        | datetime |
| spread      | int      |

### Players (dim) (v1)
| Field         | Type |
|---------------|------|
| **player_id** | text |
| **team_id**   | text |
| first_name    | text |
| last_name     | text |
| number        | int  |
| position      | text |
| attempts      | int  |
| completions   | int  |
| yards         | int  |

### GameStatistics (dim) 
| Field                              | Type  |
|------------------------------------|-------|
| **game_id**                        | text  |
| status                             | enum  |
| home_team_yards                    | int   |
| away_team_yards                    | int   |
| home_team_rush_yards               | int   |
| home_team_pass_yards               | int   |
| home_team_offensive_plays          | int   |
| home_team_defensive_plays          | int   |
| away_team_rush_yards               | int   |
| away_team_pass_yards               | int   |
| away_team_offensive_plays          | int   |
| away_team_defensive_plays          | int   |
| home_team_offensive_yards_per_play | float |
| home_team_defensive_yards_per_play | float |
| away_team_offensive_yards_per_play | float |
| away_team_defensive_yards_per_play | float |
| home_team_penalties                | int   |
| away_team_penalties                | int   |
