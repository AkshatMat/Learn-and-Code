from client.api_client.signup_client import user_signup

def show_signup_menu():
    print("\n========= SIGN UP =========")
    username = input("Enter Username: ")
    email = input("Enter email: ")
    password = input("Enter Password: ")

    result = user_signup(username, email, password)
    if "message" in result:
        print(result["message"])
    else:
        print(result.get("error", "Signup failed."))
