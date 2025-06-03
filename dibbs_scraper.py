"""DIBBS Scraper and Analysis Toolkit

This script outlines a basic pipeline to scrape DIBBS solicitation data,
optionally analyze it with OpenAI's GPT API, and save the results.
It uses Playwright for browser automation and pandas for data handling.

Prerequisites (install with pip):
    pip install playwright pandas openai flask
    playwright install

Note: Ensure you comply with DIBBS terms of service. The code assumes
access to public, logged-out pages only.
"""

from __future__ import annotations
import os
import time
from dataclasses import dataclass, asdict
from typing import List, Dict

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd

try:
    import openai
except ImportError:  # openai is optional
    openai = None


@dataclass
class Solicitation:
    """Dataclass representing a DIBBS solicitation."""
    number: str
    title: str
    closing_date: str
    detail_url: str
    item_description: str | None = None
    quantity: str | None = None
    buyer: str | None = None


class DibbsScraper:
    """Scraper encapsulating browser logic for DIBBS."""

    BASE_URL = "https://www.dibbs.bsm.dla.mil"  # Example base URL

    def __init__(self, headless: bool = True):
        self.headless = headless

    def _accept_disclaimer(self, page):
        """Accept disclaimer/landing page if present."""
        try:
            # Selector should match the actual button text or id.
            page.click("text='I Accept'", timeout=5000)
        except PlaywrightTimeoutError:
            pass  # Assume already past the disclaimer

    def fetch_solicitations(self) -> List[Solicitation]:
        """Navigate to solicitation list and parse entries."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.BASE_URL, wait_until="load")
            self._accept_disclaimer(page)

            # Example: navigate to a particular search results page
            page.goto(f"{self.BASE_URL}/solicitations/" , wait_until="load")

            solicitations: List[Solicitation] = []
            # Adjust selector according to real table rows
            rows = page.query_selector_all("table#solicitations tr")
            for row in rows[1:]:  # skip header
                cols = row.query_selector_all("td")
                if len(cols) < 4:
                    continue
                number = cols[0].inner_text().strip()
                title = cols[1].inner_text().strip()
                closing_date = cols[2].inner_text().strip()
                detail_url = cols[0].query_selector("a").get_attribute("href")
                solicitations.append(
                    Solicitation(
                        number=number,
                        title=title,
                        closing_date=closing_date,
                        detail_url=self.BASE_URL + detail_url,
                    )
                )
            browser.close()
        return solicitations

    def fetch_details(self, solicitation: Solicitation) -> Solicitation:
        """Navigate to solicitation detail page and populate additional fields."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(solicitation.detail_url, wait_until="load")
            self._accept_disclaimer(page)

            try:
                solicitation.item_description = page.query_selector("#itemDesc").inner_text().strip()
            except AttributeError:
                solicitation.item_description = None
            try:
                solicitation.quantity = page.query_selector("#qty").inner_text().strip()
            except AttributeError:
                solicitation.quantity = None
            try:
                solicitation.buyer = page.query_selector("#buyer").inner_text().strip()
            except AttributeError:
                solicitation.buyer = None

            browser.close()
        return solicitation


class Storage:
    """Handle storing scraped data."""

    def __init__(self, csv_path: str = "solicitations.csv"):
        self.csv_path = csv_path

    def save_to_csv(self, solicitations: List[Solicitation]):
        df = pd.DataFrame([asdict(s) for s in solicitations])
        if os.path.exists(self.csv_path):
            # Avoid duplicates by solicitation number
            existing = pd.read_csv(self.csv_path)
            df = pd.concat([existing, df]).drop_duplicates(subset=["number"])
        df.to_csv(self.csv_path, index=False)


class AIHelper:
    """Wrapper around OpenAI GPT for analysis and email drafting."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        if openai is None:
            raise ImportError("openai package not installed")
        self.model = model
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def summarize_solicitations(self, solicitations: List[Solicitation]) -> str:
        """Ask GPT to summarize or prioritize solicitations."""
        prompt = "Summarize these DIBBS solicitations and rank by priority:\n"
        for s in solicitations:
            prompt += f"\n{s.number}: {s.title} closing {s.closing_date}"
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]

    def draft_email(self, solicitation: Solicitation) -> str:
        """Draft outreach email for a solicitation."""
        prompt = (
            f"Draft a short outreach email regarding solicitation {solicitation.number} "
            f"for item '{solicitation.item_description}'."
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]


# Optional: minimal Flask app skeleton
try:
    from flask import Flask, jsonify
except ImportError:
    Flask = None

if Flask:
    app = Flask(__name__)
    scraper = DibbsScraper(headless=True)
    storage = Storage()

    @app.route("/scrape")
    def scrape_route():
        sols = scraper.fetch_solicitations()
        for s in sols:
            scraper.fetch_details(s)
        storage.save_to_csv(sols)
        return jsonify({"status": "ok", "count": len(sols)})

    @app.route("/data")
    def data_route():
        if os.path.exists(storage.csv_path):
            df = pd.read_csv(storage.csv_path)
            return df.to_json(orient="records")
        return jsonify([])

    @app.route("/analyze")
    def analyze_route():
        if not openai:
            return jsonify({"error": "openai not installed"}), 500
        if os.path.exists(storage.csv_path):
            df = pd.read_csv(storage.csv_path)
            sols = [Solicitation(**row) for row in df.to_dict("records")]
            helper = AIHelper()
            summary = helper.summarize_solicitations(sols)
            return jsonify({"summary": summary})
        return jsonify({"error": "no data"}), 404

    if __name__ == "__main__":
        app.run(debug=True)


if __name__ == "__main__" and not Flask:
    # Example CLI usage without Flask
    scraper = DibbsScraper(headless=True)
    storage = Storage()
    solicitations = scraper.fetch_solicitations()
    for sol in solicitations:
        scraper.fetch_details(sol)
    storage.save_to_csv(solicitations)
    print(f"Saved {len(solicitations)} solicitations to {storage.csv_path}")
