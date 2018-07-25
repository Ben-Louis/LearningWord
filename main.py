#! /Users/lupeng/miniconda3/bin/python

import os
import sys
import json
import argparse
import random
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
    parser.add_argument('--update', type=str, default='')

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

    if len(config.update) > 0:
        update(config.update)


def add(word, data):
    if word in data.keys():
        print('This word is already in the pool')
        return 

    word_dict = {'word': word, 'exps':[], 'test':[0,0]}
    i = 1
    while True:
        print('=== Explain %d ==='%i)
        tp = input('type: ')
        expl = input('explain: ')
        emp = input('example: ')
        word_dict['exps'].append([tp, expl, emp])

        nxt=input('next?[Y/N]').lower()
        while not (nxt in ('', 'y', 'n', 'q')):
            # extra question
            if nex == 'q':
                que = input('Question: ')
                ans = input('Answer: ')
                word_dict['question'] = [que, ans]

            nxt=input('next?[Y/N]').lower()
        if nxt.lower() in ['','n']:
            break

        i += 1

    data[word] = word_dict
    dump(word_dict)


def dump(word_dict, show=True):
    fname = os.path.join(LOCAL, 'data', word_dict['word']+'.json')
    with open(fname, 'w') as f:
        json.dump(word_dict, f)
    if show:
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

    num = min(num, len(data))
    print('Reviewing %d words...'%num, end='\n\n')

    keys = list(data.keys())
    random.shuffle(keys)

    for key in keys[:num]:
        word_dict = data[key]

        print(word_dict['word'])
        for i,exp in enumerate(word_dict['exps']):
            print(str(i+1)+' | ', end='')
            print(exp[0],'. ',exp[1],'; ',exp[2])

        input()



def test(num, data):

    # prepare test data
    hard, med, easy = [], [], []

    for word, word_dict in data.items():
        r, w = word_dict['test']
        if r+w == 0 or r/(w+1) < 0.8:
            hard.append(word_dict)
        elif r/(w+1) > 1.5:
            easy.append(word_dict)
        else:
            med.append(word_dict)

    ne = min(int(num*0.05), len(easy))
    nm = min(int(num*0.2), len(med))
    nh = num - nm - ne

    hard.sort(key=lambda x:x['test'][0])
    med.sort(key=lambda x:x['test'][0])
    easy.sort(key=lambda x:x['test'][0])
    
    test_words = []
    #test_words += choice(hard, size=nh)
    #test_words += choice(med, size=nm)
    #test_words += choice(easy, size=ne)
    test_words += choice(hard[:nh*3], size=nh)
    test_words += choice(med[:nm*2], size=nm)
    test_words += choice(easy[:ne*2], size=ne)

    # test 
    random.shuffle(test_words)
    for word_dict in test_words:

        # test process
        print()
        print(word_dict['word']+'  (%d/%d)'%(word_dict['test'][0], word_dict['test'][1]))
        known = input('known?[Y/N]').lower()
        while not (known in ['y', 'n']):
            known = input('known?[Y/N]').lower()

        if known == 'y':

            queans = word_dict.get('question', None) 
            if queans:
                q, a = queans
                print('Question: ',q)
                ans = input('Answer: ')

                if ans != a:
                    known = 'n'

        if known == 'y':
            word_dict['test'][0] += 1
            dump(word_dict, False)  

        if known == 'n':
            for i,exp in enumerate(word_dict['exps']):
                print(str(i+1)+' | ', end='')
                print(exp[0],'. ',exp[1],'; ',exp[2])  
            print(word_dict.get('question',None)) 
            word_dict['test'][1] += 1
            dump(word_dict, False)

    print()

def choice(seq, size=1):
    idxs = list(range(len(seq)))
    random.shuffle(idxs)
    res = []
    for i in range(size):
        res.append(seq[idxs[i]])
    return res


def update(commit):
    os.chdir(LOCAL)
    os.system('git add main.py')
    os.system('git add data')
    os.system('git commit -m %s'%commit)
    os.system('git push origin master')




if __name__ == '__main__':
    main()

