def scrape_season(stats, conference):
    """Function to scrape team data for a single season"""
    # Get wins, losses
    wins, losses, conference_wins, conference_losses = scrape_record(stats, conference)

    # Get points for/against
    points_for, points_against = scrape_points(stats)

    return wins, losses, conference_wins, conference_losses, points_for, points_against


def scrape_conference(table):
    """Function to scrape the conference"""
    conference_count = int(table['Conf'].value_counts().max())
    # Take most recent conference if the years are split
    if conference_count == 1 and len(set(table['Conf'])) > 1:
        return table['Conf'][-2]
    # Take the conference
    else:
        return table['Conf'].value_counts().idxmax()


def scrape_record(table, conference):
    """Function to scrape wins and losses"""

    # Scrape overall wins/losses
    wins = scrape_game_result(table, 'Unnamed: 7', 'W')
    losses = scrape_game_result(table, 'Unnamed: 7', 'L')

    # Scrape conference record
    if conference == "Ind":
        conference_wins = 0
        conference_losses = 0
    else:
        filtered_table = table[table['Conf'] == conference]
        conference_wins = scrape_game_result(filtered_table, 'Unnamed: 7', 'W')
        conference_losses = scrape_game_result(filtered_table, 'Unnamed: 7', 'L')

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
