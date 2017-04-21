class a3acinst:
    def __init__(self,instnumber,operand1,operator,operand2,type,out):
        self.instnumber = instnumber
        self.type = type
        self.op1 = operand1
        self.op2= operand2
        self.operator = operator
        self.out = out 

globalsection =  set()
allvariables = set()
memorymap = dict()
setofarray = {}
numberofvariables = dict()
numberofarguments = dict()
instruction = []
block = []
currentscope = ""
blocknuminst = 0