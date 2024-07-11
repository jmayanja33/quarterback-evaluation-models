import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from Logs.logger import Logger
import pandas as pd
import requests
import collections
import time
import os
import io
collections.Callable = collections.abc.Callable

load_dotenv()


# def initialize_driver():
#     """Function to initialize a selenium web driver service"""
#
#     # Initialize service
#     service = Service(os.getenv('CHROME_DRIVER_PATH'))
#
#     # Set service options
#     options = webdriver.ChromeOptions()
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--incognito')
#     options.add_argument('--headless')
#
#     prefs = {"profile.managed_default_content_settings.images": 2,
#              "profile.managed_default_content_settings.stylesheets": 2}
#     options.add_experimental_option("prefs", prefs)
#
#     # Initialize driver
#     driver = webdriver.Chrome(options=options, service=service)
#     driver.set_page_load_timeout(60)
#     driver.set_script_timeout(60)
#
#     # Return webdriver service
#     return webdriver.Chrome(options=options, service=service)


class Scraper:
    """Base class for a web scraper object"""

    def __init__(self, start_year=2001, end_year=2022):
        self.logger = Logger()
        # self.driver = initialize_driver()
        # self.session = requests.session()
        self.soup = None
        self.years = [i for i in range(start_year, end_year)]
        self.columns_to_index = dict()
        self.driver_queries = 0

    def send_request(self, url, use_pandas=False, header=None, table_id=None):
        """Function to send request for data to be scraped"""
        # response = self.session.get(url).text
        # if selenium_needed:
        #     if self.driver_queries == 5:
        #         self.driver.refresh()
        #
        #     num_retries = 10
        #     num_attempts = 0
        #
        #     while num_attempts < num_retries:
        #         num_attempts += 1
        #
        #         try:
        #             self.driver.get(url)
        #             self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        #             self.driver_queries += 1
        #             return
        #         except TimeoutException as e:
        #             self.logger.error(f"Timeout error attempting to reach: {url}")
        #             self.logger.info(f"Refreshing driver (refresh {num_attempts}/10)")
        #             self.driver.refresh()
        #
        #     self.logger.error(f"Exiting; Unable to reach: {url}")
        #     sys.exit()

        # Get html response
        response = requests.get(url).text

        # Pause for 5 seconds to avoid exceeding rate limit
        time.sleep(5)

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

        # else:
        #     dfs = pd.read_html(url, encoding="utf-8", header=header)
        #
        #     # Pause for 5 seconds to avoid exceeding rate limit
        #     time.sleep(5)
        #
        #     # Look for 2 tables, return 1 if the second is not found
        #     if len(dfs) == 0:
        #         return dfs[0], None
        #     else:
        #         return dfs[1], dfs[0]

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

    def extract_column_value_pandas(self, table, column, metric="sum"):
        """Function to extract data from an html table rendered by pandas"""
        try:
            if metric == "sum":
                return sum(table[column].fillna(0)[:-1])
            elif metric == "mean":
                return table[column].fillna(0)[:-1].mean()

        except Exception as e:
            return 0

    def save_data(self, filename, data, columns):
        """Function to save table to a csv file"""
        self.logger.info(f"Saving data to file: {filename}.csv")
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(f"../Data/{filename}.csv", index=False)
