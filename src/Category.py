from math import log
LAMBDA2 = 0.9

class Category:
    def __init__(self, category_name):
        self.__name = category_name
        self.__number_of_words = 0
        self.__unigram = {}
        self.__bigram = {}
        self.__probability = 0
        self.__TP = 0
        self.__FP = 0
        self.__FN = 0
        self.__f_measure = 0
        self.__recall = 0
        self.__precision = 0

    def __str__(self):
        return str(self.__name) + ' recall is: ' + str(self.__recall) + ' precision is: ' + str(self.__precision) + ' f is: ' + str(self.__f_measure)

    # check that two Category has same name or not?
    def __eq__(self, other):
        if isinstance(other, str):
            return self.__name == other
        if not isinstance(other, Category):
            return False
        return self.__name == other.__name

    def add_FP(self):
        self.__FP += 1

    def add_FN(self):
        self.__FN += 1

    def add_TP(self):
        self.__TP += 1

    def set_precision(self):
        self.__precision = self.__TP / (self.__TP + self.__FN)

    def set_recall(self):
        self.__recall = self.__TP / (self.__TP + self.__FP)

    def get_f(self):
        return self.__f_measure

    def f_measure(self):
        self.set_recall()
        self.set_precision()
        self.__f_measure = (2 * self.__recall * self.__precision) / \
            (self.__recall + self.__precision)

    def __hash__(self):
        return hash(self.__name)

    def get_name(self):
        return self.__name

    def get_unigrams(self):
        return self.__unigram

    def get_bigrams(self):
        return self.__bigram

    def add_unigram(self, word):
        if (self.__unigram.get(word) is None):
            self.__unigram[word] = 0
        self.__unigram[word] += 1
        self.__number_of_words += 1

    def add_bigram(self, words):
        w = words[0] + ' ' + words[1]
        if self.__bigram.get(w) is None:
            self.__bigram[w] = 0
        self.__bigram[w] += 1

    def add_sentence(self, sentence):
        words = sentence.split()
        for index in range(len(words)):
            self.add_unigram(words[index])
            if index != len(words) - 1:
                self.add_bigram((words[index], words[index+1]))
        self.__probability += 1

    def set_probability(self, count):
        self.__probability = log(self.__probability / count)
        # self.__probability = self.__probability / count

    def set_p(self, LAMBDA, word):
        ci_1 = 1
        if self.__unigram.get(word[0]) is not None:
            ci_1 = self.__unigram[word[0]]
        ci = 1
        if self.__unigram.get(word[1]) is not None:
            ci = self.__unigram[word[1]]
            pi = log(LAMBDA * ci / self.__number_of_words)
        else:
            pi = -1000

        if self.__bigram.get(word[0] + ' ' + word[1]) is not None :
            ci_1ci = self.__bigram.get(word[0] + ' ' + word[1])
            pi_1pi = log((1-LAMBDA)*ci_1ci / ci_1)
        else:
            pi_1pi = -1000
        # return LAMBDA*(LAMBDA2 * pi + (1-LAMBDA2)/self.__number_of_words)+ (1-LAMBDA) * pi_1pi

        return  pi + pi_1pi
    def get_p(self):
        return self.__probability
