import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from Logs.logger import Logger
import pandas as pd
import requests
import collections
import time
import io
from requests.exceptions import ConnectionError
collections.Callable = collections.abc.Callable

load_dotenv()


class Scraper:
    """Base class for a web scraper object"""

    def __init__(self, start_year=2000, end_year=2025):
        self.logger = Logger()
        self.soup = None
        self.years = [i for i in range(start_year, end_year)]
        self.columns_to_index = dict()
        self.driver_queries = 0

    def send_request(self, url, use_pandas=False, header=None, table_id=None):
        """Function to send request for data to be scraped"""
        counter = 0

        # Get html response
        while counter < 5:
            try:
                response = requests.get(url).text

                # Pause for 5 seconds to avoid exceeding rate limit
                time.sleep(5)
                break
            # Handle connection error
            except ConnectionError as e:
                self.logger.error(f"Unable to get response from {url} on attempt {counter+1}/5; Details: {e}")

                # Exit if unsuccessful after 5 tries
                if counter == 4:
                    self.logger.critical(f"Exiting. Unable to connect to: {url} ")
                    sys.exit(1)

                # Update counter
                counter += 1

        # Return pandas dataframes
        if use_pandas:
            # Format html to render javascript
            cleaned_response = response.replace("<!--", "").replace("-->", "")
            self.soup = BeautifulSoup(cleaned_response, 'html.parser')

            # Find table
            table_html = str(self.find_table(table_id))
            try:
                return pd.read_html(io.StringIO(table_html), encoding="utf-8", header=header)[0]
            # Handle no table found
            except ValueError:
                self.logger.error(f"Error; unable to find {table_id} table with pandas at: {url}")
                return

        # Return regular text to beautiful soup object
        self.soup = BeautifulSoup(response, 'html.parser')
        return

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

    def extract_column_value_pandas(self, table, column, indexes, metric="sum"):
        """Function to extract data from an HTML table rendered by pandas"""
        try:
            if metric == "sum":
                return sum(table[column][indexes].fillna(0))
            elif metric == "mean":
                return table[column][indexes].fillna(0).mean()

        except Exception as e:
            return 0

    def save_data(self, filename, data, columns):
        """Function to save table to a csv file"""
        self.logger.info(f"Saving data to file: {filename}.csv")
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(f"../Data/{filename}.csv", index=False)
