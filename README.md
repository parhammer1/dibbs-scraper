# DIBBS Scraper and Analyzer

This project provides a simple example of how to scrape public solicitations from the DLA Internet Bid Board System (DIBBS), store them in a local SQLite database, and use OpenAI GPT to summarize solicitations or draft outreach emails. A Streamlit web interface allows a non-technical user to run the scraper and interact with the data.

## Setup

1. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   playwright install
   ```
2. **Set environment variables**
   Create a `.env` file or export `OPENAI_API_KEY` with your OpenAI credentials.

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

The scraper uses Playwright and includes a simple disclaimer handler. Selectors may need to be adjusted for the real DIBBS site.
