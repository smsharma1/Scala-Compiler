import copy

class Dictlist(dict):
	def __setitem__(self, key, value):
		try:
			self[key]
		except KeyError:
			super(Dictlist, self).__setitem__(key, [])
		self[key].append(value)

class SymbolTable:
	uid = 0
	def __init__(self, parent, name, argList=[], returnType=None): # parent scope and symbol table name
		self.functions = Dictlist()
		self.variables = {}
		self.arrays = {}
		self.classes = Dictlist()
		self.objects = Dictlist()
		self.name = name
		self.parent = parent
		self.uid = SymbolTable.uid
		self.argList = argList
		self.returnType = returnType
		SymbolTable.uid = SymbolTable.uid+1
		# print self.argList

	def LookUpVar(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
				return scope.variables[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def LookUpFunc(self, symbolName, argList):
		scope = self
		while(scope):
			print "scope.functions " , scope.functions
			if symbolName in scope.functions:
				for func in scope.functions[symbolName]:
				#	print func.argList
					if argList == func.argList:
						return scope
			scope = scope.parent
		return False
	
	# def LookUpArr(self, symbolName, argList):
	# 	scope = self
	# 	while(scope):
	# 		print "scope.arrays " , scope.functions
	# 		if symbolName in scope.arrays:
	# 			for array in scope.arrays[symbolName]:
	# 			#	print func.argList
	# 				if argList == array.argList:
	# 					return True
	# 		scope = scope.parent
	# 	return False

	def LookUpSymbol(self, symbolName):
		scope = self
		while(scope is not None):
			value = scope.LookUpCurrentScope(symbolName)
			if(value):
				return value
			else:
				scope = scope.parent
		return False

	def LookUpCurrentScope(self, symbolName):
		scope = self
		if symbolName in scope.variables:
			# print "inupsymbol",scope.variables[symbolName][1]
			return "variable"
		elif symbolName in scope.functions:
			print symbolName, " *******", (scope.functions[symbolName])[0].returnType  
			return "function"
		elif symbolName in scope.arrays:
			return "array"
		elif symbolName in scope.classes:
			return "class"
		elif symbolName in scope.objects:
			return "object"
		else:
			return False

	def LookUpClass(self, symbolName, argList):
		# print symbolName, " ", argList
		# print self.name, " ", self.classes
		scope = self
		while(scope):
			if symbolName in scope.classes:
				for class_name in scope.classes[symbolName]:
				#	print class_name.argList
					if argList == class_name.argList:
						return scope
			scope = scope.parent
		return False
		# if symbolName in self.classes:
		# 	for class_name in self.classes[symbolName]:
		# 		# print class_name.argList
		# 		if argList == class_name.argList:
		# 			return 
		# 	return False
		# else:
		# 	return False

	def LookUpObject(self, symbolName):

		scope = self
		while(scope):
			if symbolName in scope.objects:
				return scope.objects[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def GetFuncScope(self, symbolName, argList):
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList:
					return func
			return False
		else:
			return False
	
	def GetClassScope(self, symbolName, argList):
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return class_name
			return False
		else:
			return False

	def InsertVar(self, symbolName, val, type_name):
		print "testing",type_name
		if self.LookUpCurrentScope(symbolName):
			return False
		else:
			self.variables[symbolName] = [val, type_name]
			return True

	def InsertFunc(self, symbolName, argList, returnType):
#		print symbolName, " ", argList, " ", returnType
		if self.LookUpCurrentScope(symbolName):
			return False 
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList and self.returnType == returnType:
					return False
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
		else:
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
			# print self.functions
		return self.functions[symbolName][0]
	
	def InsertArray(self, symbolName, argList, boundlist):
		if self.LookUpCurrentScope(symbolName):
			return False
		else:
			self.arrays[symbolName] = [argList, boundlist]
			return True

	def InsertClass(self, symbolName, argList):
		# print symbolName, " " , argList
		if self.LookUpCurrentScope(symbolName):
			return False
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return False
			self.classes[symbolName] = SymbolTable(self, symbolName, argList=argList)
		else:
			self.classes[symbolName] = SymbolTable(self, symbolName, argList=argList)
			# print self.classes
		return self.classes[symbolName][0]
	
	def InsertObject(self, symbolName, className, valList):
		# print symbolName, " "
		if self.LookUpCurrentScope(symbolName):
			return False
		if className in self.classes:
			class_name = self.classes[className]
			self.objects[symbolName] = copy.deepcopy(class_name)
			self.InvokeConstr(self.objects[symbolName], valList)
		else:
			print "%s not found" % (className)

	def InsertSingletonObject(self, symbolName):
		if self.LookUpCurrentScope(symbolName):
			return False
		self.singletonObject = SymbolTable(self, symbolName)
		return self.singletonObject

	# def setName(self, symbolName):
	# 	self.name = symbolName

	# def setArglist(self, argList):
	# 	self.argList = argList

	# def setReturnType(self, returnType):
	# 	self.returnType = returnType

	def NewFuncScope(self):
		return SymbolTable(self, "temp")

	def InsertFuncDetails(self, symbolName, argList, returnType):
#print symbolName, " ", argList, " ", returnType
		if self.LookUpCurrentScope(symbolName):
			return False
		self.argList = argList
		self.name = symbolName
		self.returnType = returnType

	def InvokeConstr(self, classScope, valList):
		# you can get arglist from scope.arglist to parse valList
		pass