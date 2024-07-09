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
    if conference_count < 6:
        return "Ind"
    else:
        return table['Conf'].value_counts().idxmax()


def scrape_record(table, conference):
    """Function to scrape wins and losses"""
    wins = int(table['Unnamed: 7'].value_counts()["W"])
    losses = int(table['Unnamed: 7'].value_counts()["L"])

    # Scrape conference record
    if conference == "Ind":
        conference_wins = 0
        conference_losses = 0
    else:
        filtered_table = table[table['Conf'] == conference]
        conference_wins = int(filtered_table['Unnamed: 7'].value_counts()["W"])
        conference_losses = int(filtered_table['Unnamed: 7'].value_counts()["L"])

    return wins, losses, conference_wins, conference_losses


def scrape_points(table):
    """Function to scrape points for and against"""
    points_for = int(sum(table["Pts"]))
    points_against = int(sum(table["Opp"]))

    return points_for, points_against


def scrape_ranking(stats, rank):
    """Function to scrape a teams highest ranking for a season"""
    try:
        new_ranking = int(stats.loc[0].max())
        higher_rank = max(rank, new_ranking)

        return higher_rank

    except Exception as e:
        return rank