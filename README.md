# DIBBS Scraper and Analyzer

This project provides a simple example of how to scrape public solicitations from the DLA Internet Bid Board System (DIBBS) and display them with Streamlit. A GitHub Action runs a Playwright-based scraper on a schedule and uploads an updated SQLite database as a workflow artifact so Streamlit Cloud can redeploy automatically.

## Setup

1. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```
2. **Run the scraper manually (optional)**
   ```bash
   python scraper.py
   ```
3. **Run the app**
   ```bash
   streamlit run app.py
   ```

The scraper uses Playwright with placeholder logic. Update the selectors in `scraper.py` when scraping the real DIBBS website. GitHub Actions runs `scraper.py` every 12 hours and uploads `data/solicitations.db` as an artifact instead of committing it.
