from scraper import Scraper
from ncaa_stats_scraper import NCAAStatsScraper
from columns import *


class NFLDraftScraper(Scraper):

    def __init__(self, start_year=2001, end_year=2022):
        super().__init__(start_year, end_year)
        self.logger.info("Initializing NFL Draft Scraper")
        self.columns_to_index = nfl_columns_to_index
        self.ncaa_scraper = NCAAStatsScraper()
        self.nfl_data = []
        self.college_data = []

    def scrape_all_years(self):
        """Function to scrape draft data for all years specified"""
        for year in self.years:
            self.logger.info(f"Scraping NFL draft data for quarterbacks for year: {year}")
            # Get HTML data from Sports Reference
            url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
            self.send_request(url)
            # Scrape `drafts` table from HTML
            table = self.find_table("drafts")
            self.scrape(table, year)

        # Save data to csv
        self.save_data("nfl_draft_qbs", self.nfl_data, nfl_csv_columns)
        self.save_data("ncaa_drafted_qbs", self.college_data, ncaa_csv_columns)

    def scrape(self, table, year):
        """Function to scrape NFL statistics for drafted prospects"""
        for row in table.tbody.find_all('tr'):

            # Find table columns.py
            table_columns = row.find_all('td')

            # Iterate through the columns.py
            if table_columns:

                # Find player ID, position, draft_round
                player = table_columns[2].text.strip()
                position = table_columns[3].text.strip()
                draft_round = int(row.find('th').text.strip())
                pick_number = int(table_columns[0].text.strip())
                player_id = f"{year}-{pick_number}"
                nfl_data_point = [year, position, player_id, draft_round]

                # If the player is a quarterback, scrape the data
                if position == "QB":
                    self.logger.info(f"Scraping NFL statistics for {player}")

                    # Extract data from each of the specified columns.py in self.`columns_to_index`
                    for col in nfl_csv_columns:
                        if col in self.columns_to_index.keys():
                            column_val = self.extract_column_value(table_columns, col)
                            nfl_data_point.append(column_val)

                    # Get college data
                    college = table_columns[26].text.strip()

                    # Exception if college stats are not present
                    try:
                        college_stats_url = table_columns[27].next_element.attrs["href"]
                    except AttributeError:
                        college_stats_url = None

                    college_data_point = self.ncaa_scraper.get_college_stats(player, player_id, college, college_stats_url)

                    # Track data
                    self.nfl_data.append(nfl_data_point)
                    self.college_data.append(college_data_point)

