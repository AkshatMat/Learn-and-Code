import requests
from client.config.settings import settings

def user_signup(username, email, password):
    try:
        payload = {"username": username, "email": email, "password": password}
        response = requests.post(f"{settings.BASE_URL}/signup_user/", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
