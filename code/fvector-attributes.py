#!/usr/bin/python

""" Program is used to construct the new normalised, stemmed, 
    and stop-worded feature vector attributes """

import re
import sys
from nltk.corpus import stopwords
from nltk.stem.porter import *

def read_attributes(filename):
    """ Read in a list of attributes from file """
    f = open(filename, 'rU')
    attributes = f.readlines()
    f.close()

    attributes = [re.sub(r'\n', '', attribute) for attribute in attributes]

    return attributes

def read_dictionary_file(filename):
    """ Reads a file mapping Twitter slang to a normalised word """
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    d = {}
    for line in lines:
        words = line.split('\t')

        if d.get(words[0]):
            print('Error: OOV word should not map to multiple ' 
                  'different entries!')
            sys.exit()
        else:
            d[words[0]] = re.sub(r'\n', '', words[1])

    return d

def modify_attributes(attributes, normal_dict):
    """ Returns a list of attributes that have been normalised,
        stemmed and have the stop-words removed """

    stop = stopwords.words('english')

    # intialise the Porter Stemmer
    stemmer = PorterStemmer()
    
    mattributes = []
    for attribute in attributes:
        # normalise the words using the Unimelb ESMN
        if attribute in normal_dict:
            mattribute = normal_dict[attribute]
        else:
            mattribute = attribute

        # stem the tweet words
        mattribute = stemmer.stem(mattribute)

        # remove words that are 1 characters or less
        if len(mattribute) == 1 or mattribute in stop:
            mattribute = None

        if mattribute:
            mattributes.append(mattribute + '\n')

    return mattributes

def write_new_attributes_to_file(filename, attributes):
    """ Writes the new vector attributes to file """
    f = open(filename, 'w')
    f.writelines(attributes)
    f.close()


def main():
    """ Entry point int program """
    if len(sys.argv) != 4:
        print('usage: fvector-attributes.py dict-file ' 
              'src-file destination-file')
        sys.exit()

    dict_filename = sys.argv[1]
    src_filename = sys.argv[2]
    dest_filename = sys.argv[3]

    # read in the normalisastion dictionary and the vevctor attributes
    # to be modified
    normal_dict = read_dictionary_file(dict_filename)
    attributes = read_attributes(src_filename)

    # normalise, stem and stop-word the attributes
    attributes = modify_attributes(attributes, normal_dict)

    # write the attributes to file
    write_new_attributes_to_file(dest_filename, attributes)


if __name__ == '__main__':
    main()
