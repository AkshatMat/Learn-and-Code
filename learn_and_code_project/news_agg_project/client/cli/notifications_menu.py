from client.api_client.notification_client import fetch_preferences, update_category_preference, fetch_keywords, update_keywords, fetch_unviewed_notifications, mark_notification_viewed, mark_all_notifications_viewed
from client.utils.console_format import print_article_list

def show_notifications_menu(user_id):
    while True:
        print("\n========= NOTIFICATIONS =========")
        print("1. View Notifications")
        print("2. Configure Notifications")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            print('In cli.notifications_menu!!')
            articles = fetch_unviewed_notifications(user_id)
            if articles:
                print_article_list(articles)

                while True:
                    print("\n1. Mark one as viewed")
                    print("2. Mark all as viewed")
                    print("3. Back")
                    sub = input("Choose an option: ")

                    if sub == "1":
                        article_id = input("Enter article ID to mark as viewed: ")
                        articles = fetch_unviewed_notifications(user_id)
                        print_article_list(articles)
                    elif sub == "2":
                        result = mark_all_notifications_viewed(user_id)
                        print(result.get("message", "All marked viewed"))
                    elif sub == "3":
                        break
                    else:
                        print("Invalid input.")
            else:
                print("No new notifications.")

        elif choice == "2":
            configure_notifications(user_id)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Try again.")

def configure_notifications(user_id):
    while True:
        print("\n===== CONFIGURE NOTIFICATIONS =====")
        print("1. Category Preferences")
        print("2. Keyword Preferences")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            preferences_data = fetch_preferences(user_id)
            print("\n--- Category Preferences ---")
            if isinstance(preferences_data, list):
                categories = {}
                for item in preferences_data:
                    if isinstance(item, dict):
                        categories[item['category']] = item['is_enabled']
                    else:
                        categories[item[0]] = item[1]
            else:
                categories = preferences_data
            
            if categories:
                for idx, (cat, enabled) in enumerate(categories.items(), 1):
                    status = "Enabled" if enabled else "Disabled"
                    print(f"{idx}. {cat} - {status}")
                print(f"{len(categories)+1}. Back")

                sel = input("Choose a category to toggle or go back: ")
                if sel.isdigit() and 1 <= int(sel) <= len(categories):
                    cat = list(categories.keys())[int(sel)-1]
                    new_status = not categories[cat]
                    result = update_category_preference(user_id, cat, new_status)
                    print(result.get("message", "Updated"))
                elif sel == str(len(categories)+1):
                    continue
                else:
                    print("Invalid input.")
            else:
                print("No category preferences found.")
                
        elif choice == "2":
            keywords = fetch_keywords(user_id)
            print("\n--- Current Keywords ---")
            for kw in keywords:
                print(f"- {kw}")
            new_keywords = input("Enter comma-separated new keywords (or leave blank to skip): ").strip()
            if new_keywords:
                result = update_keywords(user_id, [kw.strip() for kw in new_keywords.split(",")])
                print(result.get("message", "Keywords updated"))

        elif choice == "3":
            break
        else:
            print("Invalid choice.")
