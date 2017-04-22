import datafile
import register
asmcode = []

#soure of instruction is tutorials point
f = open('asmfile','w') 

def blockasmgenerate():
    datafile.blocknuminst = len(datafile.block)
    register.initializeblock()
    for i in range(0,len(datafile.block) - 1):
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)
    i = len(datafile.block) - 1
    if i == -1:
        return 
    if datafile.block[i].type in ['jg', 'jge', 'je', 'jle', 'jne', 'jl', 'goto', 'jump', 'call', 'ret']:
        register.save()
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)
    else:
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)
        register.save()
    for b in datafile.blockout:
        # print(b)
        f.write(b + '\n')


def asm():
    print(".section .data")
    f.write(".section .data\n")
    for data in datafile.globalsection:
        print("{}:".format(data))
        f.write("{}:\n".format(data))
        print("\t.long {}".format(1))
        f.write("\t.long {}\n".format(1))
    for data in datafile.setofarray.keys():
        print("{}:".format(data))
        f.write("{}:\n".format(data))
        print("\t.zero {}".format(4*int(datafile.setofarray[data])))
        f.write("\t.zero {}\n".format(4*int(datafile.setofarray[data])))
    print("\n.section .text\n")
    f.write("\n.section .text\n\n")
    print('.global main\n\n')
    f.write('.global main\n\n')
    print('main:')
    f.write('main:\n')
    blockbreaker = set()
    blockbreaker.add(0)   #starting of first block
    for i in range(0,len(datafile.instruction)):
        if datafile.instruction[i].type == 'label:':
            blockbreaker.add(i)   #any target of a goto statement is a leader
        elif datafile.instruction[i].type in ['jg', 'je', 'jle', 'jge', 'je', 'jne', 'ret', 'goto', 'call' ]:
            blockbreaker.add(i+1) #any statement that follows a goto statement is a leader
    blockbreaker.add(len(datafile.instruction))
    blockbreaker = sorted(blockbreaker)
    # print blockbreaker, "blockbreaker"
    for i in range (0,len(blockbreaker)-1):
        if i == 0:
            datafile.block = datafile.instruction[blockbreaker[i]:blockbreaker[i+1]]
        else:
            if datafile.instruction[blockbreaker[i]].type == 'label:':
                print("\n{}:".format(datafile.instruction[blockbreaker[i]].out))
                f.write("\n{}:\n".format(datafile.instruction[blockbreaker[i]].out))
                datafile.block = datafile.instruction[blockbreaker[i] + 1 : blockbreaker[i+1]]
                if datafile.instruction[blockbreaker[i]].op1[0:4] =='func':
                    datafile.currentscope = datafile.instruction[blockbreaker[i]].op1
                    print("\t" + "pushl %ebp")
                    f.write("pushl %ebp\n")
                    print("\t" + "movl %esp, %ebp")
                    f.write("movl %esp, %ebp\n")
                    print("\t" + "subl ${}, %esp".format(datafile.numberofvariables[datafile.instruction[blockbreaker[i]].op1] - 4))
                    f.write("subl ${}, %esp\n".format(datafile.numberofvariables[datafile.instruction[blockbreaker[i]].op1] - 4))
            else:
                datafile.block = datafile.instruction[blockbreaker[i] : blockbreaker[i+1]] 
        blockasmgenerate()  

def JE(i):
    datafile.blockout.append("je " + datafile.block[i].out)

def JNE(i):
    datafile.blockout.append("jne " + datafile.block[i].out)

def JLE(i):
    datafile.blockout.append("jle " + datafile.block[i].out)

def JL(i):
    datafile.blockout.append("jl " + datafile.block[i].out)

def JGE(i):
    datafile.blockout.append("jge " + datafile.block[i].out)

def JG(i):
    datafile.blockout.append("jg " + datafile.block[i].out)

