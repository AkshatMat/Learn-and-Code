import random

def is_valid_guess(user_input):
    try:
        number = int(user_input)
        return 1 <= number <= 100
    except Exception as e:
        return False

def get_valid_guess(prompt):
    while True:
        user_input = input(prompt)
        if is_valid_guess(user_input):
            return int(user_input)
        print("Invalid input! Please enter a number between 1 and 100.")

def play_number_game():
    target_number = random.randint(1, 100)
    guess_count = 0
    has_won = False
    
    print("\nWelcome to the Number Guessing Game!")
    print("Try to guess the number between 1 and 100.")
    
    while not has_won:
        guess = get_valid_guess("\nEnter your guess: ")
        guess_count += 1
        
        if guess < target_number:
            print("Too low! Try again.")
        elif guess > target_number:
            print("Too high! Try again.")
        else:
            print(f"\nCongratulations! You guessed the number in {guess_count} {'guess' if guess_count == 1 else 'guesses'}!")
            has_won = True

if __name__ == "__main__":
    play_number_game()