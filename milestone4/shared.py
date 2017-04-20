from activationr import *
esp = 0
activr = Stack()
ebp = 0

def backpatch(code, breaklist, label):
    print breaklist, "this is breaklist ", label, " and this is label"
    for i in breaklist:
        code[i] = code[i] + label
        print code[i]