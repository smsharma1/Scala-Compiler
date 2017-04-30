import os
import sys
import datafile 
import nasm
import symboltable
import pickle

def checkbranching(name) :
    if name in ['jump','print','append', 'call', 'goto', 'label:', 'jg', 'jl', 'jle', 'jge' ,'je', 'jne','ret','ret1','ret2','printstr','pusharg2','pushaddr', 'fopen', 'fwrite', 'fread', 'fclose', 'deletetail']:
        return True
    else:
        return False
def default(name1,name2):
    if name1 == "pusharg" and name2 == "DEFAULT":
        return False
    else:
        return True

def Size(type1):
    if type1=="INT":
        return 4
    elif type1=="CHAR":
        return 2
    elif type1=="BYTE":
        return 1
    elif type1=="SHORT":
        return 2
    elif type1=="LONG":
        return 8
    elif type1=="FLOAT":
        return 4
    elif type1=="DOUBLE":
        return 8
    elif type1=="POINTER":
        return 4
    elif type1=="BOOL":
        return 4
    elif "ARRAY" in type1:
        return Size(type1.replace("ARRAY", ''))
    elif "LIST" in type1:
        return Size(type1.replace("LIST@", ''))
    else:
        return 10

def checkvariable(name):
    try:
        int(name)
        return False
    except:
        try:
            float(name)
            return False
        except:
            if name == "DEFAULT":
                return False
            else:
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
    symbolTable = pickle.load(open("rootScope.p", "rb"))
    mainScope = symbolTable.singletonObject.functions['main'][0]
    currentScope = mainScope
    for line in data:
        index = index +1
        listvar = line.split(' ')
        node = [index]+[None]*4
        node[1:len(listvar)+1] = listvar
        node[len(listvar)] =  node[len(listvar)].replace('\n','')
        if not checkbranching(node[1]):
            for i in range(2 , (len(listvar) + 1)):
                if(checkvariable(node[i]) and default(node[1],node[2]) ):
                    if(flag):
                        if node[i] not in datafile.memorymap[scopefunc].keys():
                            if node[1] == 'arg':
                                datafile.memorymap[scopefunc][node[2]] = '['+str(arglength) + ' + ebp]'
                                try:
                                    node[3]
                                    datafile.meta[node[2]] = node[3] 
                                except:
                                    pass
                                arglength = arglength + Size(currentScope.LookUpVarSize(node[2])[1])
                            elif (node[i] not in datafile.globalsection and  node[i] not in datafile.setofList and node[i] not in datafile.setofarray and node[i] not in datafile.setofString):
                                datafile.memorymap[scopefunc][node[i]] = '['+ str(locallength) + ' + ebp]'
                                if node[1] == "ARRAY":
                                    if node[4] != None:
                                        locallength = locallength - Size(currentScope.LookUpVarSize(node[2])[1])*int(node[3])*int(node[4])
                                    else:
                                        locallength = locallength - Size(currentScope.LookUpVarSize(node[2])[1])*int(node[3])
                                elif node[1] == "LIST":
                                    if node[3] != None:
                                        datafile.Listoffset[node[2]]  = {}
                                        for m in range(0,int(node[3])):
                                            datafile.Listoffset[node[2]][str(m)] = 0     
                                    else:    
                                        locallength = locallength - Size(currentScope.LookUpVarSize(node[2])[1])*int(currentScope.listdict[node[2]])
                                        datafile.Listoffset[node[2]]  = 0
                                else:
                                    print node[i], "77777777777777777777777777777777777",currentScope.LookUpVarSize(node[i]),'88888888888888888888'
                                    locallength = locallength - Size(currentScope.LookUpVarSize(node[i])[1])
                    else:
                        if node[1] == "ARRAY":
                            try:
                                node[4]
                                size = Size(currentScope.LookUpVarSize(node[2])[1])*int(node[3])*int(node[4])
                                datafile.setofarray[node[i]] = size
                            except:
                                size = Size(currentScope.LookUpVarSize(node[2])[1])*int(node[3])
                                datafile.setofarray[node[i]] = size
                        elif node[1] == "LIST":
                            if node[3] != None:
                                size = Size(currentScope.LookUpVarSize(node[2])[1])
                                scope = currentScope.LookUpListScope(node[2])
                                datafile.Listoffset[node[2]]  = {}
                                datafile.setofList[node[i]] = {}
                                for m in range(0,int(node[3])):
                                    datafile.Listoffset[node[2]][str(m)] = 0
                                    if m == 0:
                                        datafile.setofList[node[i]][str(m)] = size * int(scope.listdict[node[2]][str(m)])
                                    else:    
                                        datafile.setofList[node[i]][str(m)] = size * int(scope.listdict[node[2]][str(m)]) + datafile.setofList[node[i]][str(m-1)] 
                            else:                                
                                size = Size(currentScope.LookUpVarSize(node[2])[1])
                                scope = currentScope.LookUpListScope(node[2])
                                datafile.Listoffset[node[2]]  = 0
                                datafile.setofList[node[i]] = size * int(scope.listdict[node[2]])
                        else:
                            datafile.globalsection.add(node[i])
                    datafile.allvariables.add(node[i])
        if node[1] == 'label:' and node[2][0:4] == "func":
            flag = 1
            scopefunc = node[2]
            newScope = currentScope.parent.functions[node[2][7:]][0]
            newScope.returnScope = currentScope
            currentScope = newScope
            datafile.memorymap[scopefunc] = {}
        if (node[1] == 'printstr') :
            for i in range(0,5):
                if node[i]:
                    pass
                else:
                    node[i] = ''
            datafile.setofString['str'+str(node[0])] = ' '.join(node[2:]).strip()
        if node[1] == 'ret':
            flag = 0
            datafile.numberofarguments[scopefunc] = -arglength
            datafile.numberofvariables[scopefunc] = -locallength
            scopefunc = 0
            arglength = 8
            locallength = -4
            currentScope = currentScope.returnScope
        if node[1] == 'cmp':
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],None))
            continue
        if node[3] == '`':
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],None,'Unary',node[4]))
            continue
        if node[1] in ['je','jne','jg','jge','jl','jle','goto','pusharg','pusharg2','pushaddr','call','label:','print','printstr','read','ret', 'get', 'ret1', 'ret2']:
            if node[1] == 'pusharg2':
                for i in range(0,5):
                    if node[i]:
                        pass
                    else:
                        node[i] = ''
                datafile.setofString['str'+str(node[0])] = ' '.join(node[2:]).strip()
            datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],node[2]))
            continue
        datafile.instruction.append(datafile.a3acinst(int(node[0]),node[2],node[1],node[3],node[1],node[4]))

    nasm.asm()

    # Useful Debug information that can be printed
    # print datafile.allvariables, "all variables"
    # print datafile.globalsection, 'globalsection'
    # print datafile.setofarray, 'setofarray'
    
    # for inst in datafile.instruction:
    #     print inst.instnumber,inst.type,inst.op1,inst.op2,inst.operator, inst.out 
    # print datafile.memorymap, 'memorymap'
    # print datafile.numberofarguments, 'numberofarguments'
    # print datafile.numberofvariables, 'numberofvariabels'        







