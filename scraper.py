"""Wrapper to run the DIBBS scraper and store results."""
from dibbs_scraper import scrape_latest
from database import init_db, insert_solicitation


def run_scraper(limit: int = 5) -> None:
    """Scrape latest solicitations and store them in the database."""
    init_db()
    items = scrape_latest(limit=limit)
    for item in items:
        insert_solicitation(item)
