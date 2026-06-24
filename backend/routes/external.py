"""
External API integrations for Fahamu.
Fetches live data from public Kenyan/global APIs and proxies them to the frontend.
"""
import os
import requests
from flask import Blueprint, jsonify, request

external_bp = Blueprint("external", __name__)

# --- Kenya news via NewsAPI (public endpoint, free tier) ---
NEWS_API_BASE = "https://newsapi.org/v2"
# In production, store this in .env and read with python-dotenv
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "YOUR_NEWS_API_KEY")

@external_bp.route("/news", methods=["GET"])
def get_kenya_news():
    """Fetch latest Kenya civic/government news from NewsAPI."""
    category = request.args.get("category", "government")
    query = f"Kenya {category}"
    try:
        resp = requests.get(
            f"{NEWS_API_BASE}/everything",
            params={
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 10,
                "apiKey": NEWS_API_KEY
            },
            timeout=5
        )
        data = resp.json()
        if data.get("status") == "ok":
            articles = [
                {
                    "title": a.get("title"),
                    "source": a.get("source", {}).get("name"),
                    "url": a.get("url"),
                    "published_at": a.get("publishedAt"),
                    "description": a.get("description"),
                    "image": a.get("urlToImage")
                }
                for a in data.get("articles", [])
                if a.get("title") and "[Removed]" not in a.get("title", "")
            ]
            return jsonify(articles)
        else:
            return jsonify({"error": "News API error", "detail": data.get("message")}), 502
    except Exception as e:
        # Return mock data if API is unavailable (dev mode)
        return jsonify(_mock_news(category))

def _mock_news(category):
    """Fallback mock news for development without an API key."""
    return [
        {
            "title": f"Kenya {category.title()} Update — Mock",
            "source": "Fahamu Dev",
            "url": "#",
            "published_at": "2026-06-13T08:00:00Z",
            "description": "This is mock data. Add your NewsAPI key in routes/external.py to get live news.",
            "image": None
        }
    ]

# --- KRA exchange rate / forex (public endpoint) ---
@external_bp.route("/forex", methods=["GET"])
def get_forex():
    """Fetch KES exchange rates from a public forex API."""
    try:
        resp = requests.get(
            "https://api.exchangerate-api.com/v4/latest/KES",
            timeout=5
        )
        data = resp.json()
        rates = data.get("rates", {})
        # Return only the most relevant currencies for Kenya
        relevant = {k: rates[k] for k in ["USD", "EUR", "GBP", "UGX", "TZS", "ETB"] if k in rates}
        return jsonify({
            "base": "KES",
            "date": data.get("date"),
            "rates": relevant
        })
    except Exception as e:
        return jsonify({"error": "Forex API unavailable", "detail": str(e)}), 503

# --- eCitizen service status (mocked — no public API exists) ---
@external_bp.route("/ecitizen-services", methods=["GET"])
def get_ecitizen_services():
    """Returns a curated list of eCitizen digital services with their direct links."""
    services = [
        {"name": "National ID Application", "url": "https://www.ecitizen.go.ke/", "category": "identity"},
        {"name": "KRA iTax Portal", "url": "https://itax.kra.go.ke/", "category": "tax"},
        {"name": "NTSA Tims Portal", "url": "https://tims.ntsa.go.ke/", "category": "transport"},
        {"name": "NHIF Self Service", "url": "https://selfservice.nhif.or.ke/", "category": "health"},
        {"name": "NSSF Member Portal", "url": "https://portal.nssf.or.ke/", "category": "tax"},
        {"name": "Huduma Centre Locator", "url": "https://www.hudumakenya.go.ke/", "category": "identity"},
        {"name": "Lands Registry (Ardhisasa)", "url": "https://ardhisasa.lands.go.ke/", "category": "land"},
        {"name": "Business Registration (BRS)", "url": "https://brs.go.ke/", "category": "business"},
        {"name": "Kenya Power Bill Pay", "url": "https://www.kplc.co.ke/", "category": "water"},
        {"name": "IEBC Voter Registration", "url": "https://www.iebc.or.ke/", "category": "elections"},
    ]
    category = request.args.get("category")
    if category:
        services = [s for s in services if s["category"] == category]
    return jsonify(services)
