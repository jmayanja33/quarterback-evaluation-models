ncaa_csv_columns = [
    "player_id", "player", "college", "conference", "years", "games_played", "completions", "passes_attempted",
    "passing_yards", "passing_touchdowns", "interceptions", "passer_rating", "rushing_attempts", "rushing_yards",
    "rushing_touchdowns", "wins", "losses", "highest_rank", "conference_wins", "conference_losses", "points_for",
    "points_against", "years_missing"
]

nfl_csv_columns = [
    "year", "position", "player_id", "player", "round", "pick", "team", "age", "final_year",
    "first_team_all_pro_selections", "pro_bowl_selections", "number_of_years_as_a_starter",
    "weighted_career_approximate_value", "games_played", "completions", "passes_attempted", "passing_yards",
    "passing_touchdowns", "interceptions", "rushing_attempts", "rushing_yards", "rushing_touchdowns", "college"
]

nfl_columns_to_index = {
    "player": {'type': 'str', 'index': 2},
    "pick": {'type': 'int', 'index': 0},
    "team": {'type': 'str', 'index': 1},
    "age": {'type': 'int', 'index': 4},
    "final_year": {'type': 'int', 'index': 5},
    "first_team_all_pro_selections": {'type': 'int', 'index': 6},
    "pro_bowl_selections": {'type': 'int', 'index': 7},
    "number_of_years_as_a_starter": {'type': 'int', 'index': 8},
    "weighted_career_approximate_value": {'type': 'int', 'index': 9},
    "games_played": {'type': 'int', 'index': 11},
    "completions": {'type': 'int', 'index': 12},
    "passes_attempted": {'type': 'int', 'index': 13},
    "passing_yards": {'type': 'int', 'index': 14},
    "passing_touchdowns": {'type': 'int', 'index': 15},
    "interceptions": {'type': 'int', 'index': 16},
    "rushing_attempts": {'type': 'int', 'index': 17},
    "rushing_yards": {'type': 'int', 'index': 18},
    "rushing_touchdowns": {'type': 'int', 'index': 19},
    "college": {'type': 'str', 'index': 26}
}
