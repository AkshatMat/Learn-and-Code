def calculate_armstrong_sum(number):
    digit_sum = 0
    digit_count = 0

    temp_number = number
    while temp_number > 0:
        digit_count = digit_count + 1
        temp_number = temp_number // 10

    temp_number = number
    for _ in range(1, temp_number + 1):
        current_digit = temp_number % 10
        digit_sum = digit_sum + (current_digit ** digit_count)
        temp_number //= 10
    return digit_sum

user_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))

if (user_number == calculate_armstrong_sum(user_number)):
    print(f"\n {user_number} is Armstrong Number.\n")
else:
    print(f"\n {user_number} is Not a Armstrong Number.\n")