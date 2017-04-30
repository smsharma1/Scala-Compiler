from activationr import *
esp = 0
activr = Stack()
ebp = 0

def backpatch(code, breaklist, label):
    for i in breaklist:
        code[i] = code[i] + label
        print code[i]