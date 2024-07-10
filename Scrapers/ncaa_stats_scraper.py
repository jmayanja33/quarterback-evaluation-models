from scraper import Scraper
from columns import ncaa_csv_columns
from ncaa_scraper_helpers import *
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()


class NCAAStatsScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.data = [0 for i in range(len(ncaa_csv_columns))]
        self.logger.info("Initializing NCAA Statistics Scraper")

    def get_college_stats(self, player, player_id, college, player_url):
        """Function to get all college stats for a certain quarterback"""
        self.logger.info(f"Scraping NCAA statistics for {player}")
        self.data = [player_id, player, college, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Get player statistics
        if player_url is None:
            for i in range(4, 20):
                self.data[i] = -1
            self.data[20] = -1

        else:
            self.send_request(player_url, selenium_needed=True)

            # Load passing df as pandas dataframe
            passing_html = str(self.find_table("passing"))
            passing_df = pd.read_html(io.StringIO(passing_html), encoding="utf-8", header=1)[0]

            rushing_html = str(self.find_table("rushing"))
            rushing_df = pd.read_html(io.StringIO(rushing_html), encoding="utf-8", header=1)[0]
            self.scrape_player_stats(passing_df, rushing_df)

        return self.data

    def scrape_player_stats(self, passing_df, rushing_df):
        """Function to scrape player stats"""
        player_years = self.scrape_passing_stats(passing_df)
        self.scrape_rushing_stats(rushing_df)
        self.scrape_team_stats(self.data[2], player_years)

    def scrape_passing_stats(self, table):
        """Function to get passing statistics for a quarterback"""

        # Scrape years played and conference
        player_years = list(table["Year"][:-1])
        self.data[4] = len(player_years)   # Years played
        self.data[3] = scrape_conference(table)   # Conference

        # Scrape passing data
        self.data[5] = self.extract_column_value_pandas(table, "Cmp")    # Completions
        self.data[6] = self.extract_column_value_pandas(table, "Att")   # Attempts
        self.data[7] = self.extract_column_value_pandas(table, "Yds")  # Passing yards
        self.data[8] = self.extract_column_value_pandas(table, "TD")  # Passing TDs
        self.data[9] = self.extract_column_value_pandas(table, "Int")  # Interceptions
        self.data[10] = self.extract_column_value_pandas(table, "Rate", metric="mean")   # Passer rating

        return player_years

    def scrape_rushing_stats(self, table):
        """Function to get rushing statistics for a quarterback"""

        # Scrape rushing data
        self.data[11] = self.extract_column_value_pandas(table, "Att")  # Rushing Attempts
        self.data[12] = self.extract_column_value_pandas(table, "yds")  # Rushing Yards
        self.data[13] = self.extract_column_value_pandas(table, "TD")  # Rushing TDs

    def scrape_team_stats(self, college, player_years):
        """Function to get a quarterback's team statistics for a certain season"""

        # Initialize rank
        rank = -1

        # Extract college stats
        for year in player_years:
            # Get yearly statistics
            self.logger.info(f"Scraping team statisitcs for {year} {college}")
            url = f"https://www.sports-reference.com/cfb/schools/{college.lower().replace(' ', '-')}/{year}-schedule.html"
            team_df, rank_df = self.send_request(url)

            # Scrape stats
            wins, losses, conference_wins, conference_losses, points_for, points_against = scrape_season(team_df, self.data[3])
            if rank_df is not None:
                rank = scrape_ranking(rank_df, rank)

            # Initialize object to save data point
            data_point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          wins, losses, rank, conference_wins, conference_losses, points_for, points_against, 0]

            # Update data
            for i in range(14, 21):
                self.data[i] += data_point[i]



