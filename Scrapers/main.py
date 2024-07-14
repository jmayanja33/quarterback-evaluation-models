from nfl_draft_scraper import NFLDraftScraper
import warnings
import time

warnings.filterwarnings("ignore")


if __name__ == "__main__":
    # Initialize start time
    start_time = time.time()

    # Scrape data
    nfl_scraper = NFLDraftScraper()
    nfl_scraper.scrape_all_years()

    # Calculate process time
    end_time = time.time()
    process_time = end_time - start_time

    # Print results
    print(f"\nFINISHED! Time to complete: {round(process_time/60/60, 2)} minutes; {round(process_time/60, 2)} seconds")

