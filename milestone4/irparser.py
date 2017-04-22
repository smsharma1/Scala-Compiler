import os
import sys
import datafile 
import nasm

def checkbranching(name) :
    if name in ['jump', 'call', 'goto', 'label:', 'ARRAY', 'jg', 'jl', 'jle', 'jge' ,'je', 'jne', '->', '<-' ]:
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
        #IMP Have to handle nextstat properly
        listvar = line.replace('nextstat + 3','3').replace('nextstat + 2','2').split(' ')
        print index, line , listvar
        node = [index]+[None]*4
        node[1:len(listvar)+1] = listvar
        node[len(listvar)] =  node[len(listvar)].replace('\n','')
        #print node
        if not checkbranching(node[1]):
            for i in range(2 , (len(listvar) + 1)):
                if(checkvariable(node[i])):
                    if(flag):
                        if node[i] not in datafile.memorymap[scopefunc].keys():
                            if node[i] == 'arg':
                                datafile.memorymap[scopefunc][node[i+1]] = '['+str(arglength) + ' + ebp]'
                                # print datafile.memorymap[scopefunc][node[i+1]],"asdfg"
                                arglength = arglength + 4
                            elif (node[i] not in datafile.globalsection):
                                datafile.memorymap[scopefunc][node[i]] = '['+ str(locallength) + ' + ebp]'
                                locallength = locallength - 4
                                #TODO procedure under procedure 
                    else:
                        datafile.globalsection.add(node[i])
                    datafile.allvariables.add(node[i])
        if node[1] == "ARRAY":
            datafile.setofarray[node[2]] = node[3]
        if node[1] == 'label:' and node[2][0:4] == "func":
            flag = 1
            scopefunc = node[2]
            datafile.memorymap[scopefunc] = {}
        if node[1] == 'printstr' :
            datafile.setofString['str'+str(node[0])] = ' '.join(node[2:])
        if node[1] == 'ret':
            flag = 0
            datafile.numberofarguments[scopefunc] = arglength
            datafile.numberofvariables[scopefunc] = locallength
            scopefunc = 0
            arglength = 8
            locallength = -4
        if node[1] == 'cmp':
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],None))
            continue
        if node[3] == '`':
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],None,'Unary',node[4]))
            continue
        if node[1] in ['je','jne','jg','jge','jl','jle','goto','pusharg','call','label:','print','printstr','read']:
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],node[2]))
            continue
        datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],node[4]))

    nasm.asm()
    # print datafile.allvariables, "all variables"
    # print datafile.globalsection, 'globalsection'
    # for inst in datafile.instruction:
    #     print inst.instnumber,inst.type,inst.op1,inst.op2,inst.operator, inst.out 
    print datafile.memorymap, 'memorymap'
    # print datafile.numberofarguments, 'numberofarguments'
    # print datafile.numberofvariables, 'numberofvariabels'        







