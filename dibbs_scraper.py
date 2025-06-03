"""Playwright-based scraper for public DIBBS solicitations."""

from typing import List, Dict
import logging

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://dibbs.defense.gov"  # base site URL


def _accept_disclaimer(page) -> None:
    """Handle potential disclaimer or landing page with an 'OK' button."""
    try:
        if page.locator("text=OK").is_visible(timeout=3000):
            page.click("text=OK")
            page.wait_for_load_state("networkidle")
    except PlaywrightTimeoutError:
        pass


def scrape_latest(limit: int = 5) -> List[Dict]:
    """Scrape the latest public solicitations from DIBBS."""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"{BASE_URL}/RFQ"  # Example listing page
        logger.info("Loading %s", url)
        page.goto(url, timeout=60000)
        _accept_disclaimer(page)

        # This is a placeholder selector; adjust according to actual page layout
        rows = page.locator("table tr").all()[1:limit+1]
        for row in rows:
            cells = row.locator("td").all()
            solicitation = cells[0].inner_text().strip()
            description = cells[1].inner_text().strip()
            deadline = cells[2].inner_text().strip()
            buyer = cells[3].inner_text().strip()
            results.append(
                {
                    "solicitation": solicitation,
                    "description": description,
                    "deadline": deadline,
                    "buyer": buyer,
                }
            )
        browser.close()
    return results


def scrape_solicitation_detail(solicitation: str) -> Dict:
    """Scrape detailed information for a specific solicitation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"{BASE_URL}/solicitations/{solicitation}"
        logger.info("Loading %s", url)
        page.goto(url, timeout=60000)
        _accept_disclaimer(page)

        # Placeholder selectors for detail fields
        description = page.locator(".description").inner_text()
        deadline = page.locator(".deadline").inner_text()
        buyer = page.locator(".buyer").inner_text()
        browser.close()
        return {
            "solicitation": solicitation,
            "description": description.strip(),
            "deadline": deadline.strip(),
            "buyer": buyer.strip(),
        }


if __name__ == "__main__":
    for item in scrape_latest():
        print(item)
