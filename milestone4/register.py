import datafile

def initializeblock():
    datafile.blockout = []
    datafile.registerdescriptor.clear()
    for x in datafile.registerlist:
        datafile.registerdescriptor[x] = None #initially register contains nothing

    datafile.addressdescriptor.clear()

    for x in datafile.allvariables:
        datafile.addressdescriptor[x] = None #initially nothing is in register

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

def getz(z):
    if z in datafile.allvariables :
        if datafile.addressdescriptor[z] != None:   #check if it is in register or not 
            datafile.zprime = datafile.addressdescriptor[z]
        else:
            datafile.zprime = z

def getreg(l, y, ino, special = None):
    if special != None : #special is when operation requires an additional register 
        datafile.L = special
    elif y in datafile.allvariables and datafile.addressdescriptor[y] != None and datafile.symtable[ino][y] == 1000000007:
        datafile.L = datafile.addressdescriptor[y]  #Y is in register and it is dead at this instruction give l = y
        return
    elif datafile.addressdescriptor[l] != None:
        datafile.L = datafile.addressdescriptor[l] #if already posses register give it 
        return

    if datafile.L == None:
        for k in datafile.registerlist:
            if datafile.registerdescriptor[k] == None: #give it empty register
                datafile.L = k

    if datafile.L == None :
        if(datafile.symtable[ino][l] != 1000000007 or (datafile.zprime not in datafile.registerlist)):
           nextuse = -1
           for k in datafile.registerlist:
               if k == datafile.zprime :
                   continue
               if nextuse <= datafile.symtable[ino][datafile.registerdescriptor[k]]:  #we have to free the register its important 
                   datafile.L = k
                   nextuse = datafile.symtable[ino][datafile.registerdescriptor[k]]
        else:
            datafile.L = l
    if datafile.L in datafile.registerlist and datafile.registerdescriptor[datafile.L] != None:
        storereg(datafile.L)

#this function free the register
def storereg(regno):
    if datafile.registerdescriptor[regno] != None and datafile.registerdescriptor[regno][0] == '[':
        datafile.blockout.append("mov {}, {}".format(mem(datafile.registerdescriptor[regno]), regno))
        datafile.lineno = datafile.lineno + 1
        datafile.addressdescriptor[datafile.registerdescriptor[regno]] = None
        datafile.registerdescriptor[regno] = None

#this function is used to find memory 
def mem(var):
    try :
        int(var)
        return str(var)
    except :
        # print datafile.registerlist, "this is registerlistin mem"
        if var in datafile.registerlist:
            return var
        else:
            if datafile.currentscope != "" and var in datafile.memorymap[datafile.currentscope].keys():
                return datafile.memorymap[datafile.currentscope][var]
            for k in datafile.memorymap.keys() :
                if var in datafile.memorymap[k].keys() :
                    return datafile.memorymap[k][var]
            else :
                return str(var)

#This function is for Yprime 
def gety(var):
    # print var , "in gety"
    if var in datafile.allvariables:
        if datafile.addressdescriptor[var] != None:
            datafile.yprime = datafile.addressdescriptor[var]
        else:
            datafile.yprime = var
    if datafile.yprime != datafile.L :
        datafile.blockout.append("mov " + mem(datafile.L) + ", " + mem(datafile.yprime))

#Update the addressdescriptor after operation is done
def UpdateAddressDescriptor(x):
    if datafile.L in datafile.registerlist:
        datafile.addressdescriptor[x] = datafile.L
        datafile.registerdescriptor[datafile.L] = x
    else:
        datafile.addressdescriptor[x] = None
    for v in datafile.allvariables :
        if datafile.addressdescriptor[v] == datafile.L and v != x:
            datafile.addressdescriptor[v] = None
    for k in datafile.registerlist:
        if datafile.L != k and datafile.registerdescriptor[k] == x:
            datafile.registerdescriptor[k] = None

#Free the register
def freereg(var, ino):
    if var in datafile.allvariables :
        if datafile.symtable[ino][var] == 1000000007 and datafile.addressdescriptor[var] != None:
            datafile.registerdescriptor[datafile.addressdescriptor[var]] = None
            datafile.addressdescriptor[var] = None

#Find the appropriate register and return it
def emptyregister(var,left=[]):
    for reg in datafile.registerlist:
        if datafile.registerdescriptor[reg] == None and reg not in left:
            return reg
    nextuse = -1
    for k in datafile.registerlist:
        if k in left:
            continue
        try:
            int(datafile.registerdescriptor[k])
            continue
        except:
            # print var, k ,datafile.registerdescriptor[k],datafile.symtable, "checking in emptyregister"
            if nextuse <= datafile.symtable[var][datafile.registerdescriptor[k]]:  #we have to free the register its important 
                reg = k
                nextuse = datafile.symtable[var][datafile.registerdescriptor[k]]
    storereg(reg)    
    return reg

#before block ends save all the register
def save():
    for reg in datafile.registerlist:
        storereg(reg)
