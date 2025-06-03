from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
from typing import Dict
import os


def scrape_dibbs(solicitation_number: str) -> Dict:
    """Scrape DIBBS solicitation details."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"https://dibbs.defense.gov/solicitations/{solicitation_number}"
        try:
            page.goto(url, timeout=60000)
        except PlaywrightTimeoutError:
            browser.close()
            raise RuntimeError(f"Timeout loading page for {solicitation_number}")

        try:
            price_text = page.inner_text("css=.price-field-selector")
            status_text = page.inner_text("css=.status-field-selector")
            deadline_text = page.inner_text("css=.deadline-selector")
        except Exception:
            browser.close()
            raise RuntimeError(
                f"Could not find expected fields on {solicitation_number}"
            )
        browser.close()

    try:
        price = float(price_text.replace("$", "").replace(",", "").strip())
    except Exception:
        price = None

    return {
        "solicitation": solicitation_number,
        "price": price,
        "status": status_text.strip(),
        "deadline": deadline_text.strip(),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python dibbs_scraper.py <solicitation_number>")
        sys.exit(1)

    solicitation_number = sys.argv[1]
    result = scrape_dibbs(solicitation_number)
    print(result)
