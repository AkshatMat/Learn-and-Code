import requests
from client.config.settings import settings

def fetch_preferences(user_id):
    response = requests.get(f"{settings.BASE_URL}/notifications/preferences/{user_id}")
    response.raise_for_status()
    return response.json()

def update_category_preference(user_id, category, enabled):
    payload = {
        "user_id": user_id,
        "category": category,
        "enabled": enabled
    }
    response = requests.post(f"{settings.BASE_URL}/notifications/preferences/category", json=payload)
    response.raise_for_status()
    return response.json()

def fetch_keywords(user_id):
    response = requests.get(f"{settings.BASE_URL}/notifications/preferences/keywords/{user_id}")
    response.raise_for_status()
    return response.json()

def update_keywords(user_id, keywords):
    payload = {
        "user_id": user_id,
        "keywords": keywords
    }
    response = requests.post(f"{settings.BASE_URL}/notifications/preferences/keywords", json=payload)
    response.raise_for_status()
    return response.json()

def fetch_unviewed_notifications(user_id):
    print("In api_client notification_clien")
    response = requests.get(f"{settings.BASE_URL}/notifications/preferences/unviewed/{user_id}")
    response.raise_for_status()
    return response.json()

def mark_notification_viewed(user_id, article_id):
    payload = {
        "user_id": user_id,
        "article_id": article_id
    }
    response = requests.post(f"{settings.BASE_URL}/notifications/viewed", json=payload)
    response.raise_for_status()
    return response.json()

def mark_all_notifications_viewed(user_id):
    response = requests.post(f"{settings.BASE_URL}/notifications/viewed_all", json={"user_id": user_id})
    response.raise_for_status()
    return response.json()
