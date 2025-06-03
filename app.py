from flask import Flask, jsonify

from dibbs_scraper import scrape_dibbs

app = Flask(__name__)

@app.route("/")
def index():
    return (
        "DIBBS Scraper Service is running.\n"
        "Use GET /scrape/<solicitation_number> to retrieve data."
    )

@app.route("/scrape/<string:solicitation>")
def scrape(solicitation):
    try:
        result = scrape_dibbs(solicitation)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=True)
