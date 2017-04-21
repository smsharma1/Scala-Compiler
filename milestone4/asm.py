import datafile
import register
asmcode = []

OperatorMap = {'+': ADD, '-': SUB, '*': MUL, '=' : ASSIGN,'/' : DIV, '%' : MOD, '^' : XOR, '&' : AND, '|' : OR, 'ret' : RETURN, 'call' : CALL, 'print' : PRINT, 'read' : READ, 'goto' : GOTO, '<-' : LOAD_ARRAY, '->' : STORE_ARRAY, 'array' : DEC, 'printstr': PRINT_STR, 'cmp': COMPARE, 'jl': JL, 'je': JE, 'jg':JG, 'jle':JLE, 'jge':JGE, 'jne':JNE, 'pusharg':  PUSH_ARG, 'arg' : ARG, 'label' : LABEL, 'get' : GET}

def blockasmgenerate():
    datafile.blocknuminst = len(datafile.block)
    register.initializeblock()
    for i in range(0,len(datafile.block) - 1):
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)

def asm():
    print(".section .data")
    for data in datafile.globalsection:
        print("{}:".format(data))
        print("\t.long {}".format(1))
    for data in datafile.setofarray.keys():
        print("{}:".format(data))
        print("\t.zero {}".format(4*int(datafile.setofarray[data])))
    print("\n.section .text\n")
    print('.global main\n')
    print('main:')
    blockbreaker = set()
    blockbreaker.add(0)   #starting of first block
    for i in range(0,len(datafile.instruction)):
        if datafile.instruction[i].type == 'label:':
            blockbreaker.add(i)   #any target of a goto statement is a leader
        elif datafile.instruction[i].type in ['jg', 'je', 'jle', 'jge', 'je', 'jne', 'ret', 'goto', 'call' ]:
            blockbreaker.add(i+1) #any statement that follows a goto statement is a leader
    blockbreaker.add(len(datafile.instruction))
    blockbreaker.sorted()
    blockbreaker = sorted(blockbreaker)
    for i in range (0,len(blockbreaker)-1):
        if i == 0:
            datafile.block = datafile.instruction[blockbreaker[i]:blockbreaker[i+1]]
        else:
            if datafile.instruction[blockbreaker[i]] == 'label:':
                datafile.block = datafile.instruction[blockbreaker[i] + 1 : blockbreaker[i+1]]
                if datafile.instruction[blockbreaker[i]].op1[0:4] =='func':
                    datafile.currentscope = datafile.instruction[blockbreaker[i]].op1
                    print("\t" + "pushl %ebp")
                    print("\t" + "movl %esp, %ebp")
                    print("\t" + "subl ${}, %esp".format(datafile.numberofvariables[datafile.instruction[blockbreaker[i]].op1] - 4))
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
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    register.getreg(l, y, i)
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("addl " + register.mem(datafile.zprime) + ", " + register.mem(datafile.L))
    register.UpdateAddressDescriptor(x)
    register.freereg(y, i)
    register.freereg(z, i)
