from get_5_letter_words import word_list
from marker import color_mapper
word_list_26 = [
    "apple",
    "beach",
    "brain",
    "cloud",
    "dance",
    "eagle",
    "flame",
    "glass",
    "house",
    "index",
    "juice",
    "light",
    "money",
    "night",
    "ocean",
    "party",
    "quiet",
    "river",
    "smile",
    "table",
    "under",
    "voice",
    "water",
    "young",
    "zebra"
]

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
    MODE = input(
        """
Type 'r' to randomly select a word
Type 's' to type in a word for your peers to guess: """)
    
    match MODE:
        case 's':
            import getpass
            WORD = getpass.getpass("Enter a word: ")
            if WORD in word_list:
                return WORD
            print("Chosen word is not a valid word. Choosing a random word...")
            return random.choice(word_list_26)
        case 'r':
            return random.choice(word_list_26)
    
def converter(word):
    letters = set(word)
    struct = {letter: [] for letter in letters}
    for i, letter in enumerate(word):
        letter_at = struct.get(letter)
        letter_at.append(i)
    return struct
    
def guess(struct, word):
    from colorama import Back, Fore, Style
    count = 0
    attempt = 0
    MAX_ATTEMPTS = 6
    color_maps = []
    guesses = []

    while attempt < MAX_ATTEMPTS:
        if count == 5:
            print(Style.RESET_ALL)
            break

        print(Style.RESET_ALL)
        print()
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
        guesses.append(guess)

        color_map_guess = color_mapper(word, guess)
        color_maps.append(color_map_guess)

        for color_map_guess, guess in zip(color_maps, guesses):
            print()
            count = 0
            for i, letter in enumerate(guess):
                if letter in struct:
                    print(Fore.RED + color_map_guess[i] + " " + guess[i], end=" ")
                    print(Style.RESET_ALL, end="")
                    if i in struct[letter]:
                        color_map_alphabet[ord(letter) - ord('a')] = Back.GREEN
                        count += 1
                    else:
                        if color_map_alphabet[ord(letter) - ord('a')] != Back.GREEN:
                            color_map_alphabet[ord(letter) - ord('a')] = Back.YELLOW
                else:
                    print(color_map_guess[i] + " " + guess[i], end=" ")
                    print(Style.RESET_ALL, end="")
                    if color_map_alphabet[ord(letter) - ord('a')] != Back.GREEN or color_map_alphabet[ord(letter) - ord('a')] != Back.YELLOW:
                        color_map_alphabet[ord(letter) - ord('a')] = Back.LIGHTBLACK_EX

        attempt += 1
    
    print(Style.RESET_ALL)
    if count == 5:
        print("You won!")
    else:
        print(f"The word was {word}.")

word = choose_word()
# word = "pupil"
# print(word)
if word:
    struct = converter(word)
    # print(struct)
    guess(struct, word)
        