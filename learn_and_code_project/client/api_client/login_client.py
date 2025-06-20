import requests
from client.config.settings import settings

def user_login(username, password):
    try:
        payload = {"username": username, "password": password}
        response = requests.post(f"{settings.BASE_URL}/login_user/", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def admin_login(username, password):
    try:
        payload = {"username": username, "password": password}
        response = requests.post(f"{settings.BASE_URL}/login_admin/", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
