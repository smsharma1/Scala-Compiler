import os
import sys

def check_branching(name) :
    if name in ['jump', 'call', 'goto', 'label']:
        return True
    else:
        return False


if __name__ == "__main__" :
    filename = sys.argv[1]
    with open(filename) as f:
        data = f.readlines()
    index = 0
    for line in data:
        index = index +1
        listvar = line.split(' ')
        # print index, line , listvar
        node = [index]+[None]*4
        node[1:len(listvar)+1] = listvar
        node[len(listvar)] =  node[len(listvar)].replace('\n','')
        print node
        if (not check_branching[node[1]]):

