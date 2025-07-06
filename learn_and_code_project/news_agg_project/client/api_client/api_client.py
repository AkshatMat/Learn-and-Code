import requests
from client.config.settings import settings
from client.utils.exception import APIError

def get_all_apis():
    try:
        response = requests.get(f"{settings.BASE_URL}/admin/apis")
        response.raise_for_status()
        data = response.json()
        return data.get("apis", [])
    except Exception as e:
        raise APIError(f"Failed to get API details: {str(e)}")

def get_api_by_name(api_name: str):
    try:
        response = requests.get(f"{settings.BASE_URL}/admin/apis/{api_name}")
        response.raise_for_status()
        data = response.json()
        return data.get("api")
    except Exception as e:
        raise APIError(f"Failed to get API by name: {str(e)}")

def upsert_api(api_url: str, status: str, api_key: str, name: str):
    try:
        payload = {
            "api_url": api_url,
            "status": status,
            "api_key": api_key,
            "name": name
        }
        response = requests.post(f"{settings.BASE_URL}/admin/apis", json=payload)
        
        if response.status_code == 422:
            error_data = response.json()
            error_details = error_data.get('detail', [])
            if isinstance(error_details, list):
                error_messages = []
                for error in error_details:
                    if 'msg' in error and 'loc' in error:
                        field = '.'.join(str(x) for x in error['loc'])
                        error_messages.append(f"{field}: {error['msg']}")
                raise APIError(f"Validation errors: {'; '.join(error_messages)}")
            else:
                raise APIError(f"Validation error: {error_details}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APIError(f"Failed to upsert API: {str(e)}")
    except Exception as e:
        raise APIError(f"Failed to upsert API: {str(e)}")

def delete_api(api_url: str):
    try:
        response = requests.delete(f"{settings.BASE_URL}/admin/apis", json={"api_url": api_url})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise APIError(f"Failed to delete API: {str(e)}")

def update_api_status(api_name: str, status: str):
    try:
        payload = {
            "api_name": api_name,
            "status": status
        }
        response = requests.put(f"{settings.BASE_URL}/admin/apis/status", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise APIError(f"Failed to update API status: {str(e)}") 