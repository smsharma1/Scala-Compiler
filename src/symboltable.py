class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.name = name
        self.parent = parent