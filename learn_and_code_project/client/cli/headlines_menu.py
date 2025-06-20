from client.api_client.headlines_client import fetch_today_headlines, fetch_range_headlines, search_headlines_by_keyword
from client.api_client.saved_article_client import save_article, get_saved_articles, delete_saved_article
from client.utils.console_format import print_article_list
from client.utils.time_utils import current_time_info

def show_headlines_menu(username, user_id):
    while True:
        date_str, time_str = current_time_info()
        print(f"\nWelcome to the News Application, {username}! Date: {date_str} Time: {time_str}\n")

        print("1. Today's Headlines")
        print("2. Headlines by Date Range")
        print("3. Saved Articles")
        print("4. Search by Keyword")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice in ["1", "2"]:
            if choice == "1":
                category = input("Enter category (or All): ")
                articles = fetch_today_headlines(category)
            else:
                start = input("Enter start date (YYYY-MM-DD): ")
                end = input("Enter end date (YYYY-MM-DD): ")
                category = input("Enter category (or All): ")
                articles = fetch_range_headlines(start, end, category)

            print_article_list(articles)

            while True:
                print("\n1. Save Article")
                print("2. Back to Headlines Menu")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    article_id = input("Enter Article ID to save: ")
                    result = save_article(user_id, article_id)
                    print(result.get("message", "No response"))
                elif sub_choice == "2":
                    break
                else:
                    print("Invalid choice. Try again.")

        elif choice == "3":
            articles = get_saved_articles(user_id)
            print_article_list(articles)

            while True:
                print("\n1. Back")
                print("2. Logout")
                print("3. Delete Saved Article")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    print("\nLogging out...")
                    exit()
                elif sub_choice == "3":
                    article_id = input("Enter Article ID to delete: ")
                    result = delete_saved_article(user_id, article_id)
                    print(result.get("message", "No response"))
                else:
                    print("Invalid choice. Try again.")

        elif choice == "4":
            keyword = input("Enter keyword to search: ")
            articles = search_headlines_by_keyword(keyword)
            print_article_list(articles)

            while True:
                print("\n1. Save Article")
                print("2. Back to Headlines Menu")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    article_id = input("Enter Article ID to save: ")
                    result = save_article(user_id, article_id)
                    print(result.get("message", "No response"))
                elif sub_choice == "2":
                    break
                else:
                    print("Invalid choice. Try again.")

        elif choice == "5":
            print("\nLogging out...")
            exit()
        else:
            print("Invalid choice. Try again.")
