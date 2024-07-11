from scraper import Scraper
from columns import ncaa_csv_columns
from ncaa_scraper_helpers import *
from college_url_formats import format_college_for_url
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()


class NCAAStatsScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.data = []
        self.logger.info("Initializing NCAA Statistics Scraper")

    def get_college_stats(self, player, player_id, college, player_url):
        """Function to get all college stats for a certain quarterback"""
        self.logger.info(f"Scraping NCAA statistics for {player}")
        self.data = [player_id, player, college, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Get player statistics
        if player_url is None:
            self.except_missing_data_point()

        else:
            # Load passing df as pandas dataframe
            passing_df = self.send_request(player_url, table_id="passing", use_pandas=True, header=1)
            rushing_df = self.send_request(player_url, table_id="rushing", use_pandas=True, header=1)
            self.scrape_player_stats(passing_df, rushing_df)

        return self.data

    def except_missing_data_point(self):
        """Function to fill in placeholders for missing data"""
        for i in range(4, 22):
            self.data[i] = -1

    def scrape_player_stats(self, passing_df, rushing_df):
        """Function to scrape player stats"""
        player_years = self.scrape_passing_stats(passing_df)
        self.scrape_rushing_stats(rushing_df)
        self.scrape_team_stats(self.data[2], player_years)

    def scrape_passing_stats(self, table):
        """Function to get passing statistics for a quarterback"""

        # Scrape years played
        player_years = []
        for i in list(table["Year"][:-1]):
            year = str(i).replace("*", "")
            player_years.append(int(year))

        # Assign years played and conference
        self.data[4] = len(player_years)   # Years played
        self.data[3] = scrape_conference(table)   # Conference

        # Scrape passing data
        self.data[5] = self.extract_column_value_pandas(table, "G")     # Games played
        self.data[6] = self.extract_column_value_pandas(table, "Cmp")   # Completions
        self.data[7] = self.extract_column_value_pandas(table, "Att")   # Attempts
        self.data[8] = self.extract_column_value_pandas(table, "Yds")   # Passing yards
        self.data[9] = self.extract_column_value_pandas(table, "TD")    # Passing TDs
        self.data[10] = self.extract_column_value_pandas(table, "Int")  # Interceptions
        self.data[11] = self.extract_column_value_pandas(table, "Rate", metric="mean")   # Passer rating

        return player_years

    def scrape_rushing_stats(self, table):
        """Function to get rushing statistics for a quarterback"""

        # Scrape rushing data
        self.data[12] = self.extract_column_value_pandas(table, "Att")  # Rushing Attempts
        self.data[13] = self.extract_column_value_pandas(table, "Yds")  # Rushing Yards
        self.data[14] = self.extract_column_value_pandas(table, "TD")   # Rushing TDs

    def scrape_team_stats(self, college, player_years):
        """Function to get a quarterback's team statistics for a certain season"""

        # Initialize rank
        rank = 999

        # Extract college stats
        for year in player_years:
            # Get yearly statistics
            self.logger.info(f"Scraping team statisitcs for {year} {college}")
            url = f"https://www.sports-reference.com/cfb/schools/{format_college_for_url(college)}/{year}-schedule.html"
            team_df = self.send_request(url, table_id="schedule", use_pandas=True)
            rank_df = self.send_request(url, table_id="polls", use_pandas=True)

            if team_df is not None:

                # Scrape stats
                wins, losses, conference_wins, conference_losses, points_for, points_against = scrape_season(team_df, self.data[3])
                if rank_df is not None:
                    rank = scrape_ranking(rank_df, rank)

                # Initialize object to save data point
                data_point = ['player_id', 'player', 'college', 'conference', 'years', 'games_played', 'completions',
                              'pass_attempts', 'pass_yards', 'pass_tds', 'int', 'pass_rating', 'rush_attempts',
                              'rush_yds', 'rush_tds', wins, losses, rank, conference_wins, conference_losses,
                              points_for, points_against]

                # Update data
                for i in range(15, 22):
                    # Special case for rank
                    if i == 17:
                        self.data[i] = data_point[i]
                    # Sum yearly data
                    else:
                        self.data[i] += data_point[i]

            # Handle missing data
            else:
                self.logger.error(f"Unable to scrape team data for {year} {college}; Url: {url}")
                for i in range(4, 22):
                    self.data[i] = -1

