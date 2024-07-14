import pandas as pd
import io
from scraper import Scraper


class CombineScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.data = None
        self.logger.info("Initializing NCAA Statistics Scraper")

    def scrape(self, player):
        """Function to scrape statistics from combine"""
        self.logger.info(f"Scraping combine data for {player}")

        # If table isn't found, return 0 for height and weight
        if self.data is None:
            return 0, 0

        # Filter data
        filtered_data = self.data[self.data["Name"] == player]
        if len(filtered_data) == 0:
            self.logger.error(f"No combine data found for {player}")
            return 0, 0

        # Scrape height and weight
        height = float(filtered_data["Height (in)"])
        weight = float(filtered_data["Weight (lbs)"])

        return height, weight

    def find_table(self, year):
        """Function to find the combine table"""
        self.logger.info(f"Retrieving combine data for year: {year}")

        url = f"https://nflcombineresults.com/nflcombinedata.php?year={year}&pos=QB&college="
        formatted_html = self.format_html(url)

        # Exit if the table is not found
        if formatted_html is None:
            self.logger.error(f"Unable to scrape combine statistics for: {year}; URL: {url}")
            self.data = None

        # Find table
        try:
            table = pd.read_html(formatted_html)[0]
            self.data = table

        # Table can't be found
        except Exception as e:
            self.logger.error(f"Unable to find combine table for year: {year} with cleaned html")
            return None

    def format_html(self, url):
        """Function to format the html returned to find the combine table"""

        # Get html
        html = self.send_request(url)

        # Exit if data is not found
        if html is None:
            return None

        # Format html to find table
        split_html = html.split("<!DOCTYPE html>")
        formatted_html = "<!DOCTYPE html>" + split_html[1]

        return io.StringIO(formatted_html)



