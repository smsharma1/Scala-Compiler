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
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.variables):
				pass
			else:
				return False
		while(scope):
			if symbolName in scope.variables:
				# print "hola ", scope.variables[symbolName]
				return scope.variables[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def LookUpFunc(self, symbolName, argList):
		scope = self
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.functions):
				pass
			else:
				return False
		while(scope):
		#	print "scope.functions " , scope.functions
			if symbolName in scope.functions:
				print scope.functions
				for func in scope.functions[symbolName]:
				#	print func.argList
					if argList == func.argList:
						return True
			scope = scope.parent
		return False
	
	def LookUpCurrentScope(self, symbolName):
		scope = self
		# print symbolName
		if symbolName in scope.variables:
			# print "inupsymbol",scope.variables[symbolName][1]
			return [self.variables[symbolName][1]]
		elif symbolName in scope.functions:
			# print self.functions[symbolName][0].returnType, " return type look up current scope"
			return [self.functions[symbolName][0].returnType]
		elif symbolName in scope.classes:
			return ['class', self.classes[symbolName][0].name]
		elif symbolName in scope.objects:
			# print self.objects[symbolName]
			return ['object', self.objects[symbolName][0].name]
		else:
			return False

	def LookUpSymbol(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
			#	print "inupsymbol",scope.variables[symbolName][1]
				return scope.variables[symbolName][1]
			elif symbolName in scope.functions:
			#	print symbolName, " *******", (scope.functions[symbolName])[0].returnType  
				return (scope.functions[symbolName])[0].returnType
			scope = scope.parent
		return False

	def LookUpClass(self, symbolName, argList):
		# print symbolName, " ", argList
		# print self.name, " ", self.classes
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.objects):
				pass
			else:
				return False
		scope = currentScope
		while(scope):
			if symbolName in scope.classes:
				for class_name in scope.classes[symbolName]:
					# print class_name.argList
					if argList == class_name.argList:
						return True
		return False

	def LookUpObject(self, symbolName):
		scope = self
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.objects):
				pass
			else:
				return False
		while(scope):
			if symbolName in scope.objects:
				# print  scope.objects[symbolName][0], " In Look up object"
				# print scope.objects[symbolName][0].name, " ", scope.objects[symbolName][0].variables, " "
				return scope.objects[symbolName][0]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def GetFuncScope(self, symbolName, argList):
		scope = self
		while(scope):
		#	print "scope.functions " , scope.functions
			if symbolName in scope.functions:
				for func in scope.functions[symbolName]:
				#	print func.argList
					#print argList, " ", func.argList, "arglists in getfuncscope"
					if argList == func.argList:
						return func
			scope = scope.parent
		return False
	
	def GetClassScope(self, symbolName, argList):
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return class_name
			return False
		else:
			return False

	def LookDotThing(self,rootScope,symbolName):
		looklist = symbolName.split('.')
		name = ""
		myobject = self.LookUpObject(looklist[0])
		print myobject," myobject ",looklist[0]
		if myobject :
			if looklist[1] in myobject.functions:
				return [myobject.functions[looklist[1]][0].returnType]
			elif looklist[1] in myobject.variables:
				return [myobject.variables[looklist[1]][1]]		
		else:
			for name in looklist[:-1]:
				# print name," inelse ",rootScope.classes
				if name in rootScope.classes:
					rootScope = rootScope.classes[name]
				else:
					return False
			if name in rootScope.functions:
				for func in rootScope.functions[symbolName]:
					return [func.returnType]
			else:
				return False
		return False

	def LookUpSymbolType(self, symbolName):
		scope = self
		# print "ddddddd",symbolName
		while(scope):
			value = scope.LookUpCurrentScope(symbolName)
			if(value):
				# print value
				return value
			scope = scope.parent
		return False

	def SetObjectName(self, currentName, newName):
		# print "Insetobjectname", currentName," ",newName
		myobject = self.LookUpObject(currentName)
		self.objects[newName] = copy.deepcopy(myobject)
		self.objects.pop(currentName, None)
		# print self.objects[newName][0], "last line in set object name"

	def InsertVar(self, symbolName, val, type_name, length=0):
		# print "testing",type_name
		if symbolName in self.variables:
			return False
		else:
			self.variables[symbolName] = [val, type_name, length]

	def InsertFunc(self, symbolName, argList, returnType):
#		print symbolName, " ", argList, " ", returnType
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList and self.returnType == returnType:
					return False
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
		else:
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
			# print self.functions
		return self.functions[symbolName][0]
	
	def InsertClass(self, symbolName, argList):
		# print symbolName, " " , argList
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
		# print symbolName, " ", className, " insert object***************"
		if self.LookUpCurrentScope(symbolName):
			return False
		scope = self
		while(scope):
			if className in scope.classes:
				# print  "className"
				class_name = scope.classes[className][0]
				self.objects[symbolName] = copy.deepcopy(class_name) #notice that we actually need self here instead of scope
				# print class_name, " ", self.objects[symbolName],"after deepcopy"
				# self.InvokeConstr(self.objects[symbolName], valList)
				return True
			scope = scope.parent
		# print "%s not found" % (className)
		return False

	def InsertSingletonObject(self, symbolName):
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
		print symbolName, " ", argList, " ", returnType
		print "hello in insertfuncdetails"
		self.argList = argList
		self.name = symbolName
		self.returnType = returnType

	def InvokeConstr(self, classScope, valList):
		# you can get arglist from scope.arglist to parse valList
		pass

	def Dumper(self, scope, fileh):
		# column description
		# return Type
		# type name ActType/class type
		# print scope.name , fileh
		buffer = ""
		# print scope.variables, "i am symbol table"
		# print scope.objects, "i am symbol table"
		# print scope.name, " in dumper"
		offset = 0
		fileh.write(scope.name+"\n")
		for key in scope.variables:
			if(scope.variables[key][1]=="STRING"):
				size = scope.variables[key][2]*2
				prevoffset = offset
				offset = offset + size
			elif(scope.variables[key][1][5:10]=="ARRAY"):
				typename = self.Size(scope.variables[key][1][10:])
				# print typename, scope.variables[key][2]
				size = int(scope.variables[key][2])*typename
				prevoffset = offset
				offset = offset + size
			elif(scope.variables[key][1][0:5]=="ARRAY"):
				typename = self.Size(scope.variables[key][1][5:])
				# print typename, scope.variables[key][2]
				size = int(scope.variables[key][2])*typename
				prevoffset = offset
				offset = offset + size
			else:
				size = self.Size(scope.variables[key][1])
				prevoffset = offset
				offset = offset + size
			buffer = "var, " + str(key) +", "+ str(scope.variables[key][1])+ ", " + str(size) + ", " + str(prevoffset)+ "\n"
			fileh.write(buffer)
		for key in scope.objects:
			buffer = "object, " + str(key) + ", "+ str(scope.objects[key][0].name) +", \n"
			fileh.write(buffer)
		for key in scope.functions:
			arglist = str(scope.functions[key][0].argList)
			buffer = "function, " + str(key) + ", " + arglist+ "-->" + str(scope.functions[key][0].returnType)+",  " + " \n"
			fileh.write(buffer)
		fileh.write('\n')

	def Size(self, type ):
		if type=="INT":
			return 4
		elif type=="CHAR":
			return 2
		elif type=="BYTE":
			return 1
		elif type=="SHORT":
			return 2
		elif type=="LONG":
			return 8
		elif type=="FLOAT":
			return 4
		elif type=="DOUBLE":
			return 8
		else:
			return 10