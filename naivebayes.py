#!/usr/bin/env python

# Modified from code by Andrew McCallum of UMass Amherst

# Your job is to replace the two sections marked below with code and
# run the classifier on test files.

import math
import sys
import glob
import pickle
from collections import defaultdict

# In the documentation and variable names below "class" is the same
# as "category"

def naivebayes (dirs):
    """Train and return a naive Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class"""
    # Set up the vocabulary for all files in the training set
    vocab = defaultdict(int)
    for dir in dirs:
        temp = files2countdict(glob.glob(dir+"/*"))
        vocab.update(temp[1])
    # Set all counts to 0
    vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))
    
    classes = []
    for dir in dirs:
        print dir
        # Initialize to zero counts
        countdict = defaultdict(int, vocab)
        # Add in counts from this class
        f2cd = files2countdict(glob.glob(dir+"/*"))
        countdict.update(f2cd[1])
        numwords = f2cd[0]

        #***
        # Here turn the "countdict" dictionary of word counts into
        # into a dictionary of smoothed word probabilities
        #***
        probdict = defaultdict(float, vocab)
        length = len(countdict)
        for x in countdict:
            probdict[x] = float(float(countdict[x] + 1) / float(numwords + length))

        classes.append((dir,probdict))
    return classes

def classify (classes, filename):
    """Given a trained naive Bayes classifier returned by naivebayes(), and
    the filename of a test document, d, return an array of tuples, each
    containing a class label; the array is sorted by log-probability 
    of the class, log p(c|d)"""
    answers = []
    print 'Classifying', filename
    for c in classes:
        score = 0
        #***
        # Here, compute the naive bayes score for a file for a given class by:
        # 1. Reading in each word, and converting it to lower case (see code below)
        # 2. Adding  the log probability of that word for that class
        #***
        for x in open(filename).read().split():
            x = x.lower()
            score = score + math.log(c[1].get(x,1))
        answers.append((score,c[0]))
    answers.sort()
    return answers[1][1].split('/')[1]

def files2countdict (files):
    """Given an array of filenames, return a dictionary with keys
    being the space-separated, lower-cased words, and the values being
    the number of times that word occurred in the files."""
    numwords = 0
    d = defaultdict(int)
    for file in files:
        for word in open(file).read().split():
            numwords = numwords + 1
            d[word.lower()] += 1
    return (numwords, d)
    

if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [testfile...]"
    dirs = sys.argv[1:3]
    testfiles = sys.argv[3:]
    nb = naivebayes (dirs)
    answers = []
    for x in testfiles:
        answers.append((x, classify(nb, x)))
    print(answers)
    spam = 0
    ham = 0
    for x in answers:
        if x[1] == "ham":
            ham = ham + 1
        else:
            spam = spam + 1
    print("ham: " + str(ham))
    print("spam: " + str(spam))
    pickle.dump(nb, open("classifier.pickle",'w'))
