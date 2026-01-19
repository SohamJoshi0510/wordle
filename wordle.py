from get_5_letter_words import word_list
from marker import color_mapper
# word_list = [
#     "apple",
#     "beach",
#     "brain",
#     "cloud",
#     "dance",
#     "eagle",
#     "flame",
#     "glass",
#     "house",
#     "index",
#     "juice",
#     "light",
#     "money",
#     "night",
#     "ocean",
#     "party",
#     "quiet",
#     "river",
#     "smile",
#     "table",
#     "under",
#     "voice",
#     "water",
#     "young",
#     "zebra"
# ]

alphabet = [chr(ord('a') + i) for i in range(26)]
color_map_alphabet = [None for i in range(26)]

import random

def print_alphabet():
    from colorama import Style, Fore, Back
    for color, alph in zip(color_map_alphabet, alphabet):
        if color:
            if color != Back.LIGHTBLACK_EX:
                print(color + Fore.RED + " " + alph, end=" ")
            else:
                print(color + " " + alph, end=" ")
        else:
            print(alph, end=" ")
        print(Style.RESET_ALL, end=" ")
    print()

def choose_word():
    return random.choice(word_list)
    
def converter(word):
    letters = set(word)
    struct = {letter: [] for letter in letters}
    for i, letter in enumerate(word):
        letter_at = struct.get(letter)
        letter_at.append(i)
    return struct
    
def guess(struct, word):
    from colorama import Back, Fore, Style
    # print(Style.RESET_ALL)
    guessed = False
    attempt = 0
    MAX_ATTEMPTS = 6
    while attempt < MAX_ATTEMPTS:
        if guessed:
            print(Style.RESET_ALL)
            break

        print(Style.RESET_ALL)
        print_alphabet()
        print()

        guess = input(f"[ATTEMPT {attempt + 1}/{MAX_ATTEMPTS}]\nGuess the word: ").lower()
        if guess == "exit" or guess == "cls":
            break
                
        if len(guess) < 5:
            print("The word is 5 letters long!")
            continue

        if not guess in word_list:
            print("The guess does not exist in the corpus!")
            continue
        guess = guess[:5]
        guessed = True

        color_map_guess = color_mapper(word, guess)

        for i, letter in enumerate(guess):
            if letter in struct:
                print(Fore.RED + color_map_guess[i] + " " + guess[i], end=" ")
                if i in struct[letter]:
                    color_map_alphabet[ord(letter) - ord('a')] = Back.GREEN
                else:
                    guessed = False
                    if color_map_alphabet[ord(letter) - ord('a')] != Back.GREEN:
                        color_map_alphabet[ord(letter) - ord('a')] = Back.YELLOW
            else:
                guessed = False
                print(color_map_guess[i] + " " + guess[i], end=" ")
                if color_map_alphabet[ord(letter) - ord('a')] != Back.GREEN or color_map_alphabet[ord(letter) - ord('a')] != Back.YELLOW:
                    color_map_alphabet[ord(letter) - ord('a')] = Back.LIGHTBLACK_EX
        attempt += 1
    
    print(Style.RESET_ALL)
    if guessed:
        print("You won!")
    else:
        print(f"The word was {word}.")

word = choose_word()
# word = "pupil"
# print(word)
struct = converter(word)
# print(struct)
guess(struct, word)
        