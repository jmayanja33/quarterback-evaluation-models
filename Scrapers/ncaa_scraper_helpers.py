from independents import independent_schools

def scrape_season(stats, conference):
    """Function to scrape team data for a single season"""
    # Get wins, losses
    wins, losses, conference_wins, conference_losses = scrape_record(stats, conference)

    # Get points for/against
    points_for, points_against = scrape_points(stats)

    return wins, losses, conference_wins, conference_losses, points_for, points_against


def scrape_conference(table, college, year):
    """Function to scrape the conference"""
    if college in independent_schools.keys():
        if year in independent_schools[college]:
            return "Ind"

    try:
        conference = table["Conf"].mode()[0]
        return conference

    except Exception as e:
        return "MISSING"


def scrape_record(table, conference):
    """Function to scrape wins and losses"""

    if len(table.columns) == 15:
        wins_col = "Unnamed: 8"
    else:
        wins_col = "Unnamed: 7"

    # Scrape overall wins/losses
    wins = scrape_game_result(table, wins_col, 'W')
    losses = scrape_game_result(table, wins_col, 'L')

    # Scrape conference record
    if conference == "Ind":
        conference_wins = 0
        conference_losses = 0
    else:
        filtered_table = table[table['Conf'] == conference]
        conference_wins = scrape_game_result(filtered_table, wins_col, 'W')
        conference_losses = scrape_game_result(filtered_table, wins_col, 'L')

    return wins, losses, conference_wins, conference_losses


def scrape_points(table):
    """Function to scrape points for and against"""
    points_for = int(sum(table["Pts"].fillna(0)))
    points_against = int(sum(table["Opp"].fillna(0)))

    return points_for, points_against


def scrape_ranking(stats, rank):
    """Function to scrape a teams highest ranking for a season"""
    try:
        rankings = list(stats.loc[0].dropna())
        new_ranking = int(min(rankings))
        higher_rank = min(rank, new_ranking)

        return higher_rank

    except Exception as e:
        return rank


def scrape_game_result(table, column_name, value):
    """Function to scrape win/loss counts"""
    try:
        return int(table[column_name].value_counts()[value])
    except KeyError:
        return 0
