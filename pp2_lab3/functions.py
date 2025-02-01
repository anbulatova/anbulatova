# Task 1
def grams_to_ounces(grams):
    ounces = 28.3495231 * grams
    return ounces
print(grams_to_ounces(123))

# Task 2
def fahrenheit_temperature(F):
    C = (5 / 9) * (F - 32)
    return C
print(fahrenheit_temperature(123))

# Task 3
def solve(numheads, numlegs):
    r = (numlegs - 2*numheads)/2
    c = numheads - r
    return r, c
print(solve(35, 94))

# Task 4
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    return list(filter(is_prime, numbers))

numbers = [10, 3, 5, 8, 13, 17, 20, 23]
print(filter_prime(numbers))

# Task 5
def permute(string, l=0):
    if l == len(string) - 1:
        print("".join(string))
        return
    
    for i in range(l, len(string)):
        string[l], string[i] = string[i], string[l]
        permute(string, l + 1)
        string[l], string[i] = string[i], string[l]  

user_input = list(input("Enter a string: "))
permute(user_input)

# Task 6
def reverse(s):
    words = s.split()
    reversed_s = ' '.join(reversed(words))
    return reversed_s
sentence = input("Enter a sentence: ")
print(reverse(sentence))

# Task 7
def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False


print(has_33([1, 3, 3]))  
print(has_33([1, 3, 1, 3]))  
print(has_33([3, 1, 3]))  

# Task 8
def spy_game(nums):
    code = [0, 0, 7]
    for num in nums:
        if num == code[0]:
            code.pop(0)
        if not code:
            return True
    return False

print(spy_game([1, 2, 4, 0, 0, 7, 5]))  
print(spy_game([1, 0, 2, 4, 0, 5, 7]))  
print(spy_game([1, 7, 2, 0, 4, 5, 0]))  

# Task 9
def sphere_volume(radius):
    pi = 3.14
    return (4/3) * pi * radius**3

print(sphere_volume(3))

# Task 10
def unique_elements(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

print(unique_elements([1, 2, 2, 3, 4, 4, 5]))  
print(unique_elements([7, 8, 9, 7, 7, 8]))  

# Task 11
def is_palindrome(s):
    cleaned_string = ""
    
    for char in s:
        if char.isalnum():  
            cleaned_string += char.lower()  
    return cleaned_string == cleaned_string[::-1]


print(is_palindrome("madam"))    
print(is_palindrome("hello"))  

# Task 12
def histogram(lst):
    for num in lst:
        print('*' * num)


histogram([1, 2, 3])

# Task 13
import random

def guess_the_number():
    print("Hello! What is your name?")
    name = input()  

    number_to_guess = random.randint(1, 20)  
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")
    print("Take a guess.")

    attempts = 0  

    while True:
        try:
            guess = int(input())  
            attempts += 1  

            if guess < number_to_guess:
                print("Your guess is too low.")
            elif guess > number_to_guess:
                print("Your guess is too high.")
            else:
                print(f"Good job, {name}! You guessed my number in {attempts} guesses!")
                break  
        except ValueError:  
            print("Please enter a valid number.")
 
guess_the_number()
