import requests
from client.config.settings import settings
from client.utils.exception import APIError

def user_login(username, password):
    try:
        payload = {"username": username, "password": password}
        response = requests.post(f"{settings.BASE_URL}/login_user/", json=payload)
        return response.json()
    except Exception as e:
        raise APIError(f"User login failed: {str(e)}")

def admin_login(username, password):
    try:
        payload = {"username": username, "password": password}
        response = requests.post(f"{settings.BASE_URL}/login_admin/", json=payload)
        return response.json()
    except Exception as e:
        raise APIError(f"Admin login failed: {str(e)}")
