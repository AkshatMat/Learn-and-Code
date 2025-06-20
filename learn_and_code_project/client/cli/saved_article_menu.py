from client.api_client.saved_article_client import get_saved_articles, save_article, delete_saved_article
from utils.console_format import print_article_list
from utils.time_utils import current_time_info

def show_saved_articles_menu(user_id, username):
    while True:
        date_str, time_str = current_time_info()
        print(f"\nWelcome to the News Application, {username}! Date: {date_str} Time: {time_str}\n")

        print("1. View Saved Articles")
        print("2. Delete a Saved Article")
        print("3. Back")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            articles = get_saved_articles(user_id)
            print_article_list(articles)

        elif choice == "2":
            article_id = input("Enter Article ID to delete: ")
            result = delete_saved_article(user_id, article_id)
            print(result.get("message", "No response"))

        elif choice == "3":
            break

        elif choice == "4":
            print("\nLogging out...")
            exit()

        else:
            print("Invalid choice. Try again.")
