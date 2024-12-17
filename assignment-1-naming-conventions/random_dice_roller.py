import random

def roll_die(max_sides):
    number = random.randint(1, max_sides)
    return number


def play_dice_game():
    die_sides = 6
    is_playing = True
    while is_playing:
        user_input = input("Ready to roll? Enter Q to Quit: ")
        if user_input.lower() != "q":
            rolled_number = roll_die(die_sides)
            print("You have rolled a", rolled_number)
        else:
            is_playing = False

if __name__ == "__main__":
    play_dice_game()