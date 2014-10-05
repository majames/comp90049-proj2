#!/usr/bin/python
""" Program is used to balance the training and developement 
    files """

import numpy as np
import sys
import re

def read_csv(filename):
    """ Read in the .csv file vectors """
    filename = filename + '.csv'

    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    return lines

def read_arff(filename):
    """ Read in the .arff file """
    filename = filename + '.arff'

    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    return lines

def write_arff(filename, lines):
    """ Write the .arff file """
    filename = filename + '.arff'

    f = open(filename, 'w')
    f.writelines(lines)
    f.close()


def write_csv(filename, lines):
    """ Write lines to .csv file """
    filename = filename + '.csv'

    f = open(filename, 'w')
    f.writelines(lines)
    f.close()

def balance_arff(train_filename, dev_filename, vectors):
    """ Used to balance the .arff training and development files """
    old_train_lines = read_arff(train_filename)

    i = 0
    for i in range(len(old_train_lines)):
        if re.match(r'\d+', old_train_lines[i]):
            break

    header = old_train_lines[0:i]

    new_train_lines = header + vectors[0]
    new_dev_lines = header + vectors[1]

    write_arff(train_filename, new_train_lines)
    write_arff(dev_filename, new_dev_lines)


def balance_csv(train_filename, dev_filename):
    """ Used to balance the .csv file """

    train_lines = read_csv(train_filename)
    dev_lines = read_csv(dev_filename)

    # 80% training data, 20% dev data
    a = np.array([[1, 1], [1, -4]])
    b = np.array([len(train_lines) + len(dev_lines), 0])

    x = np.linalg.solve(a, b)

    # the number of lines to move from the dev file to the train file
    lines_to_move = int(round(len(dev_lines) - x[1], 0))

    # move the lines across
    if lines_to_move > 0:
        for i in range(lines_to_move):
            line = dev_lines.pop()
            train_lines.append(line)
    else:
        for i in range(abs(lines_to_move)):
            line = train_lines.pop()
            dev_lines.append(line)

    write_csv(train_filename, train_lines)
    write_csv(dev_filename, dev_lines)

    return (train_lines, dev_lines)



def main():
    """ Program entry point """
    if len(sys.argv) != 3:
        print('usage: fvector-balancer.py train-file dev-file ')
        sys.exit()

    train_filename = sys.argv[1]
    dev_filename = sys.argv[2]    

    vectors = balance_csv(train_filename, dev_filename)
    balance_arff(train_filename, dev_filename, vectors)




if __name__ == '__main__':
    main()

