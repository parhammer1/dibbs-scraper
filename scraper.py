"""Playwright-based scraper that saves results to SQLite."""

from typing import List, Dict
from datetime import datetime

from playwright.sync_api import sync_playwright

from database import init_db, insert_solicitation


def scrape_example(limit: int = 5) -> List[Dict]:
    """Scrape example.com with Playwright and return fake solicitation data."""
    results: List[Dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)
        page.goto("https://example.com", timeout=60000)
        heading = page.locator("h1").inner_text()
        for i in range(1, limit + 1):
            results.append(
                {
                    "solicitation": f"SOL-{i}",
                    "description": heading,
                    "deadline": datetime.utcnow().strftime("%Y-%m-%d"),
                    "buyer": "DIBBS",
                    "nsn": f"1234-00-000{i:04d}",
                    "fsc": f"{1000 + i}",
                    "posted": datetime.utcnow().strftime("%Y-%m-%d"),
                }
            )
        browser.close()
    return results


def run_scraper(limit: int = 5) -> None:
    """Scrape solicitations and store them in the database."""
    init_db()
    items = scrape_example(limit=limit)
    for item in items:
        insert_solicitation(item)


if __name__ == "__main__":
    run_scraper()