def ADD(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    # print datafile.L , "Hello"
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("addl " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def SUB(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("subl " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def AND(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("and " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def OR(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("or " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def XOR(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("xor " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def PUSH_ARG(i) :
    var = datafile.block[i].out
    t = False
    try:
        int(var)
    except:
        t = True
    if t and datafile.addressdescriptor[var] != None :
        place = datafile.addressdescriptor[var]
    else :
        place = register.emptyregister(i)
        datafile.blockout.append("movl  " + register.mem(var) +', ' +  register.mem(place))
        datafile.registerdescriptor[place] = var
    datafile.blockout.append("pushl %" + place)
    pass

def ARG(i):
    pass

def LABEL(i):
    pass

def GET(i):
    datafile.blockout.append("movl %eax, " + register.mem(datafile.block[i].out))
    pass

#CMP destination, source
#One has to be in register 
def COMPARE(i):
    (y,z) = (datafile.block[i].op1,datafile.block[i].op2)
    try:
        int(z)
        datafile.zprime = z
    except:
        datafile.zprime = register.getz(z)
    
    try:
        int(y)
        datafile.yprime = y
    except:
        if datafile.addressdescriptor[y] != None:
            datafile.L = datafile.addressdescriptor[y]
        elif datafile.zprime in datafile.allvariables:
            reg = register.emptyregister(i)
            datafile.blockout.append("movl " + register.mem(y) + ", " + register.mem(reg))
            datafile.L = reg
            datafile.registerdescriptor[reg] = y
            datafile.addressdescriptor[y] = reg
        else:
            datafile.L = y

    datafile.blockout.append("cmp " + register.mem(y) + ", " + register.mem(z))
    register.freereg(y,i)
    register.freereg(z,i)
    
def MUL(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("imul " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def ASSIGN(i):
    (y,l) = (datafile.block[i].op1,datafile.block[i].out)
    register.getreg(l,y,i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)

def RETURN(i):
    if datafile.block[i].out != None:
        datafile.blockout.append("movl " + register.mem(datafile.block[i].out) + ", %eax")
    datafile.blockout.append("movl %ebp, %esp")
    datafile.blockout.append("popl %ebp")
    datafile.blockout.append("ret")
    datafile.currentscope = ""

def DIV(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    register.storereg('edx')
    datafile.blockout.append("xor %edx, %edx")
    try :
        int(z)
        reg = register.emptyregister(i,['edx', 'eax'])
        datafile.blockout.append('mov $' + z + ", %" + reg)
        datafile.zprime = reg
    except :
        if datafile.addressdescriptor[z] == 'eax':
            register.storereg(z)
        register.getz(z)
        pass
    register.getreg(l, y, i, 'eax')
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("idivl " + register.mem(datafile.zprime))
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def MOD(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    register.storereg('edx')
    datafile.blockout.append("xor %edx, %edx")
    try :
        int(z)
        datafile.zprime = z
        reg = register.emptyregister(i,['eax', 'edx'])
        datafile.blockout.append('mov $' + z + ", %" + reg)
        datafile.zprime = reg

    except :
        if datafile.addressdescriptor[z] == 'eax':
            register.storereg(z)
        register.getz(z)
        pass
    register.getreg(l, y, i, 'eax')
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("idivl " + register.mem(datafile.zprime))
    datafile.L = 'edx'    #since the remainder is store in edx 
    register.update(l)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def ARRAYLOAD(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    #sb $0, array1($3)  index addressing mode is used here
    try:
        int(z)
        datafile.zprime = z
    except:
        register.getz(z)
    reg = register.emptyregister(i)
    datafile.blockout.append("movl " + register.mem(datafile.zprime) + ", " + register.mem(reg))
    datafile.L = reg
    datafile.blockout.append("movl " + y + "(, %" + reg +", 4 ), %" + reg )
    register.UpdateAddressDescriptor(l)


def GOTO(i):
    datafile.blockout.append('jmp ' + datafile.block[i].out)

def ARRAY(i):
    pass

def CALL(i):
    datafile.blockout.append('call ' + datafile.block[i].out)
    datafile.blockout.append('addl ${}, %esp'.format(datafile.numberofarguments[datafile.block[i].out]-8))


OperatorMap = {'jl': JL, 'je': JE, 'jg':JG, 'jle':JLE, 'jge':JGE, 'jne':JNE, 'pusharg':  PUSH_ARG, 'arg' : ARG, 'label:' : LABEL, 'get' : GET, 'cmp': COMPARE, '+' : ADD, '-' : SUB,'|' : OR, '&': AND, '^': XOR, '*' : MUL, '=' : ASSIGN, 'ret' : RETURN, '/' : DIV, '%' : MOD, '<-' : ARRAYLOAD, 'goto' : GOTO, 'ARRAY' : ARRAY , 'call' : CALL }
