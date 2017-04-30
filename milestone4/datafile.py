class a3acinst:
    def __init__(self,instnumber,operand1,operator,operand2,type,out):
        self.instnumber = instnumber
        self.type = type
        self.op1 = operand1
        self.op2= operand2
        self.operator = operator
        self.out = out 

globalsection =  set() #to store global data
allvariables = set() #to store all the variables  
memorymap = dict() #to store the function act record
meta = dict()
setofarray = {}  #set of arrays
setofList = {} #set of LIST
setofString = {}
numberofvariables = dict()  #length of variables in particular function
numberofarguments = dict() #length of arguments 
instruction = []  #to store the 3AC instruction
block = []  #to store basic block
currentscope = "" #name of  currentscope
blocknuminst = 0  #
registerlist = ['eax', 'ebx', 'ecx', 'edx'] #registers
registerdescriptor = {}   #register descriptor
addressdescriptor = {} #address descriptor 
symtable = [] #to store next use etc
lineno = 0
L = None
yprime = None 
zprime = None
Listoffset = 0

blockout = [] #to store the output of block