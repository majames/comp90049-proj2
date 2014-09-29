""" Program is used to construct the new stemmed, stop-worded and
    user-level feature vectors """

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



def main():
    """ Program entry point """
    if len(sys.argv) != 3:
        print('usage: fvector-constructor.py src-file destination-file')
    
    srcfilename = sys.argv[1]
    destfilename = sys.argv[2]

    d = parse_tweets(srcfilename)



if __name__ == '__main__':
    main()

