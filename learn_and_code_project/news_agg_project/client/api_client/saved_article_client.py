import requests
from client.config.settings import settings
from client.utils.exception import APIError

def save_article(user_id, article_id):
    try:
        response = requests.post(f"{settings.BASE_URL}/articles/save_article", json={"user_id": user_id, "article_id": article_id})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise APIError(f"Failed to save article: {str(e)}")

def get_saved_articles(user_id):
    response = requests.get(f"{settings.BASE_URL}/articles/saved_articles/{user_id}")
    return response.json()

def delete_saved_article(user_id, article_id):
    response = requests.delete(f"{settings.BASE_URL}/articles/delete_article", json={"user_id": user_id, "article_id": article_id})
    return response.json()

