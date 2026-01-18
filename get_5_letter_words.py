with open('words_alpha.txt', 'r') as fileObj:
    word_list = [line.rstrip() for line in fileObj if len(line) == 6]
    print(word_list)