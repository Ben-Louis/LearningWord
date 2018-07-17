#! /Users/lupeng/miniconda3/bin/python

import os
import sys
import json
import argparse
LOCAL = os.path.abspath(__file__).rsplit(os.sep,1)[0]

def str2bool(s):
    return s.lower() == 'true'

# get parameters
def get_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', type=str, default='')
    parser.add_argument('--readd', type=str, default='')
    parser.add_argument('--review', type=int, default=-1)
    parser.add_argument('--test', type=int, default=-1)

    config = parser.parse_args()
    return config

def main():
    config = get_parameter()

    data = load_data()

    if config.add:
        add(config.add, data)

    if config.readd:
        remove(config.readd, data)
        add(config.readd, data)

    if config.review > 0:
        review(config.review, data)

    if config.test > 0:
        test(config.test, data)

def add(word, data):
    if word in data.keys():
        print('This word in already in the pool')
        return 

    word_dict = {'word': word, 'exps':[]}
    i = 1
    while True:
        print('=== Explain %d ==='%i)
        tp = input('type: ')
        expl = input('explain: ')
        emp = input('example: ')
        word_dict['exps'].append([tp, expl, emp])

        nxt=input('next?[Y/N]').lower()
        while nxt in ('y', 'n'):
            mode = 'continue'
            if nxt.lower() == 'n':
                mode = 'break'
                break
            nxt=input('next?[Y/N]').lower()

        if mode == 'break':
            break
        i += 1

    data[word] = word_dict
    dump(word_dict)


def dump(word_dict):
    fname = os.path.join(LOCAL, 'data', word_dict['word']+'.json')
    with open(fname, 'w') as f:
        json.dump(word_dict, f)
    print('Save \'%s\' successfully!'%word_dict['word'])

def load_data():
    words = os.listdir(os.path.join(LOCAL, 'data'))
    data = {}
    for w in words:
        if w[0] == '.':
            continue
        with open(os.path.join(LOCAL, 'data', w), 'r') as f:
            word_dict = json.load(f)
        data[word_dict['word']] = word_dict
    return data

def remove(word, data):
    os.remove(os.path.join(LOCAL, 'data', word+'.json'))
    del data[word]
    print('Remove \'%s\' successfully!'%word)

def review(num, data):
    raise NotImplementedError

def test(num, data):
    raise NotImplementedError


if __name__ == '__main__':
    main()

