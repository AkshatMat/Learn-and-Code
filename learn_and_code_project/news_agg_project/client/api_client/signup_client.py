import requests
from client.config.settings import settings
from client.utils.exception import APIError

def user_signup(username, email, password):
    try:
        payload = {"username": username, "email": email, "password": password}
        response = requests.post(f"{settings.BASE_URL}/signup_user/", json=payload)
        return response.json()
    except Exception as e:
        raise APIError(f"User signup failed: {str(e)}")
