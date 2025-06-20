import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from client.api_client.login_client import user_login, admin_login

def show_login_menu():
    while True:
        print("\n========== LOGIN ==========")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            response = user_login(username, password)
            if "token" in response:
                print("User login successful!")
                return {"username": username, "role": "User", "token": response["token"], "user_id": response["user_id"]}
            else:
                print(response.get("error", "Login failed."))

        elif choice == "2":
            username = input("Admin Username: ")
            password = input("Admin Password: ")
            response = admin_login(username, password)
            if "token" in response:
                print("Admin login successful!")
                return {"username": username, "role": "Admin", "token": response["token"]}
            else:
                print(response.get("error", "Login failed."))

        elif choice == "3":
            return None
        else:
            print("Invalid choice. Try again.")
