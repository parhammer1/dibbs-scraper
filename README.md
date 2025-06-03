# DIBBS Scraper and Analyzer

This project provides a simple example of how to scrape public solicitations from the DLA Internet Bid Board System (DIBBS) and display them with Streamlit. A GitHub Action runs the scraper every two hours and commits a CSV file with the latest data so Streamlit Cloud can redeploy automatically.

## Setup

1. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```
2. **Run the scraper manually (optional)**
   ```bash
   python dibbs_scraper.py
   ```
3. **Run the app**
   ```bash
   streamlit run app.py
   ```

The scraper uses `requests` and `BeautifulSoup` with placeholder logic. Update the selectors in `dibbs_scraper.py` when scraping the real DIBBS website.
