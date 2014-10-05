#!/usr/bin/python
""" Program is used to construct the new normalised, stemmed, 
    stop-worded and user-level feature vectors """

import re
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

    attributes = [re.sub(r'\n', '', attribute) for attribute in attributes] 

    # ignore the first user-id attribute
    return [attr for attr in attributes if attr != 'id']

def parse_classes(filename):
    """ Get the location of each user """
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    # remove the new line character from the end of the tweet text
    lines = [re.sub(r'\n', '', line) for line in lines]  
    lines = [line.split('\t') for line in lines]

    class_dict = {}
    for line in lines:
        if class_dict.get(line[0]) \
           and class_dict[line[0]] != normalise_class_string(line[1]) \
           and not class_dict[line[0]]:
            print('Error: duplicate user ids in class file')
            print(line[0], normalise_class_string(line[1]), class_dict[line[0]])
            sys.exit()
        elif normalise_class_string(line[1]):
            class_dict[line[0]] = normalise_class_string(line[1])

    return class_dict

def normalise_class_string(class_name):
    """ Given a class name it is normalised """
    if 'San Francisco' in class_name:
        return 'SF'
    elif 'Chicago' in class_name:
        return 'C'
    elif 'New York' in class_name:
        return 'NY'
    elif 'Atlanta' in class_name:
        return 'At'
    elif 'Los Angeles' in class_name:
        return 'LA'
    else:
        return None

def construct_vector_instance(tweet_dict, attributes, class_dict):
    """ Make the feature vectors, given a dictionary of Tweet 
        usernumber - content and list of attributes """

    # vector dict: key - user id integer, value - string .csv
    vectors_dict = {}
    for entry in tweet_dict.items():
        if vectors_dict.get(entry[0]):
            print('Error: Twitter user ids should be unique!')
            sys.exit()
        elif not class_dict.get(entry[0]):
            print('Error: Twitter user id not found in class dictionary')
            sys.exit()
        else:
            vectors_dict[entry[0]] = make_vector(entry[1], attributes) + \
                                     ',' + str(class_dict[entry[0]])

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

    vector_values = [str(value) for value in vector_dict.values()]

    return ','.join(vector_values)


def write_vectors_to_file(dest_filename, vectors_dict, attributes):
    """ Write the dictionary of feature vectors to .csv 
        and .arff file """

    # write the .csv file
    csv_filename = dest_filename + '.csv'
    f = open(csv_filename, 'w')
    for entry in vectors_dict.items():
        f.write(entry[0] + ',' + entry[1] + '\n')
    f.close()

    # write the .arff file
    arff_filename = dest_filename + '.arff'
    f = open(arff_filename, 'w')

    # write the .arff file header 
    f.write('@RELATION twitter-loc-reduced\n')
    f.write('@ATTRIBUTE id NUMERIC\n')
    for attr in attributes:
        f.write('@ATTRIBUTE ' + attr + ' NUMERIC\n')
    f.write('@ATTRIBUTE location {LA,NY,C,At,SF}\n')

    instance = vectors_dict.values()[0]
    print('length of attributes: ' + str(len(attributes)))
    print('length of instance vector: ' + str(len(instance.split(','))))

    # write the instances of vectors to file
    f.write('@DATA\n')
    for entry in vectors_dict.items():
        f.write(entry[0] + ',' + entry[1] + '\n')

    f.close()


def main():
    """ Program entry point """
    if len(sys.argv) != 5:
        print('usage: fvector-instances.py tweet-file attr-file ' 
              'class-file destination-file')
        sys.exit()
    
    tweet_filename = sys.argv[1]
    attr_filename = sys.argv[2]
    class_filename = sys.argv[3]
    dest_filename = sys.argv[4]

    # get the tweet instances
    tweet_dict = parse_tweets(tweet_filename)

    # get the feature vector attributes
    attributes = parse_attributes(attr_filename)

    # get a dictionary of the classes
    class_dict = parse_classes(class_filename)

    # get the new feature vectors
    vectors_dict = construct_vector_instance(tweet_dict, attributes, class_dict)

    write_vectors_to_file(dest_filename, vectors_dict, attributes)



if __name__ == '__main__':
    main()

