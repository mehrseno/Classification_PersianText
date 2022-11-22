from Category import Category
import sys
from collections import defaultdict
import numpy as np

LAMBDA = 0.7
TOKEN = '@@@@@@@@@@'
START = '<S> ' 

categories = []
test_set_sentences = []

def add_to_categories(line):
    category_name = line[0]
    category_sentence = line[1]
    category_sentence = START + category_sentence
    if category_name not in categories:
        categories.append(Category(category_name))

    categories[categories.index(category_name)].add_sentence(category_sentence)


def save_file(file_name, words_list):
    f = open(file_name, 'w')
    for word in words_list:
        f.write(str(word[0]) + ' ' + str(word[1]) + '\n')
    f.close()


def save_ngrams_to_file():
    for category in categories:
        save_file('./Ngrams/' + category.get_name() +
                  '-1.txt', category.get_unigrams().items())
        save_file('./Ngrams/' + category.get_name() +
                  '-2.txt', category.get_bigrams().items())


def create_ngrams(file_path="./dataset/HAM-Train.txt"):
    try:
        f = open(file_path, 'r')
        print('file opened...')
    except OSError as e:
        print('error in opening training file, error message is: ' + e.strerror)
        sys.exit()
    line_number = 0
    for line in f:
        line_number += 1
        print(line_number)
        add_to_categories(line.split(TOKEN))
    f.close()

    for category in categories:
        category.set_probability(line_number)
        print(category)

    # save_ngrams_to_file()


def read_test_set(file_path="./dataset/HAM-Test.txt"):
    try:
        f = open(file_path, 'r')
        print('test set is oppened...')
    except OSError as e:
        print('can not open test set, error message is ' + e.strerror )
    for (line_n, line) in enumerate(f):
        line = line.split(TOKEN)
        test_set_sentences.append([line[0], float('-inf'), ''])
        line[1] = START + line[1]
        for category in categories:
            words = line[1].split()
            line_p = 0
            for index in range(1, len(words)) :
                line_p += category.set_p(LAMBDA, (words[index - 1], words[index]))
            if  line_p + category.get_p() > test_set_sentences[line_n][1]:
                test_set_sentences[line_n][1] = line_p + category.get_p()
                test_set_sentences[line_n][2] = category.get_name()        
    
def calc_fscore():
    for instance in test_set_sentences:
        if instance[0] == instance[2]:
            for topic in categories:
                if topic == instance[0]:
                    topic.add_TP()
                    break
        else:
            for topic in categories:
                if topic == instance[0]:
                    topic.add_FN()
                elif topic == instance[2]:
                    topic.add_FP()
    for topic in categories:
        topic.f_measure()

def main():
    create_ngrams()
    read_test_set()
    cnt = 0
    cc = 0
    eq = 0
    ej = 0
    si = 0
    ad = 0 
    va = 0
    for c in test_set_sentences:
        if c[0] == c[2]:
            cnt += 1 
        if c[2] == 'اجتماعی':
            ej += 1
        if c[2] == 'اقتصاد':
            eq += 1
        if c[2] == 'ادب و هنر' :
            ad +=1
        if c[2] == 'سیاسی':
            si +=1
        if c[2] == 'ورزش':
            va += 1
    
    print(cnt)

    print(ej)
    print(eq)
    print(ad)
    print(si)
    print(va)
    calc_fscore()
    f = open(str(LAMBDA) + 'result.txt ', 'w')
    for topic in categories:
        f.write(str(topic) + '\n')
        print(topic)
    f.close()

if __name__ == "__main__":
    main()