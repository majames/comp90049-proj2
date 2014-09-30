#!/usr/bin/python
""" Program is used to construct the new normalised, stemmed, 
    stop-worded and user-level feature vectors """

import sys


def parse_tweets(filename):
    """ Used to extract a list of tweets from the modified tweet files
        or the ideal tweet-location pairs. Returns a dictionary,
        key: user-id
        value: tweet contents """
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    # remove the new line character from the end of the tweet text
    lines = [re.sub(r'\n', '', line) for line in lines]    
    lines = [line.split('\t') for line in lines]

    d = {}
    for line in lines:
        if d.get(line[0]):
            d[line[0]] = d.get(line[0]) + ' ' + line[2]
        else:
            # first entry for this Twitter user
            d[line[0]] = line[2]

    return d

def parse_attributes(filename):
    """ Get the attributes of the feature vectors """
    f = open(filename, 'rU')
    attributes = f.readlines()
    f.close()

    return attributes


def construct_vector_instance(tweet_dict, attributes):
    """ Make the feature vectors, given a dictionary of Tweet 
        usernumber - content and list of attributes """

    # vector dict: key - user id integer, value - string .csv
    vectors_dict = {}
    for entry in tweet_dict.items():
        if d.get(entry[0]):
            print('Error: Twitter user ids should be unique!')
            sys.exit()
        else:
            vectors_dict[entry[0]] = make_vector(entry[1], attributes)

    return vectors_dict



def make_vector(tweet_text, attributes):
    """ Make a feature vector corresponding to a User """
    # intialise the feature vector
    vector_dict = {}
    for attribute in attributes:
        vector_dict[attribute] = 0

    tweet_words = tweet_text.split(' ')
    for word in tweet_words:
        if word in vector_dict:
            vector_dict[word] += 1

    return vector_dict.values().join(',')


def write_vectors_to_file(dest_filename, vectors_dict):
    """ Write the dictionary of feature vectors to .csv 
        and .arff file """

    # write the .csv file
    csv_filename = dest_filename + '.csv'
    f = open(csv_filename, 'w')
    for entry in vectors_dict.items():
        f.write(entry[0] + ',' + entry[1] + '\n')
    f.close()

    #TODO write the .arff file and include the class in the end


def main():
    """ Program entry point """
    if len(sys.argv) != 3:
        print('usage: fvector-constructor.py src-file attr-file ' 
              'destination-file')
    
    src_filename = sys.argv[1]
    attr_filename = sys.argv[2]
    dest_filename = sys.argv[3]

    # get the tweet instances
    tweet_dict = parse_tweets(src_filename)

    # get the feature vector attributes
    attributes = parse_attributes(attr_filename)

    vectors_dict = construct_vector_instance(tweet_dict, attributes)

    write_vectors_to_file(dest_filename, vectors_dict)



if __name__ == '__main__':
    main()

