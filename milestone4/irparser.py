import os
import sys
import datafile 

def checkbranching(name) :
    if name in ['jump', 'call', 'goto', 'label:', 'ARRAY', 'jg', 'jl', 'jle', 'jge' ,'je', 'jne' ]:
        return True
    else:
        return False

def arraysim(name):
    if name in ['<-' , '->']:
        return True
    else:
        return False

def checkvariable(name):
    try:
        int(name)
        return False
    except:
        return True

if __name__ == "__main__" :
    filename = sys.argv[1]
    with open(filename) as f:
        data = f.readlines()
    index = 0
    flag = 0
    scopefunc = 0
    arglength = 8
    locallength = -4
    for line in data:
        index = index +1
        listvar = line.split(' ')
        print index, line , listvar
        node = [index]+[None]*5
        node[1:len(listvar)+1] = listvar
        node[len(listvar)] =  node[len(listvar)].replace('\n','')
        #print node
        if (not (checkbranching(node[1]) and arraysim(node[4]))):
            for i in range(1 , (len(listvar) + 1)):
                if(checkvariable(node[i])):
                    if(flag):
                        if node[i] not in datafile.memorymap[scopefunc].keys():
                            if node[i] == 'arg':
                                datafile.memorymap[scopefunc][node[i+1]] = str(arglength) + '(%ebp)'
                                # print datafile.memorymap[scopefunc][node[i+1]],"asdfg"
                                arglength = arglength + 4
                            elif (node[i] not in datafile.globalsection):
                                datafile.memorymap[scopefunc][node[i]] = str(locallength) + '(%ebp)'
                                locallength = locallength - 4
                    else:
                        datafile.globalsection.add(node[i])
                    datafile.allvariables.add(node[i])
        if node[1] == "ARRAY":
            datafile.setofarray[node[2]] = node[3]
        if node[1] == 'label:' and node[2][0:4] == "func":
            flag = 1
            scopefunc = node[2]
            datafile.memorymap[scopefunc] = {}
        if node[1] == 'ret':
            flag = 0
            datafile.numberofarguments[scopefunc] = (arglength-8)/4
            datafile.numberofvariables[scopefunc] = ((-1)*locallength - 4)/4
            scopefunc = 0
            arglength = 8
            locallength = -4
        if node[1] == 'cmp':
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],None))
            continue
        datafile.instruction.append(datafile.a3acinst(int(node[0]),node[3],node[4],node[5],node[2],node[1]))
    print datafile.allvariables, "all variables"
    print datafile.globalsection, 'globalsection'
    print datafile.instruction, 'instruction'
    print datafile.memorymap, 'memorymap'
    print datafile.numberofarguments, 'numberofarguments'
    print datafile.numberofvariables, 'numberofvariabels'        







