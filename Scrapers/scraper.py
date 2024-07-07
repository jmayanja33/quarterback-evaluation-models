from bs4 import BeautifulSoup
from Logs.logger import Logger
import pandas as pd
import requests
import collections
import time
collections.Callable = collections.abc.Callable


class Scraper:
    """Base class for a web scraper object"""

    def __init__(self, start_year=2001, end_year=2022):
        self.logger = Logger()
        self.session = requests.Session()
        self.soup = None
        self.years = [i for i in range(start_year, end_year)]
        self.columns_to_index = dict()

    def send_request(self, url):
        """Function to send request for data to be scraped"""
        response = self.session.get(url).text
        self.soup = BeautifulSoup(response, 'html.parser')

        # Pause for 5 seconds to avoid exceeding rate limit
        time.sleep(5)

    def find_table(self, table_id):
        """Function to find a table by its id in the soup result"""
        return self.soup.find('table', id=table_id)

    def extract_column_value(self, columns, column):
        """Function to extract row value from table in the soup results"""
        value_type = self.columns_to_index[column]['type']
        value_index = self.columns_to_index[column]['index']

        # Extract the value if it is present
        try:
            if value_type == 'int':
                return int(columns[value_index].text.strip())

            elif value_type == 'float':
                return float(columns[value_index].text.strip())

            else:
                return columns[value_index].text.strip()

        # Return a filler value if not
        except ValueError:
            if value_type == 'int':
                return 0
            else:
                return "MISSING"

    def save_data(self, filename, data, columns):
        """Function to save table to a csv file"""
        self.logger.info(f"Saving data to file: {filename}.csv")
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(f"../Data/{filename}.csv", index=False)
