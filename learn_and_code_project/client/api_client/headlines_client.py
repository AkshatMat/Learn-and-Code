import requests
from client.config.settings import settings

def fetch_today_headlines(category="All"):
    try:
        response = requests.get(f"{settings.BASE_URL}/headlines/today", params={"category": category})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching today's headlines: {e}")
        return []


def fetch_range_headlines(start_date, end_date, category="All"):
    try:
        payload = {
            "start_date": start_date,
            "end_date": end_date,
            "category": category
        }
        response = requests.post(f"{settings.BASE_URL}/headlines/range", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching range headlines: {e}")
        return []

def search_headlines_by_keyword(keyword):
    try:
        response = requests.get(f"{settings.BASE_URL}/headlines/search", params={"keyword": keyword})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching headlines: {e}")
        return []