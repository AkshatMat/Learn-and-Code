from client.api_client.api_client import get_all_apis, get_api_by_name, upsert_api, delete_api, update_api_status
from client.utils.console_format import print_article_list
from client.utils.time_utils import current_time_info
from client.utils.exception import APIError

def print_error(msg):
    print(f"\033[91m{msg}\033[0m")

def print_success(msg):
    print(f"\033[92m{msg}\033[0m")

def show_admin_menu(username):
    while True:
        date_str, time_str = current_time_info()
        print(f"\nWelcome to Admin Panel, {username}! Date: {date_str} Time: {time_str}\n")

        print("1. View All API Details")
        print("2. View Specific API Details")
        print("3. Add/Update API")
        print("4. Delete API")
        print("5. Update API Status")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_all_apis()
        elif choice == "2":
            show_specific_api()
        elif choice == "3":
            add_update_api()
        elif choice == "4":
            delete_api_menu()
        elif choice == "5":
            update_api_status_menu()
        elif choice == "6":
            print("\nLogging out...")
            exit()
        else:
            print_error("Invalid choice. Try again.")

def show_all_apis():
    try:
        print("\n" + "="*60)
        print("ALL API DETAILS")
        print("="*60)
        
        apis = get_all_apis()
        
        if not apis:
            print("No APIs found.")
            return
        
        for i, api in enumerate(apis, 1):
            print(f"\n{i}. API Name: {api['name']}")
            print(f"   Status: {api['status']}")
            print(f"   URL: {api['api_url']}")
            print(f"   Last Accessed: {api['last_accessed'] or 'Never'}")
            print("-" * 40)
            
    except APIError as e:
        print_error(f"Error fetching API details: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

def show_specific_api():
    try:
        api_name = input("Enter API name to view details: ").strip()
        
        if not api_name:
            print_error("API name cannot be empty.")
            return
        
        print("\n" + "="*60)
        print(f"API DETAILS FOR: {api_name}")
        print("="*60)
        
        api = get_api_by_name(api_name)
        
        if not api:
            print_error(f"API '{api_name}' not found.")
            return
        
        print(f"Name: {api['name']}")
        print(f"Status: {api['status']}")
        print(f"URL: {api['api_url']}")
        print(f"API Key: {'*' * len(api['api_key']) if api['api_key'] else 'Not set'}")
        print(f"Last Accessed: {api['last_accessed'] or 'Never'}")
        
    except APIError as e:
        print_error(f"Error fetching API details: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

def add_update_api():
    try:
        print("\n" + "="*60)
        print("ADD/UPDATE API")
        print("="*60)
        
        api_url = input("Enter API URL (must start with http:// or https://): ").strip()
        if not api_url:
            print_error("API URL cannot be empty.")
            return
        
        if not api_url.startswith(('http://', 'https://')):
            print_error("API URL must start with http:// or https://")
            return
        
        name = input("Enter API name (no spaces allowed): ").strip()
        if not name:
            print_error("API name cannot be empty.")
            return
        
        if any(char.isspace() for char in name):
            print_error("API name cannot contain spaces")
            return
        
        api_key = input("Enter API key: ").strip()
        if not api_key:
            print_error("API key cannot be empty.")
            return
        
        print("\nStatus options:")
        print("1. Active")
        print("2. Inactive")
        print("3. Maintenance")
        
        status_choice = input("Select status (1-3): ").strip()
        
        status_map = {
            "1": "Active",
            "2": "Inactive", 
            "3": "Maintenance"
        }
        
        status = status_map.get(status_choice, "Active")
        
        try:
            result = upsert_api(api_url, status, api_key, name)
            print_success(f"\n{result.get('message', 'API updated successfully!')}")
        except APIError as e:
            print_error(f"Error adding/updating API: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")

def delete_api_menu():
    try:
        print("\n" + "="*60)
        print("DELETE API")
        print("="*60)
        
        api_url = input("Enter API URL to delete: ").strip().strip('"')
        if not api_url:
            print_error("API URL cannot be empty.")
            return
        
        if not api_url.startswith(('http://', 'https://')):
            print_error("API URL must start with http:// or https://")
            return
        
        confirm = input(f"Are you sure you want to delete API with URL '{api_url}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        
        try:
            result = delete_api(api_url)
            print_success(f"\n{result.get('message', 'API deleted successfully!')}")
        except APIError as e:
            print_error(f"Error deleting API: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")

def update_api_status_menu():
    try:
        print("\n" + "="*60)
        print("UPDATE API STATUS")
        print("="*60)
        
        api_name = input("Enter API name: ").strip()
        if not api_name:
            print_error("API name cannot be empty.")
            return
        
        print("\nStatus options:")
        print("1. Active")
        print("2. Inactive")
        print("3. Maintenance")
        
        status_choice = input("Select new status (1-3): ").strip()
        
        status_map = {
            "1": "Active",
            "2": "Inactive", 
            "3": "Maintenance"
        }
        
        status = status_map.get(status_choice, "Active")
        
        try:
            result = update_api_status(api_name, status)
            print_success(f"\n{result.get('message', 'API status updated successfully!')}")
        except APIError as e:
            print_error(f"Error updating API status: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        
    except Exception as e:
        print_error(f"Unexpected error: {e}") 