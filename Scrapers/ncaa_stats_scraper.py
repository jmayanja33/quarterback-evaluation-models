from scraper import Scraper
from columns import ncaa_csv_columns, ncaa_columns_to_index
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()


class NCAAStatsScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.data = [0 for i in range(len(ncaa_csv_columns))]
        self.columns_to_index = ncaa_columns_to_index
        self.logger.info("Initializing NCAA Statistics Scraper")

    def get_college_stats(self, player, player_id, college, player_url):
        """Function to get all college stats for a certain quarterback"""
        self.logger.info(f"Scraping NCAA statistics for {player}")
        self.data = [player_id, player, college, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Get player statistics
        if player_url is None:
            for i in range(4, 13):
                self.data[i] = -1
            self.data[20] = -1

            player_years = None
        else:
            self.send_request(player_url)
            player_years = self.scrape_passing_stats()
            self.scrape_rushing_stats()

        # Get team statistics
        if college is None or player_years is None:
            for i in range(14, 20):
                self.data[i] = -1
        else:
            self.scrape_team_stats(college, player_years)

        return self.data

    def scrape_passing_stats(self):
        """Function to get passing statistics for a quarterback"""
        return self.scrape("passing", "passing")

    def scrape_rushing_stats(self):
        """Function to get rushing statistics for a quarterback"""
        self.scrape("rushing", "rushing")

    def scrape(self, table_id, index):
        """Function to scrape data"""
        table = self.find_table(table_id)
        player_years = []

        for row in table.tbody.find_all('tr'):
            # Find table columns
            table_columns = row.find_all('td')

            # Iterate through columns
            for i, col in enumerate(ncaa_csv_columns):
                if col in self.columns_to_index[index].keys():
                    column_val = self.extract_column_value(table_columns, col, index)

                    # Update data point
                    if type(column_val) == int:
                        # Track years
                        if col == "years":
                            player_years.append(column_val)
                            self.data[i] += 1
                        else:
                            self.data[i] += column_val
                    # Add strings
                    else:
                        self.data[i] = column_val

        return player_years

    def scrape_team_stats(self, college, player_years):
        """Function to get a quarterback's team statistics for a certain season"""

        # Initialize rank
        rank = -1

        # Extract college stats
        for year in player_years:
            # Get yearly statistics
            self.logger.info(f"Scrpaing team statisitcs for {year} {college}")
            url = f"https://www.sports-reference.com/cfb/schools/{college.lower().replace(' ', '-')}/{year}-schedule.html"
            dfs = pd.read_html(url, encoding="utf-8")
            # self.send_request(url)

            # Scrape stats
            if len(dfs) == 1:
                conference, wins, losses, conference_wins, conference_losses, points_for, points_against = self.scrape_season(dfs[0])
            else:
                conference, wins, losses, conference_wins, conference_losses, points_for, points_against = self.scrape_season(dfs[1])
                rank = self.scrape_ranking(dfs[0], rank)

            data_point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          wins, losses, rank, conference_wins, conference_losses, points_for, points_against, 0]

            # Set conference (most recent conference will be used)
            self.data[3] = conference

            # Update data
            for i in range(14, 21):
                self.data[i] += data_point[i]

    def scrape_season(self, stats):
        """Function to scrape team data for a single season"""
        # stats = self.find_table('schedule')
        # html_table = io.StringIO(str(self.find_table('schedule')))
        # stats = pd.read_html(html_table, encoding="utf-8")[0]

        # Get conference
        conference = self.scrape_conference(stats)

        # Get wins, losses
        wins, losses, conference_wins, conference_losses = self.scrape_record(stats, conference)

        # Get points for/against
        points_for, points_against = self.scrape_points(stats)

        return conference, wins, losses, conference_wins, conference_losses, points_for, points_against

    def scrape_conference(self, table):
        """Function to scrape the conference"""
        conference_count = int(table['Conf'].value_counts().max())
        if conference_count < 6:
            return "Ind"
        else:
            return table['Conf'].value_counts().idxmax()

    def scrape_record(self, table, conference):
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

    def scrape_points(self, table):
        """Function to scrape points for and against"""
        points_for = int(sum(table["Pts"]))
        points_against = int(sum(table["Opp"]))

        return points_for, points_against

    def scrape_ranking(self, stats, rank):
        """Function to scrape a teams highest ranking for a season"""
        try:
            # html_table = io.StringIO(str(self.find_table('polls')))
            # stats = pd.read_html(html_table)[0]
            new_ranking = int(stats.loc[0].max())
            higher_rank = max(rank, new_ranking)

            return higher_rank

        except Exception as e:
            return rank


