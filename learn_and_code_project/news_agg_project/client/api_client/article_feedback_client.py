import requests
from client.config.settings import settings

def give_feedback(user_id, article_id, feedback):
    response = requests.post(f"{settings.BASE_URL}/articles/feedback", json={
        "user_id": user_id,
        "article_id": article_id,
        "feedback": feedback
    })
    return response.json()
