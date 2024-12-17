import random

def is_valid_guess(user_input):
    if user_input.isdigit() and 1 <= int(user_input) <= 100:
        return True
    else:
        return False

def number_guessing_game():
    target_number = random.randint(1, 100)
    game_won = False
    user_guess = input("Guess a number between 1 and 100:")
    number_of_guesses = 0
    
    while not game_won:
        if not is_valid_guess(user_guess):
            user_guess = input("I won't count this one. Please enter a number between 1 to 100")
            continue
        else:
            number_of_guesses += 1
            user_guess = int(user_guess)

        if user_guess < target_number:
            user_guess = input("Too low. Guess again")
        elif user_guess > target_number:
            user_guess = input("Too High. Guess again")
        else:
            print("You guessed it in", number_of_guesses, "guesses!")
            game_won = True

number_guessing_game()