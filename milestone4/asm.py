import datafile

asmcode = []

def blockasmgenerate():
    datafile.blocknuminst = len(datafile.block)

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
