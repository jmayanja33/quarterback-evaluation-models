import pandas as pd
from Data.colleges import *
from Scrapers.college_url_formats import special_cases

YEAR = 2024


def format_college(college):
    """Function to format a college"""

    if college in special_cases.keys():
        formatted_college = special_cases[college]
        return formatted_college[0].upper() + formatted_college[1:]

    return college


if __name__ == "__main__":
    data = pd.read_csv(f"../Data/FutureData/{YEAR+1}/prospects.csv")
    data["conference"] = [conferences[i] for i in data["conference"]]
    data["college"] = [format_college(colleges[i]) for i in data["college"]]
    data.to_csv(f"../Data/FutureData/{YEAR+1}/cleaned_prospects.csv")
