#!/usr/bin/env python

import sys
import os
import glob
import pickle

if __name__ == '__main__':
    spam = 0
    ham = 0
    if len(sys.argv) < 3:
        print 'Usage:', sys.argv[0], 'pickleFile, testFileOrFolder'
    else:
        if os.path.isfile(sys.argv[1]):
            # load pickle
            predictor = pickle.load(open(sys.argv[1], 'r'))
            if os.path.isdir(sys.argv[2]):
                # predict all files in folder
                for f in glob.glob(sys.argv[2]+'/*'):
                    prediction = predictor.predict(f)
                    print f, 'is', prediction
                    if prediction:
                        spam = spam + 1
                    else:
                        ham = ham + 1
                print("spam:", str(spam))
                print("ham:", str(ham))
            elif os.path.isfile(sys.argv[2]):
                # predict this file
                print sys.argv[2], 'is', predictor.predict(sys.argv[2])
            else:
                print 'test file illegal'
        else:
            print 'pickle file illegal'
