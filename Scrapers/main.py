from nfl_draft_scraper import NFLDraftScraper
import warnings

warnings.filterwarnings("ignore")


if __name__ == "__main__":
    nfl_scraper = NFLDraftScraper(end_year=2002)
    nfl_scraper.scrape_all_years()

