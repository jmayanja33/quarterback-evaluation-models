from scraper import Scraper
from columns import ncaa_csv_columns, ncaa_columns_to_index


class NCAAStatsScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.data = [0 for i in range(len(ncaa_csv_columns))]
        self.columns_to_index = ncaa_columns_to_index
        self.logger.info("Initializing NCAA Statistics Scraper")

    def get_college_stats(self, player, player_id, college, player_url):
        """Function to get all college stats for a certain quarterback"""
        self.logger.info(f"Scraping NCAA statistics for {player}")
        self.data = [player_id, player]

        # Get player statistics
        if player_url is None:
            self.data += [-1 for i in range(12)]
        else:
            self.send_request(player_url)

            self.scrape_passing_stats()
            self.scrape_rushing_stats()

        # Get team statistics
        if college is None:
            self.data += [-1 for i in range(9)]
        else:
            self.scrape_team_stats(college)

        return self.data

    def scrape_passing_stats(self):
        """Function to get passing statistics for a quarterback"""
        self.scrape("passing", "passing")

    def scrape_rushing_stats(self):
        """Function to get rushing statistics for a quarterback"""
        self.scrape("rushing", "rushing")

    def scrape_team_stats(self, college):
        """Function to get a quarterback's team statistics for a certain season"""
        for year in self.years:
            url = f"https://www.sports-reference.com/cfb/schools/{college.replace(' ', '-')}/{year}-schedule.html"
            self.send_request(url)

        pass

    def scrape(self, table_id, index):
        """Function to scrape data"""
        table = self.find_table(table_id)

        for row in table.tbody.find_all('tr'):
            # Find table columns
            table_columns = row.find_all('td')

            # Iterate through columns
            for i, col in enumerate(ncaa_csv_columns):
                if col in self.columns_to_index[index].keys():
                    column_val = self.extract_column_value(table_columns, col)

                    # Update data point
                    if type(column_val) == int:
                        # Track years
                        if col == "years":
                            self.years.append(column_val)
                            self.data[i] += 1
                        else:
                            self.data[i] += column_val
                    # Add strings
                    else:
                        self.data[i] = column_val

