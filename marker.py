def get_struct_2(word):
    struct_2 = {letter: [] for letter in word}
    for i, letter in enumerate(word):
        struct_2[letter].append(i)
    return struct_2

def color_mapper(word, guess):
    struct_2_word = get_struct_2(word)
    color_map = [None for _ in range(len(word))]
    
    from collections import Counter
    counter_word = Counter(word)

    from colorama import Back

    for i in range(len(word)):
        if word[i] == guess[i]:
            color_map[i] = Back.GREEN
            counter_word[word[i]] -= 1

    for i in range(len(word)):
        if guess[i] in counter_word and counter_word[guess[i]] > 0:
            if guess[i] in struct_2_word:
                if not i in struct_2_word[guess[i]]:
                    color_map[i] = Back.YELLOW
            else:
                color_map[i] = Back.LIGHTBLACK_EX

        elif color_map[i] != Back.GREEN:
            color_map[i] = Back.LIGHTBLACK_EX

    return color_map

def print_mapping(color_map, guess):
    from colorama import Style

    for i in range(len(guess)):
        print(color_map[i] + guess[i], end=" ")
    print(Style.RESET_ALL)


if __name__ == '__main__':
    word = 'eagee'
    for _ in range(6):
        guess = input("Guess the word: ")
        if not guess:
            break
        color_map = color_mapper(word, guess)
        color_map_truth = color_mapper(word, word)
        print_mapping(color_map, guess)
        print_mapping(color_map_truth, word)
