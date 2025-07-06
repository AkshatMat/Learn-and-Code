from client.cli.login_menu import show_login_menu
from client.cli.signup_menu import show_signup_menu
from client.cli.headlines_menu import show_headlines_menu
from client.cli.admin_menu import show_admin_menu  

def main():
    while True:
        print("\n==============================")
        print("  WELCOME TO NEWS AGGREGATOR")
        print("==============================")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_info = show_login_menu()
            if user_info:
                if user_info["role"] == "User":
                    show_headlines_menu(user_info["username"],user_info["user_id"])
                elif user_info["role"] == "Admin":
                    show_admin_menu(user_info["username"])
        elif choice == "2":
            show_signup_menu()
        elif choice == "3":
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Try again.")
