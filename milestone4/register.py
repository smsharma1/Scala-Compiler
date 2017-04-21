import datafile

def initializeblock():
    datafile.registerdescriptor.clear()
    for x in datafile.registerlist:
        datafile.registerdescriptor[x] = None #initially register contains nothing

    datafile.addressdescriptor.clear()

    for x in datafile.allvariables:
        datafile.addressdescriptor[x] = None #initially nothing is in register

        #done up to this point 
    datafile.symtable = []
    for x in range(0, datafile.blocknuminst-1):
        datafile.symtable.append({})
        for y in datafile.allvariables :
            datafile.symtable[x][y] = 1000000007
    datafile.symtable.append({})
    for y in datafile.allvariables:
        datafile.symtable[datafile.blocknuminst-1][y] = datafile.blocknuminst-1


    #scan from backwards to set the live ranges assuming all variables to be dead on exit
    i = datafile.blocknuminst - 1
    while(i > 0):
        (x, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
        for k in datafile.allvariables:
            if k == y or k == z :
                datafile.symtable[i - 1][k] = i
            elif k != x:
                datafile.symtable[i - 1][k] = datafile.symtable[i][k]
        i = i - 1
