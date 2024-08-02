from Scrapers.ncaa_stats_scraper import NCAAStatsScraper
from future_players import players
from columns import ncaa_csv_columns
from Helpers.helpers import make_directory
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Upcoming season
YEAR = 2024


if __name__ == "__main__":

    # Initialize objects
    ncaa_scraper = NCAAStatsScraper(current_season=YEAR)
    player_list = sorted(players.keys())
    players_stats = []

    # Iterate through players to make predictions
    for i, player in enumerate(player_list):

        # Extract player data
        player_id = f"2025_{i}"
        url = players[player]["url"]
        college = players[player]["college"]
        height = players[player]["height"]
        weight = players[player]["weight"]

        # Scrape stats
        stats = ncaa_scraper.get_college_stats(player, player_id, college, url)
        stats.append(height)
        stats.append(weight)
        players_stats.append(stats)

    # Make future data directory
    dir_path = f"../Data/FutureData/{YEAR+1}"
    make_directory("../Data", "FutureData")
    make_directory("../Data/FutureData", str(YEAR+1))

    # Save data
    df = pd.DataFrame(players_stats, columns=ncaa_csv_columns)
    df.to_csv(f"{dir_path}/prospects.csv", index=False)
