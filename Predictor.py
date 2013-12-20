import time
import glob
import math
import random
from collections import defaultdict


class Predictor:
    '''
    Predictor which will do prediction on emails
    '''
    def __init__(self, spamFolder, hamFolder):
        self.__createdAt = time.strftime("%d %b %H:%M:%S", time.gmtime())
        self.__spamFolder = spamFolder
        self.__hamFolder = hamFolder
        # do training on spam and ham
        self.__train__()

    def __train__(self):
        '''train model on spam and ham'''
        # the following code is only an naive example,
        # implement your own training methond here
        spamCount = len(glob.glob(self.__spamFolder+'/*'))
        hamCount = len(glob.glob(self.__hamFolder+'/*'))

        # Set up the vocabulary for all files in the training set
        vocab = defaultdict(int)
        self.spam = self.files2countdict(glob.glob(self.__spamFolder+"/*"))
        vocab.update(self.spam[1])
        self.ham = self.files2countdict(glob.glob(self.__hamFolder+"/*"))
        vocab.update(self.ham[1])

        # Set all counts to 0
        vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))

        classes = []
        dirs = [self.spam, self.ham]
        for dir in dirs:
            # Initialize to zero counts
            countdict = defaultdict(int, vocab)
            # Add in counts from this class
            countdict.update(dir[1])
            numwords = dir[0]

            #***
            # Here turn the "countdict" dictionary of word counts into
            # into a dictionary of smoothed word probabilities
            #***
            probdict = defaultdict(float, vocab)
            length = len(countdict)
            for x in countdict:
                probdict[x] = float(float(countdict[x] + 1) / float(numwords + length))

            classes.append(probdict)
        self.__dict = classes

    def files2countdict(self, files):
        """Given an array of filenames, return a dictionary with keys
        being the space-separated, lower-cased words, and the values being
        the number of times that word occurred in the files."""
        numwords = 0
        d = defaultdict(int)
        numupper = 0
        numchar = 0
        caps = 0
        for file in files:
            for word in open(file).read().split():
                for x in word:
                    numchar = numchar + 1
                    if x.isupper():
                        numupper = numupper + 1
                if word.isupper():
                    caps = caps + 1
                word = word.lower()
                numwords = numwords + 1
                d[word] += 1
        return (numwords, d, numupper, numchar, caps)

    def predict(self, filename):
        '''Take in a filename, return whether this file is spam
        return value:
        True - filename is spam
        False - filename is not spam (is ham)'''
        spam = self.__dict[0]
        s_score = 0
        ham = self.__dict[1]
        h_score = 0
        #***
        # Here, compute the naive bayes score for a file for a given class by:
        # 1. Reading in each word, and converting it to lower case (see code below)
        # 2. Adding  the log probability of that word for that class
        #***
        spam_caps = float(float(self.spam[4])/float(self.spam[0]))
        ham_caps = float(float(self.ham[4])/float(self.ham[0]))
        spam_upper = float(float(self.spam[2])/float(self.spam[3]))
        ham_upper = float(float(self.ham[2])/float(self.ham[3]))
        for x in open(filename).read().split():
            for y in x:
                if y.isupper():
                    s_score = s_score + math.log(spam_upper)
                    h_score = h_score + math.log(ham_upper)
            if x.isupper():
                s_score = s_score + math.log(spam_caps)
                h_score = h_score + math.log(ham_caps)
            x = x.lower()
            s_score = s_score + math.log(spam.get(x,1))
            h_score = h_score + math.log(ham.get(x,1))
        
        if s_score > h_score:
            return True
        else:
            return False
