with open('words_alpha.txt', 'r') as fileObj:
    words = filter(lambda x: len(x) == 6, fileObj.readlines())
    word_list = list(map(lambda x: x.strip('\n'), words))