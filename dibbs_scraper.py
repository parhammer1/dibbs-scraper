"""Simple requests-based scraper for sample DIBBS data."""

from typing import List, Dict
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

DATA_PATH = "data/dibbs_data.csv"


def scrape_latest(limit: int = 5) -> List[Dict]:
    """Fetch example.com and return placeholder solicitation data."""
    response = requests.get("https://example.com", timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")
    heading = soup.find("h1").get_text(strip=True)
    results = []
    for i in range(1, limit + 1):
        results.append(
            {
                "solicitation": f"SOL-{i}",
                "description": heading,
                "nsn": f"1234-00-000{i:04d}",
                "fsc": f"{1000 + i}",
                "quantity": 10 * i,
            }
        )
    return results


def save_to_csv(records: List[Dict]) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df = pd.DataFrame(records)
    df.to_csv(DATA_PATH, index=False)


if __name__ == "__main__":
    data = scrape_latest()
    save_to_csv(data)
