#!/usr/bin/env python
import ply.yacc as yacc
import pydot
import sys
from symboltable import *
from shared import *
# Get the token map from the lexer.  This is required.
from lexer import tokens
Error = 0
tempcount = 0
graph = pydot.Dot(graph_type='digraph')
rootScope = SymbolTable(None, "root")
currentScope = rootScope
a3AC=[]
symbol_file = open("Symbols.csv", "w+")
def newtemp():
	global tempcount
	tempcount = tempcount + 1
	return "t" + str(tempcount)

class Node:
	uid=0
	def __init__(self,type,children,leaf,typelist=[],seqNo=1,order='',isLeaf=False,notreenode=False,code=[], breaklist = [], continuelist = [], place="A",next=None,meta=None):
		self.meta = meta
		self.next = next
		self.code = code 
		self.place = place
		self.type = type
		self.typelist = typelist
		Node.uid = Node.uid + 1
		self.uid = Node.uid
		self.name = type+"##"+str(self.uid)
		self.breaklist = breaklist
		self.continuelist = continuelist
		if(notreenode):
			return
		# print self.name, " ", typelist
		self.childOrder = ""
		count = 1
		leafno = 0
		childno = 0
		for letter in order:
			if letter == 'l':
				if leaf[leafno] != None:
					self.childOrder = self.childOrder + leaf[leafno] + " "
					count = count + 1
				leafno = leafno + 1
			elif letter == 'c':
				if children[childno] != None:
					self.childOrder = self.childOrder + children[childno].name + " "
					count = count + 1
				childno = childno + 1


		if isLeaf:
			self.node = pydot.Node(self.name, style="filled", fillcolor="green", myNo=seqNo, myOrder=self.childOrder)
		else:
			self.node = pydot.Node(self.name, style="filled", fillcolor="red", myNo=seqNo, myOrder=self.childOrder)
		graph.add_node(self.node)
		self.children = children
		self.leaf = leaf
		count = 1
		leafno = 0
		childno = 0
		for letter in order:
			if letter == 'l':
				if leaf[leafno] != None:
					term = Node(leaf[leafno], [], [],seqNo = count, isLeaf=True).name
					graph.add_edge(pydot.Edge(self.name, term))
					count = count + 1
				leafno = leafno + 1
			elif letter == 'c':
				if children[childno] != None:
					graph.add_edge(pydot.Edge(self.name, children[childno].name))
					# mynode = graph.get_node("EndStatement 1")
					mynodes = graph.get_nodes()
					for nodes in mynodes:
					# graph.write_png('debug.png')
						if nodes.get_name() == children[childno].name:
							nodes.set("myNo", count)
						#	print(nodes.to_string())
					count = count + 1
				childno = childno + 1

def p_CompilationUnit(p):
	'''CompilationUnit : ImportDeclarationss ClassObjectsList'''
						# | ClassesObjects'''
	if len(p)==3:
		p[0] = Node("CompilationUnit", [p[1], p[2]],[], order="cc",code=p[2].code)
	global a3AC
	a3AC = p[0].code 
	# 	p[0] = Node("CompilationUnit", [p[1]],[])
def p_ImportDeclarationss(p):
	'''ImportDeclarationss : ImportDeclarations
							| empty'''
	if(p[1] == None):
		pass
	else:
		p[0] = p[1]
		# p[0] = Node("ImportDeclarationss",[p[1]],[], order="c")
#<import declarations> ::= <import declaration> | <import declarations> <import declaration>

def p_ImportDeclarations(p):
	'''	ImportDeclarations : ImportDeclaration
							| ImportDeclarations ImportDeclaration'''
	if len(p)==3:
		p[0] = Node("ImportDeclarations", [p[1], p[2]],[], order="cc")
	else:
		p[0] = p[1]
		#Node("ImportDeclarations", [p[1]],[], order="c")

#<import declaration> ::= import <type name> ;

def p_ImportDeclaration(p):
	'''ImportDeclaration : R_IMPORT AmbiguousName'''
	p[0] = Node("ImportDeclaration", [p[2]],[p[1]], order = "lc")


def p_ClassObjectsList(p):
	'''ClassObjectsList : ClassObjectsList ClassAndObjectDeclaration
						| ClassAndObjectDeclaration'''
	if len(p) ==2:
		p[0] = p[1] #Node('ClassObjectsList',[p[1]],[], order="c")
	else:
		# print p[1].code
		p[0] = Node('ClassObjectsList',[p[1],p[2]],[], order = "cc",code=p[1].code+p[2].code)
#<classes_objects> ::= <class_object> | <class_object> <classes_objects>
def p_ClassAndObjectDeclaration(p):
	'''ClassAndObjectDeclaration : ObjectDeclaration
								| ClassDeclaration'''
	p[0] = p[1] #Node('ClassAndObjectDeclaration',[p[1]],[], order="c")


#<object_declaration> ::= object <identifier> <super>? { method_body }
def p_ObjectDeclaration(p):
	'''ObjectDeclaration : ObjectHeader ObjectBody'''
	print p[2].code
	p[0] = Node("ObjectDeclaration", [p[1], p[2]],[ ], order="cc",code=p[2].code)

def p_ObjectHeader(p):
	'''ObjectHeader : R_OBJECT ID Super'''
	global currentScope
	currentScope =  currentScope.InsertSingletonObject(p[1])
	p[0] = Node("ObjectHeader",[p[3]],[p[1],p[2]],order="llc")

def p_ObjectBody(p):
	'''ObjectBody : Block'''
	global currentScope
	global symbol_file
	currentScope.Dumper(currentScope, symbol_file)
	currentScope = currentScope.parent

	p[0] = p[1] #Node("ObjectBody",[p[1]],[],order='c')
	#print p[0].code,"adad"

#<class_declaration> ::= class <identifier> <class_header> <super>? { <class body declarations>? }

def p_ClassDeclaration(p):
	'''ClassDeclaration :  ClassHeader ClassBody '''
	p[0] = Node("ClassDeclaration", [p[1], p[2]],[], order="cc",code=p[2].code) 
					#  | R_CLASS ID ClassHeader Super BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
					#  | R_CLASS ID ClassHeader Super BLOCKOPEN  BLOCKCLOSE'''
	# R_CLASS Identifier ClassHeader BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
	# 				 |
	# 				 	 | R_CLASS Identifier ClassHeader BLOCKOPEN  BLOCKCLOSE
def p_ClassBody(p):
	'''ClassBody : Super BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
					| Super BLOCKOPEN  BLOCKCLOSE'''
	global currentScope
	# print currentScope
	currentScope = currentScope.parent
#	print currentScope.classes
	if len(p) == 5:
		p[0] = Node("ClassBody",[p[1],p[3]],[],order="cc",code=p[3].code)
	else:
		p[0] = Node("ClassBody",[p[1]],[ ],order="c")
# 	if len(p)==8:
# 		
# 	# elif "Super" in p[4].name:
# 	# 	p[0] = Node("ClassDeclaration", [p[2], p[3], p[4]],[p[1], p[5], p[6]])
# 	elif len(p)==7:
# 		p[0] = Node("ClassDeclaration", [p[3], p[4]],[p[1],p[2],p[5], p[6]], order="llccll")
# # 	else:
# # 		p[0] = Node("ClassDeclaration", [p[2], p[3]],[p[1], p[4], p[5]])
# # #<super> ::= extends <class type>

def p_Super(p):
	'''Super : R_EXTENDS ClassType
			| empty'''
	if(p[1] == None):
		pass
	elif len(p) == 3:
		p[0] = Node("Super", [p[2]],[p[1]], order="lc")
#<class_header> ::= ( <formal parameter list>? )
def p_ClassHeader(p):
	'''ClassHeader : R_CLASS ID LPARAN FormalParameterLists RPARAN'''
	
	global currentScope
	# print currentScope
	if p[4] != None:
		if(currentScope.LookUpClass(p[2], p[4].typelist)):
			print "Method Declaration Error at line number: " + str(p.lexer.lineno) 
			global Error
			Error = Error + 1 
		currentScope = currentScope.InsertClass(p[2],p[4].typelist)
	else:
		if(currentScope.LookUpClass(p[2],[])):
			print "Method Declaration Error at line number: " + str(p.lexer.lineno)
			Error = Error + 1 
		currentScope = currentScope.InsertClass(p[2],[])

	p[0] = Node("ClassHeader", [p[4]],[p[1], p[2]], order="llc")
	
def p_FormalParameterLists(p):
	'''FormalParameterLists : FormalParameterList
							| empty'''
	if(p[1] == None):
		pass
	else:
		p[0] = p[1]
	# elif 'FormalParameterList' in p[1].name:
	# 	p[0] = Node('FormalParameterList',[p[1]],[],order="c")

#<class body declarations> ::= <class body declaration> | <class body declarations> <class body declaration>
def p_ClassBodyDeclarations(p):
	'''ClassBodyDeclarations : ClassBodyDeclaration
							 | ClassBodyDeclarations ClassBodyDeclaration'''
	if len(p)==3:
		p[0] = Node("ClassBodyDeclarations", [p[1], p[2]],[], order="cc",code=p[1].code + p[2].code)
	else:
		p[0] = p[1]
#<class body declaration> ::= <field declaration> | <method declaration>
def p_ClassBodyDeclaration(p):
	'''ClassBodyDeclaration : FieldDeclaration
						| MethodDeclaration'''
	p[0] = p[1]
	# if "FieldDeclaration" in p[1].name:
	# 	p[0] = Node("ClassBodyDeclaration", [p[1]],[], order="c")
	# else:
	# 	p[0] = Node("ClassBodyDeclaration", [p[1]],[], order="c")

#<formal parameter list> ::= <formal parameter> | <formal parameter list> , <formal parameter>
def p_FormalParameterList(p):
	'''FormalParameterList : ID COLON Type
							| ID COLON Type COMMA FormalParameterList'''
	if len(p)==4:
		p[0] = Node("FormalParameterList", [p[3]],[p[1],p[2]], order="llc")
	else:
		p[0] = Node("FormalParameterList", [p[3], p[5]],[p[1],p[2], p[4]], order="llclc")

#<field declaration> ::=  val <variable declarator> ;
def p_FieldDeclaration(p):
	'''FieldDeclaration : VariableHeader VariableDeclarator1 EndStatement'''
	p[0] = Node("FieldDeclaration", [p[1],p[2]],[], order="cc",code=p[2].code)
#<variable declarator> ::= <identifier> | <identifier>: <type>   | <identifier> <variable_declarator_extra>

def p_VariableDeclarator1(p):
	''' VariableDeclarator1 : ID COLON Type EQUALASS VariableInitializer
							| ID EQUALASS VariableInitializer
							| ID COLON Type EQUALASS VariableInitializer COMMA VariableDeclarator1
							| ID EQUALASS VariableInitializer COMMA VariableDeclarator1'''
	global currentScope
	global symbol_file
	global esp
	if(currentScope.LookUpVar(p[1])):
		print "Variable " + p[1] + " already declared error at line number: " + str(p.lexer.lineno)
		global Error  
		Error = Error + 1
	if len(p)==4:
		if(p[3].typelist[0] == 'object'):
			code = ['= ' + p[1] + ' '+  p[3].place + ' '+ p[1]]
			currentScope.SetObjectName("temp", p[1])
			# print self.LookUpObject(p[1]).name, " ", self.LookUpObject(p[1]).variables, "before dumper is called"
			currentScope.Dumper(currentScope.LookUpObject(p[1]),symbol_file)
		elif "ARRAY" in p[3].typelist[0]:
			#TO check
			print p[3].typelist, p[1], "variable declarator1"
			code = ['ARRAY ' + p[1] + " " + str(p[3].typelist[1])]
			currentScope.InsertVar(p[1],0,p[3].typelist[0], length= p[3].typelist[1])
		else:
			code = ['= ' + p[1] + ' '+  p[3].place + ' '+ p[1]]
			# print p[3].typelist, " in variabledeclarator1"
			currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node("VariableDeclarator1", [p[3]],[p[1],p[2]], order="llc",code=p[3].code + code)
	elif len(p)==8:
		code = ['= ' + p[1] + ' '+  p[5].place + ' '+ p[1]]
		currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node("VariableDeclarator1", [p[3], p[5], p[7]],[p[1],p[2], p[4], p[6]], order="llclclc",code = p[5].code + code + p[7].code )
	elif p[2] == ':':
		code = ['= ' + p[1] + ' '+  p[5].place + ' '+ p[1]]
		currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node("VariableDeclarator1", [p[3], p[5]],[p[1],p[2], p[4]], order="llclc",code = p[5].code + code)
	else:
		code = ['= ' + p[1] + ' '+  p[3].place + ' '+ p[1]]
		if(p[3].typelist[0] == 'object'):
			currentScope.SetObjectName("temp", p[1])
			currentScope.Dumper(currentScope.LookUpObject(p[1]),symbol_file)
		else:
			currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node("VariableDeclarator1", [p[3], p[5]],[p[1],p[2], p[4]], order="llclc",code = p[3].code + code + p[5].code)

def p_FuncArgumentListExtras(p):
	''' FuncArgumentListExtras : VariableDeclarators
								| empty'''
	k = []
	if(p[1] == None):
		pass
	else:
		p[0]= p[1]
		if(p[0].meta is None): p[1].meta = 0
		code = []
		k = p[1].place.split(',,,')
		print p[1].place.split(',,,') , "hello there"
    	k.reverse()
    	for k1 in k:
        	code.append("arg " + k1)
		p[0].code = code
		#print p[0].code, "aaaaaaa"
		# p[0] = Node("FuncArgumentListExtras", [p[1]],[],typelist = p[1].typelist, order="c") 

def p_VariableDeclarators(p):
	'''VariableDeclarators : VariableDeclarator
						| VariableDeclarator COMMA VariableDeclarators'''
	if len(p)==4:
		p[0] = Node("VariableDeclarators", [p[1], p[3]],[p[2]],typelist = p[1].typelist + p[3].typelist, order="clc",place = p[1].place + ',,,' +  p[3].place) 
	else:
		p[0] = p[1]
		# p[0] = Node("VariableDeclarators", [p[1]],[],typelist = p[1].typelist, order="c") 
						
def p_VariableDeclarator(p):
	'''VariableDeclarator : ID COLON Type '''
	global currentScope
	# print currentScope.variables, "tttttttttttttttttttttttttttttttttttttttttttttttttttttt"
	if(currentScope.LookUpVar(p[1])):
		print "Variable " + p[1] + " already declared error at line number: " + str(p.lexer.lineno)
		global Error 
		Error = Error + 1
	else:
		currentScope.InsertVar(p[1],0,p[3].typelist[0])
	#print "jajajaja",p[1]
	p[0] = Node("VariableDeclarator", [p[3]],[p[1],p[2]],typelist = p[3].typelist, order="llc",place = p[1]) 

def p_VariableInitializer(p):
	'''VariableInitializer : ArrayInitializer
							| Expression
							| ClassInstanceCreationExpression'''

	p[0] = p[1]
	print "VariableInitializer",p[1].type
	# p[0] = Node("VariableInitializer", [p[1]],[],typelist = p[1].typelist, order="c")

def p_ArrayInitializer(p):
	''' ArrayInitializer : R_NEW R_ARRAY LSQRB Type RSQRB LPARAN INT RPARAN
							| R_NEW R_ARRAY LSQRB Type RSQRB LPARAN INT COMMA INT RPARAN'''
	if len(p) == 9:
		p[0] = Node('ArrayInitializer',[p[4]],[p[1],p[2],p[3],p[5],p[6],p[7],p[8]],typelist =['ARRAY' + p[4].typelist[0], int(p[7])], order="lllcllll")
	else:
		p[0] = Node('ArrayInitializer',[p[4]],[p[1],p[2],p[3],p[5],p[6],p[7],p[8],p[9], p[10]],typelist=['ARRAYARRAY'+p[4].typelist[0], int(p[7]),int(p[9])], order="lllcllllll")

def p_EndStatement(p):
	'''EndStatement : SEMICOLON
					| LINEFEED'''
	p[0] = Node(p[1], [], [], isLeaf=True,notreenode=True)
	# p[0] = Node("EndStatement", [],[p[1]], order="l")
#<method declaration> ::= <method header> <method body>
def p_MethodDeclaration(p):
	'MethodDeclaration : MethodHeader MethodBody'
	#code1 = ['goto ' + p[1].meta[2:]]
	#code2 = ['label: ' + p[1].meta[2:]]
	p[0] = Node("MethodDeclaration", [p[1], p[2]],[], order="cc",code= p[1].code + p[2].code + ['ret'])
#<method header> ::= def <method declarator> : <type> = | def <method declarator> =
def p_MethodHeader(p):
	'''MethodHeader : MethodDefine MethodDeclarator MethodReturnTypeExtras'''
	global currentScope
	parentScope = currentScope.parent
	l1 = ["label: " + p[2].meta]
	# print ("\n\n\n\nam i vissibl now")
	if p[3] != None:
		if(currentScope.LookUpFunc(p[2].typelist[0], p[2].typelist[1:])):
		#	print "in if part"
			print "Method Declaration Error at line number: " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
		else:
			parentScope.functions[p[2].typelist[0]] = currentScope
			currentScope.InsertFuncDetails(p[2].typelist[0], p[2].typelist[1:], p[3].typelist)
			# print currentScope.name ," i am in method header see me please"
		p[0] = Node("MethodHeader", [p[1], p[2], p[3]],[],typelist = p[2].typelist + p[3].typelist,order="ccc",meta=p[2].meta,code=l1 + p[2].code)
	else:
		if(currentScope.LookUpFunc(p[2].typelist[0], p[2].typelist[1:])):
			print "Method declaration error at line number: " + str(p.lexer.lineno)
			Error = Error + 1
		else:
			parentScope.functions[p[2].typelist[0]] = currentScope
			currentScope.InsertFuncDetails(p[2].typelist[0], p[2].typelist[1:],[])
			print currentScope.name ," i am in method header see me please"
		p[0] = Node("MethodHeader", [p[1], p[2], p[3]],[],typelist = p[2].typelist + [] ,order="ccc",meta=p[2].meta,code=l1+p[2].code)

def p_MethodDefine(p):
	'''MethodDefine : R_DEF'''
	global currentScope
	currentScope = currentScope.NewFuncScope()	
	# print "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"	
	p[0] = Node(p[1], [],[], isLeaf=True)
	

#<method declarator> ::= <identifier> ( <formal parameter list>? )
def p_MethodDeclarator(p):
	'''MethodDeclarator : ID LPARAN FuncArgumentListExtras RPARAN'''
	# if len(p)==4:
	# 	p[0] = Node("MethodDeclarator", [p[1]],[p[2], p[3]])
	# else:
	global currentScope
	meta = 'func_' +str(currentScope.parent.uid) + "_" + p[1]
	if p[3] == None:
		p[0] = Node("MethodDeclarator", [p[3]],[p[1]],typelist=[p[1]], order="lc",meta=meta)
	else:
		p[0] = Node("MethodDeclarator", [p[3]],[p[1]],typelist=[p[1]] + p[3].typelist, order="lc",meta=meta,code=p[3].code)
	#	print p[3].code,"aasdada"


def p_MethodReturnTypeExtras(p):
	'''MethodReturnTypeExtras : COLON MethodReturnType EQUALASS
								| EQUALASS
								| empty '''
	if(p[1] == None):
		pass
	elif len(p)==4:
		p[0] = Node("MethodReturnTypeExtras", [p[2]],[],typelist = p[2].typelist, order="c")
	elif "=" in p[1]:
		p[0] = Node("MethodReturnTypeExtras", [],[p[1]], order="l")

def  p_MethodReturnType(p):
	'''MethodReturnType : Type'''
	p[0] = p[1]
	# p[0] = Node("MethodReturnType", [p[1]],[],typelist = p[1].typelist, order="c")
	# else:
	# 	p[0] = Node("MethodReturnType", [],[p[1]], order="l")

#<method body> ::= <block> | ;
def p_MethodBody(p):
	'''MethodBody : Block'''
	global currentScope
	global symbol_file
	currentScope.Dumper(currentScope, symbol_file)
	currentScope = currentScope.parent
	# print currentScope.functions
	p[0] = p[1]
	# p[0] = Node("MethodBody", [p[1]],[], order="c")

#<type> ::= <primitive type> | <reference type>
def p_Type(p):
	'''Type : PrimitiveType
		| ReferenceType'''
	# print p[1].typelist
	#print p[1]
	p[0] = p[1]
	# if "PrimitiveType" in p[1].type:
	# 	p[0] = Node("Type", [p[1]],[],typelist = p[1].typelist, order="c") 
	# else:
	# 	p[0] = Node("Type", [p[1]],[],typelist = p[1].typelist, order="c") 

#<primitive type> ::= <numeric type> | boolean
def p_PrimitiveType(p):
	'''PrimitiveType : NumericType
					| R_BOOLEAN'''
	if p[1] == 'Boolean':
		p[0] = Node(p[1], [], [], typelist = ['BOOL'], isLeaf=True)
	else:
		p[0] = p[1]
	# if "NumericType" in p[1].type:
	# 	p[0] = Node("PrimitiveType", [p[1]],[],typelist = p[1].typelist, order="c") 
	# else:
	# 	p[0] = Node("PrimitiveType", [],[p[1]],['BOOL'] ,order="l") 

#<numeric type> ::= <integral type> | <floating-point type>
def p_NumericType(p):
	'''NumericType : IntegralType
				| FloatingPointType'''
	p[0] = p[1]
	# if "IntegralType" in p[1].type:
	# 	p[0] = Node("NumericType", [p[1]],[],typelist = p[1].typelist, order="c") 
	# else:
	# 	p[0] = Node("NumericType", [p[1]],[],typelist = p[1].typelist, order="c") 

#<integral type> ::= byte | short | int | long | char

def p_IntegralType(p):
	'''IntegralType : R_BYTE
				 | R_SHORT
				 | R_INT
				 | R_LONG
				 | R_CHAR
				 | R_STRING
				 | R_UNIT'''
	if 'Byte' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['BYTE'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['BYTE'], order="l") 
	elif 'Short' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['SHORT'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['SHORT'], order="l")
	elif 'Int' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['INT'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['INT'], order="l")
	elif 'Long' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['LONG'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['LONG'], order="l")
	elif 'Char' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['CHAR'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['CHAR'], order="l")
	elif 'String' in p[1]:
		p[0] = Node(p[1], [], [], typelist = ['STRING'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['STRING'], order="l")
	else:
		p[0] = Node(p[1], [], [], typelist = ['UNIT'], isLeaf=True)
		# p[0] = Node("IntegralType", [],[p[1]],typelist = ['UNIT'], order="l")

#<floating-point type> ::= float | double
def p_FloatingPointType(p):
	'''FloatingPointType : R_FLOAT
						| R_DOUBLE'''
	if 'Float' in p[1]:
		p[0] = Node("FloatingPointType", [],[p[1]],typelist = ['FLOAT'], order="l")
	else:
		p[0] = Node("FloatingPointType", [],[p[1]],typelist = ['DOUBLE'], order="l")

def p_ReferenceType(p):
	'''ReferenceType : ArrayType'''
	if "ArrayType" in p[1].type:
		p[0] = Node("ReferenceType", [p[1]],[],typelist = p[1].typelist ,order="c") 

def p_ClassType(p):
	'''ClassType : ID
				 |	R_WITH ClassType'''
	if len(p) == 2:
		p[0] = Node("ClassType", [ ] ,[p[1]], order="l")
	else:
		p[0] = Node("ClassType", [p[2]],[p[1]], order="lc")
#<array type> ::= <type> [ ]
def p_ArrayType(p):
	'''ArrayType : R_ARRAY LSQRB Type RSQRB
				| R_LIST LSQRB Type RSQRB'''
	p[0] = Node("ArrayType", [p[3]],[p[1], p[2], p[4]],typelist = ['ARRAY' + p[3].typelist[0]], order="llcl") 

#<block> ::= { <block statements>? }
def p_Block(p):
	'''Block : BLOCKOPEN BLOCKCLOSE
			| BLOCKOPEN BlockStatements BLOCKCLOSE'''
	if len(p)==3:
		p[0] = Node("Block", [],[],notreenode=True,code=p[2].code, breaklist = p[2].breaklist, continuelist = p[2].continuelist)
	else:
		p[0] = p[2]
	#print p[0].code,'bbbbb'
#<block statements> ::= <block statement> | <block statements> <block statement>
def p_BlockStatements(p):
	'''BlockStatements : BlockStatement
					| BlockStatements BlockStatement'''
	if len(p)==2:
		p[0] = p[1]
	else:
		p[2].breaklist[:] = [i+len(p[1].code) for i in p[2].breaklist]
		p[2].continuelist[:] = [i+len(p[1].code) for i in p[2].continuelist]
		p[0] = Node("BlockStatements", [p[1],p[2]],[], order="cc",code=p[1].code + p[2].code, breaklist = p[1].breaklist + p[2].breaklist, continuelist = p[1].continuelist + p[2].continuelist)
	#print p[0].code,"aaaaa"

def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement
					| Statement
					| MethodDeclaration'''
	p[0] = p[1]
	#print p[0].code, "asdad"

def p_LocalVariableDeclarationStatement(p):
	'LocalVariableDeclarationStatement : LocalVariableDeclaration EndStatement'
	p[0] = p[1]

def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : VariableHeader VariableDeclarationBody'''
	p[0] = Node("LocalVariableDeclaration", [p[1],p[2]],[], order="cc",code=p[2].code)

def p_VariableDeclarationBody(p):
	'''VariableDeclarationBody : ID COLON Type EQUALASS VariableInitializer
		| ID EQUALASS VariableInitializer'''
	global currentScope
	global symbol_file
	if(currentScope.LookUpVar(p[1])):
		print "Variable " + p[1] + " already declared error at line number: " + str(p.lexer.lineno)
		global Error
		Error = Error + 1
	if len(p) == 6:
		code = ['= ' + p[1] + ' '+  p[5].place + ' '+ p[1]]
		# print "checking ",p[3].typelist," ",p[5].typelist
		if(not allowed(p[3].typelist[0], p[5].typelist[0])):
			# print p.lexer.lineno
			print "Type mismatch in line " + str(p.lexer.lineno)
			# global Error
			Error = Error + 1 
	#		sys.exit("Error: ", p[1]," : ", p[3].typelist[0], " = ", p[5].typelist[0], " type mismatch")
		currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node(p[4],[p[3],p[5]],[p[1],p[2]], order="llcc",isLeaf=True,code = p[5].code + code)
	else:
		code =[]
		if(p[3].typelist[0] == 'object'):
			code = ['= ' + p[1] + ' '+  p[3].place + ' '+ p[1]]
			# print p[1]
			currentScope.SetObjectName("temp", p[1])
		#	print p[1] ,"jajajajj"
			currentScope.Dumper(currentScope.LookUpObject(p[1])[0],symbol_file)
		else:
		#	print p[3].typelist, "I am in typelist"
			print p[3].typelist, p[1], "variable declaration"
			if(p[3].typelist[0][0:5] == 'ARRAY'):
				try:
					p[3].typelist[2]
					code = ['ARRAY ' + p[1] + " " + str(p[3].typelist[1]) + " " + str(p[3].typelist[2])]
					currentScope.InsertVar(p[1],0,p[3].typelist[0], arrlength= [p[3].typelist[1],p[3].typelist[2]])
				except:
					code = ['ARRAY ' + p[1] + " " + str(p[3].typelist[1])]
					currentScope.InsertVar(p[1],0,p[3].typelist[0], length= p[3].typelist[1])
				
			else:
				code = ['= ' + p[1] + ' '+  p[3].place + ' '+ p[1]]
				currentScope.InsertVar(p[1],0,p[3].typelist[0])
		p[0] = Node(p[2],[p[3]],[p[1]], order="lc",isLeaf=True,code = p[3].code + code)


def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
				| IfThenStatement
				| IfThenElseStatement
				| WhileStatement
				| ForStatement'''
	p[0] = p[1]
	# print p[0].breaklist , " i am in statement with breaklist"


def p_StatementWithoutTrailingSubstatement(p):
	'''StatementWithoutTrailingSubstatement : Block
										| EmptyStatement
										| ExpressionStatement
										| SwitchStatement
										| BreakStatement
										| ContinueStatement
										| ReturnStatement'''
	p[0] = p[1]

# <statement no short if> ::= <statement without trailing substatement> | <if then else statement no short if>
# | <while statement no short if> | <for statement no short if>
def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
						| IfThenElseStatementNoShortIf'''
	p[0] = p[1]
	# p[0] = Node("StatementNoShortIf", [p[1]],[],order='c')

#<expression statement> ::= <statement expression> ;
def p_ExpressionStatement(p):
	'ExpressionStatement : StatementExpression EndStatement'
	p[0] = p[1]

#<statement expression> ::= <assignment> | <preincrement expression>
# | <postincrement expression> | <predecrement expression> | <postdecrement expression>
# | <method invocation> | <class instance creation expression>
def p_StatementExpression(p):
	'''StatementExpression : Assignment
						| MethodInvocation
						| ClassInstanceCreationExpression'''
						# | PreincrementExpression
						# | PostincrementExpression
						# | PredecrementExpression
						# | PostdecrementExpression
	p[0] =p[1] #Node("StatementExpression", [p[1]],[],order='c')

def p_IfThenStatement(p):
	'''IfThenStatement : M R_IF LPARAN Expression RPARAN Statement N
					|	M R_IF LPARAN R_TRUE RPARAN Statement N
					| 	M R_IF LPARAN R_FALSE RPARAN Statement N'''
	s_after = newtemp()
	print s_after, "I am in IfThenStatement"
	if p[4] == 'true':
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code =p[6].code + ['label: ' + s_after], breaklist = p[6].breaklist, continuelist = p[6].continuelist )
	elif p[4] == 'false':
		p[6].breaklist[:] = [i+1 for i in p[6].breaklist]
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code=['jump ' +  s_after] + p[6].code + ['label: ' + s_after], breaklist = p[6].breaklist, continuelist = p[6].continuelist)
	else:
		if(not (p[4].typelist[0] == 'BOOL')):
			print "Syntax error in expression of while Statement at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("ERROR: While statement expression is not BOOL it is "+p[4].typelist[0])
		p[6].breaklist[:] = [i+len(p[4].code)+2 for i in p[6].breaklist]
		p[6].continuelist[:] = [i+len(p[4].code)+2 for i in p[6].continuelist]
		p[0] = Node(p[2], [p[4], p[6]],[],order='cc',isLeaf=True,code=p[4].code + ['cmp ' + p[4].place + ' 0']+['je ' + s_after] + p[6].code + ['label: ' + s_after], breaklist = p[6].breaklist, continuelist = p[6].continuelist)

def p_IfThenElseStatement(p):
	'IfThenElseStatement : ifstat elsestat'
	# '''IfThenElseStatement : M R_IF LPARAN Expression RPARAN StatementNoShortIf elsestat
	# 					| M R_IF LPARAN R_TRUE RPARAN StatementNoShortIf elsestat
	# 					| M R_IF LPARAN R_FALSE RPARAN StatementNoShortIf elsestat'''

	# '''IfThenElseStatement : M R_IF LPARAN Expression RPARAN StatementNoShortIf R_ELSE Statement N
	# 					| M R_IF LPARAN R_TRUE RPARAN StatementNoShortIf R_ELSE Statement N
	# 					| M R_IF LPARAN R_FALSE RPARAN StatementNoShortIf R_ELSE Statement N'''
	p[2].breaklist[:] = [i+len(p[1].code) for i in p[2].breaklist]
	p[2].continuelist[:] = [i+len(p[1].code) for i in p[2].continuelist]
	# print p[1].breaklist + p[2].breaklist, " this is breaklist in if then else statement"
	p[0] = Node("IfThenElseStatement", [p[1],p[2]],[],order='cc',code=p[1].code + p[2].code + ['label: ' + p[1].next], breaklist = p[1].breaklist + p[2].breaklist, continuelist = p[1].continuelist + p[2].continuelist)
	# if p[4] == "true" or p[4] == "false":
	# 	p[0] = Node("IfThenElseStatement", [p[6], p[7]],[p[2], p[4]],order='llcc')
	# else:
	# 	if(not (p[4].typelist[0] == 'BOOL')):
	# 		print "Syntax error in expression of if then else statement at line " + str(p.lexer.lineno)
	# 		global Error
	# 		Error = Error + 1
	# 		#sys.exit("Error in IfThenelseStatement")
	# 	p[0] = Node("IfThenElseStatement", [p[4], p[6], p[7]],[p[2]],order='lccc')

def p_ifstat(p):
	'''ifstat : M R_IF LPARAN Expression RPARAN StatementNoShortIf
			| M R_IF LPARAN R_TRUE RPARAN StatementNoShortIf
			| M R_IF LPARAN R_FALSE RPARAN StatementNoShortIf'''
	s_else = newtemp()
	s_after = newtemp()
	# print s_else,s_after, "I am in Ifstat"
	if p[4] == "true":
		# print p[6].code[p[6].breaklist[0]], " i am the code in ifstat which should be backpatched"
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code=p[6].code + ['label: ' + s_else],next=s_after, breaklist = p[6].breaklist, continuelist = p[6].continuelist)
	elif p[4] == "false":
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code=['jump ' +  s_after] + p[6].code ['label: ' + s_else],next=s_after, breaklist = p[6].breaklist, continuelist = p[6].continuelist)
	else:
		if(not (p[4].typelist[0] == 'BOOL')):
			print "Syntax error in expression of if then else statement at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error in IfThenelseStatement")
		p[6].breaklist[:] = [i+len(p[4].code)+2 for i in p[6].breaklist]
		p[6].continuelist[:] = [i+len(p[4].code)+2 for i in p[6].continuelist]
		# print p[6].breaklist, "breaklist in ifstat"
		p[0] = Node(p[2], [p[4], p[6]],[],order='cc',isLeaf=True,code=p[4].code + ['cmp ' + p[4].place + ' 0']+['je ' + s_else] + p[6].code + ['goto ' + s_after] +  ['label: ' + s_else],next=s_after, breaklist = p[6].breaklist, continuelist = p[6].continuelist)


def p_elsestat(p):
	'elsestat : R_ELSE Statement N'
	p[0] = Node(p[1],[p[2]],[],order='c',isLeaf=True,code= p[2].code, breaklist=p[2].breaklist, continuelist = p[2].continuelist)
	
def p_IfThenElseStatementNoShortIf(p):
	'''IfThenElseStatementNoShortIf : ifstat elsenoshortif'''
	# '''IfThenElseStatementNoShortIf : ifstat R_ELSE StatementNoShortIf N'''
	p[2].breaklist[:] = [i+len(p[1].code) for i in p[2].breaklist]
	p[2].continuelist[:] = [i+len(p[4].code) for i in p[2].continuelist]
	p[0] = Node("IfThenElseStatementNoShortIf",[p[1],p[2]],[],order='cc',code=p[1].code + p[2].code + ['label: ' + p[1].next ], breaklist = p[1].breaklist + p[2].breaklist, continuelist = p[1].continuelist + p[2].continuelist)
	# if p[4] == "true" or p[4] == "false":
	# 	p[0] = Node("IfThenElseStatementNoShortIf", [p[6], p[8]],[p[2] ,p[4] ,p[7]],order='llclc')
	# else:
	# 	if(not (p[4].typelist[0] == 'BOOL')):
	# 		print "Syntax error in expression of if then else statement at line " + str(p.lexer.lineno)
	# 		global Error
	# 		Error = Error + 1
	# 		#sys.exit("Error in IfThenelseStatementnoshortif")
	# 	p[0] = Node("IfThenElseStatementNoShortIf", [p[4], p[6], p[8]],[p[2], p[7]],order='lcclc')
def p_elsenoshortif(p):
	'''elsenoshortif : R_ELSE StatementNoShortIf N '''
	p[0] = Node(p[1],[p[2]],[],order='c',code=p[2].code, breaklist = p[2].breaklist, continuelist = p[2].continuelist)

def p_SwitchStatement(p):
	'''SwitchStatement : Expression R_MATCH BLOCKOPEN SwitchBlockStatementGroups BLOCKCLOSE'''
	exp = p[1].place
	code = []
	ml = p[4].place.split(',,,')
	l = len(p[4].meta)-2
	code += ["label: " + p[4].meta[0]]
	for i in range(0, l):
		code += ["cmp " + ml[i] + " "  + exp]
		code += ["je " + p[4].meta[-i-2]]
	code += ["label: "  + p[4].meta[-1]]
	# we will backpatch here
	backpatch(p[4].code, p[4].breaklist, p[4].meta[-1])
	p[0] = Node(p[2], [p[1],p[4]],[],order='cc',isLeaf=True,code= p[4].code + code)

def p_SwitchBlockStatementGroups(p):
	'''SwitchBlockStatementGroups : SwitchBlock
					| SwitchBlockStatementGroups  SwitchBlock  '''
				#	| SwitchBlockStatementGroups LINEFEED SwitchBlock
	if len(p) ==  2:
		p[0] = p[1]
		vl = []
		test = newtemp()
		lab = newtemp()
		next1 = newtemp()
		print test,lab,next1, "I am in switch statement"
		vl.append(test)
		vl.append(lab)
		vl.append(next1)
		l1 = ["label: " + lab]
		l2 = ["goto " + next1]
		l3 = ["goto " + test]
		p[0].code =  l3 + l1 + p[1].code + l2
		p[0].place = p[1].place
		p[0].meta = vl
		p[0].breaklist = [i+len(l3)+len(l1) for i in p[1].breaklist]
		# p[0] = Node("SwitchBlockStatementGroups", [p[1]],[],order='c')
	elif len(p) == 3:
		vl = []
		lab = newtemp()
		print lab, "I am in switch statement"
		vl.append(p[1].meta[0])
		vl.append(lab)
		for k in p[1].meta[1:]:
			vl.append(k) 
		l1 = ["label: " + lab]
		l2 = ["goto " + p[1].meta[-1]]
		p[2].breaklist = [i+len(p[1].code)+len(l1) for i in p[2].breaklist]
		p[0] = Node("SwitchBlockStatementGroups", [p[1],p[2]],[],order='cc',meta = vl,code= p[1].code + l1 + p[2].code + l2,place=p[1].place + ",,,"+p[2].place, breaklist = p[1].breaklist + p[2].breaklist )
	
def p_SwitchBlock(p):
	'''SwitchBlock : SwitchBlockHeader SwitchBlockBody'''
	if len(p) ==  3:
		p[0] = Node("SwitchBlock", [p[1], p[2]],[],order='cc',code=  p[2].code ,place= p[1].place, breaklist = p[2].breaklist)

def p_SwitchBlockHeader(p):
	'SwitchBlockHeader : R_CASE ID IMPLIES1'
	p[0] = Node(p[1],[ ],[p[2],p[3]],order='ll',isLeaf=True,place = p[2])

def p_SwitchBlockBody(p):
	'''SwitchBlockBody : Expression
					| BlockStatements'''
	p[0] = Node("SwitchBlockBody", [p[1]],[],order='c',code= p[1].code,place= p[1].place, breaklist=p[1].breaklist)


def p_WhileStatement(p):
	'''WhileStatement : M R_WHILE  LPARAN Expression RPARAN Statement N
					|  M R_WHILE  LPARAN R_TRUE RPARAN Statement N
					|  M R_WHILE  LPARAN R_FALSE RPARAN Statement N'''
	s_begin = newtemp()
	s_after = newtemp()
	print s_begin , s_after ,"I am in While Statement"
	if(p[4] == 'true'):
		backpatch(p[6].code, p[6].breaklist, s_after)
		code = ["label: "+ s_begin ] + p[6].code + ["goto " + s_begin] + ["label: " + s_after ]
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code=code)
	elif p[4] == 'false':
		backpatch(p[6].code, p[6].breaklist, s_after)
		code = ["label: " + s_after ]
		p[0] = Node(p[2], [p[6]],[ p[4]],order='lc',isLeaf=True,code=code)
	else:
		backpatch(p[6].code, p[6].breaklist, s_after)
		backpatch(p[6].code, p[6].continuelist, s_begin)
		code = ["label: "+ s_begin] + p[4].code + ['cmp ' + p[4].place + " 0"] + ['je ' + s_after] + p[6].code + ["goto " + s_begin] + ["label: " + s_after ]
		if(not (p[4].typelist[0] == 'BOOL')):
			print "Syntax error in expression of while Statement at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("ERROR: While statement expression is not BOOL it is "+p[4].typelist[0])
		p[0] = Node(p[2], [p[4], p[6]],[],order='cc',isLeaf=True,code=code)

def p_ForStatement(p):
	'ForStatement : M R_FOR LPARAN ForVariables RPARAN Statement N'
	to_until = p[4].meta[1]
	if(to_until == 0):
		sym = "jge"
	else:
		sym = "jg"
	s_begin = newtemp()
	s_continue = newtemp()
	s_after = newtemp()
	print s_begin,s_continue, s_after,"I am in For statement"
	backpatch(p[6].code, p[6].breaklist, s_after)
	backpatch(p[6].code, p[6].continuelist, s_continue)
	# print p[6].breaklist, "breaklist in forstatement"
	# print p[6].continuelist, "continuelist in forstatement" 
	code =  p[4].code +  ["= " + p[4].place + " " + p[4].meta[2] + " " + p[4].place] + ["label: " + s_begin] +  ["cmp " + p[4].place + " " + p[4].meta[3]] + [sym + " " + s_after] + p[6].code + ["label: "+s_continue]+["+ " + p[4].place + " 1 " + p[4].place ] + ["goto " + s_begin] + ["label: " + s_after]
	p[0] = Node(p[2], [p[4], p[6]],[],order='cc',isLeaf=True,code=code)

def p_M(p):
	'M : empty'
	global currentScope
	newscope = currentScope.NewFuncScope()
	newscope.returnType = currentScope.returnType
	# print "dddddddddddddddddddddddddddddddddddddddd"
	newscope.parent = currentScope
	newscope.returnType = currentScope.returnType
	currentScope = newscope
def p_N(p):
	'N : empty'
	global currentScope
	for key in currentScope.sizevars:
		currentScope.parent.sizevars[key] = currentScope.sizevars[key]
	currentScope = currentScope.parent

# def p_ForExprs(p):
# 	'''ForExprs :  ForVariables EndStatement ForExprs
# 			| ForVariables'''
# 	if len(p) ==  4:
# 		p[0] = Node("ForExprs", [p[1],p[2],p[3]], [],order='ccc')
# 	else:
# 		p[0] = Node("ForExprs", [p[1]],[],order='c')

#''' for_variables : declaration_keyword_extras IDENTIFIER IN expression for_untilTo expression '''
def p_ForVariables(p):
	'ForVariables : DeclarationKeywordExtras ID LEFTARROW Expression ForUntilTo Expression'
	if(p[1] == None):
		# print "For variables ",currentScope.LookUpVar(p[2])[1]
		if(not (currentScope.LookUpVar(p[2])[1] == p[4].typelist[0] and p[4].typelist[0]==p[6].typelist[0]) ):
			print "Type mismatch in line " + str(p.lexer.lineno)
			global Error 
			Error = Error + 1
			#sys.exit("Error: ", p[2], "<-", p[4], " For Until To ", p[6], " type mismatch" )
	else:
		if(not (p[4].typelist[0] == p[6].typelist[0])):
			print "Type mismatch in line " + str(p.lexer.lineno)
			# global Error 
			Error = Error + 1
		else:
			currentScope.InsertVar(p[2], p[4].typelist[0])
	meta = []
	meta.append("#")
	meta.append(p[5].type)
	meta.append(p[4].place)
	meta.append(p[6].place)
	p[0] = Node("ForVariables", [p[1],p[4],p[5],p[6]], [p[2],p[3]],order='cllccc',meta=meta,code=p[4].code + p[6].code,place=p[2])
 #'''declaration_keyword_extras : variable_header | empty'''
#'''variable_header : K_VAL | K_VAR '''
def p_DeclarationKeywordExtras(p):
	'''DeclarationKeywordExtras : VariableHeader
								| empty'''
	if(p[1] == None):
		pass
	# elif 'VariableHeader' in p[1].name:
	# 	p[0] = Node('DeclarationKeywordExtras',[p[1]],[],order='c')
	else:
		p[0] = p[1]

def p_VariableHeader(p):
	'''VariableHeader : R_VAL
					| R_VAR'''
	p[0] = Node(p[1],[],[],isLeaf=True)

def p_ForUntilTo(p):
	'''ForUntilTo : R_UNTIL
				| R_TO'''
	p[0] = Node(p[1], [],[],isLeaf=True)


def p_BreakStatement(p) :
	'''BreakStatement : R_BREAK ID EndStatement
					| R_BREAK EndStatement'''
	if len(p) ==  4:
		p[0] = Node(p[1], [], [p[2]],order='l',isLeaf=True)
	else:
		code = ['goto ']
		p[0] = Node(p[1], [],[],isLeaf = True, code = code, breaklist = [0])

def p_ContinueStatement(p):
	'''ContinueStatement : R_CONTINUE ID EndStatement
						| R_CONTINUE  EndStatement'''
	if len(p) ==  4:
		p[0] = Node(p[1], [],[p[2]],order='l',isLeaf=True)
	else:
		code = ['goto ']
		p[0] = Node(p[1], [],[],isLeaf=True, code = code, continuelist = [0])

def p_ReturnStatement(p):
	'''ReturnStatement : R_RETURN Expression EndStatement
					| R_RETURN EndStatement'''
	if len(p) ==  4:
		code = ['ret2 ' + p[2].place]
		if not (currentScope.returnType == p[2].typelist):
			print currentScope.name
			print currentScope.returnType, p[2].typelist
			print "Actual returned object has different Type than function declared at " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
		p[0] = Node(p[1], [p[2]], [],order='c',isLeaf=True,code= p[2].code + code)
	else:
		code = ['ret1']
		p[0] = Node(p[1], [],[],isLeaf=True,code=code)


def p_Expression(p):
	'''Expression : OrExpression'''
	p[0] = p[1]
	# print p[1].typelist , "In expression",p[1].type
	# p[0] = Node("Expression", [p[1]],[],typelist = p[1].typelist,order='c')


# def p_CondititionalExpression(p):
# 	'''  CondititionalExpression : OrExpression
# 			|  OrExpression Expression COLON CondititionalExpression
# 									| Expression COLON CondititionalExpression'''


def p_LeftHandSide(p):
	'''LeftHandSide : AmbiguousName'''
					# | FieldAccess
	p[0] = p[1] #Node("LeftHandSide", [p[1]],[],typelist=p[1].type,order='c')

def p_AssignmentOperator(p):
	'''AssignmentOperator : EQUALASS
						| MULASS
						| DIVASS
						| MODASS
						| ADDASS
						| SUBASS
						| BITLEFTASS
						| BITRIGHTASS
						| BITRSFILLASS
						| BITANDASS
						| BITXORASS
						| BITORASS'''
	p[0] = Node(p[1], [],[],isLeaf=True,notreenode=True)

##check it very important issue
def p_Assignment(p):
	'''Assignment : LeftHandSide AssignmentOperator OrExpression
				| ArrayAccess EQUALASS OrExpression'''
				#| AmbiguousName LSQRB Expression COMMA Expression RSQRB EQUALASS OrExpression'''
	#print p[1].typelist,"hello ",p[3].typelist

	if p[2]=="=":
		code = ["<--> " + p[1].place  + " " +  p[3].place + " " + p[1].place ]
		p[1].meta = p[1].code
		p[1].code = []
		for met in p[1].meta:
			p[1].code.append(met.replace("<-","->"))

		# code = ["= " + p[1].place + " " + p[3].place + " " + p[1].place]
		# print p[1].typelist[0], " " ,  p[3].typelist[0], "assignment"
		if not allowed(p[1].typelist[0], p[3].typelist[0]) :
			print "Assignment mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
		p[0] = Node(p[2], [p[1], p[3]],[], order="cc",isLeaf=True,code = p[1].code + p[3].code + code)
						#return sys.exit("assignment mismatch error")
	else:
		print "000000000000000000000000000000000000000000000000000",p[2].type, p[1].place
		code = [p[2].type+ " " + p[1].place + " " + p[3].place + " " + p[1].place]
		# print p[1].typelist[0], " " ,p[2].type, " " , p[3].typelist[0], "assignment"
		if not allowed(p[1].typelist[0], p[3].typelist[0]) :
			print "Assignment mismatch error at line " + str(p.lexer.lineno)
			# global Error
			Error = Error + 1
		p[0] = Node(p[2].type, [p[1], p[3]],[], order="cc",isLeaf=True,code= p[1].code + p[3].code + code)

			


def p_OrExpression(p):
	'''OrExpression : AndExpression
				  | AndExpression OR OrExpression'''
	if(len(p)==2):
		p[0] = p[1]
	else:
		if (not (p[1].typelist[0] == 'BOOL' and p[3].typelist[0] ==  'BOOL')):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		nodename = newtemp()
		currentScope.InsertVar(nodename,0, 'BOOL')
		print nodename,"I am in OrExpression"
		code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
		p[0] = Node(p[2], [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)

def p_AndExpression(p):
	'''AndExpression : XorExpression
					| AndExpression AND XorExpression'''
	if len(p) ==  4:
		if (not (p[1].typelist[0] == 'BOOL' and p[3].typelist[0] ==  'BOOL')):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: " + p[1].typelist[0] + " " + p[3].typelist[0] + " type mismatch")
		nodename = newtemp()
		currentScope.InsertVar(nodename,0, 'BOOL')
		print nodename,"I am in And Expression"
		code1 = p[1].code + ["cmp " + p[1].place + " 0", "jle " + falselabel]+ p[3].code + ["cmp " + p[3].place + " 0", "jle " + falselabel, "jmp "+truelabel, "label: ", falselabel]
		code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
		p[0] = Node(p[2], [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
	else:
		p[0] = p[1]

def p_XorExpression(p):
	'''XorExpression : EqualityExpression
					| XorExpression BITXOR EqualityExpression'''
	if len(p) == 2:
		p[0] = p[1]
	else :
		if(not (p[1].typelist[0]=='BOOL' and p[3].typelist[0]=='BOOL')):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		nodename = newtemp()
		currentScope.InsertVar(nodename,0, 'BOOL')
		print nodename,"I am in Xorexpression"
		code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
		p[0] = Node(p[2], [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)



def p_EqualityExpression(p):
	'''EqualityExpression : RelationalExpression
						 | EqualityExpression EQUAL RelationalExpression
						| EqualityExpression NOTEQUAL RelationalExpression'''
	truelabel = newtemp()
	falselabel = newtemp()
	if len(p) ==  4:
		if(not p[1].typelist[0] == p[3].typelist[0]):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		if p[2] == "==":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Equality Expression"
			code = ["cmp "+  p[1].place + " "+ p[3].place] + ['je '+truelabel] + ["= " + nodename + " 0 " + nodename] +["goto " + falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node(p[2], [p[1], p[3]], [],typelist = ['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
		elif p[2] == "!=":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Equality Expression"
			code = ["cmp " + p[1].place + " " + p[3].place] + ['je '+truelabel] +["= " + nodename + " 0 " + nodename] +["goto " + falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node(p[2], [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)	
	else:
		p[0] = p[1]

def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression
						| RelationalExpression LT ShiftExpression
						| RelationalExpression GT ShiftExpression
						| RelationalExpression LE ShiftExpression
						| RelationalExpression GE ShiftExpression
						| RelationalExpression R_INSTANCEOF ReferenceType'''
	if len(p) ==  4:
		type_here = higher(p[1].typelist[0] , p[3].typelist[0])
		# print p[1].typelist[0],"jjfjfjfj"
		truelabel = newtemp()
		falselabel = newtemp()
		if(not type_here):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		if p[2] == "<":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Relational Expression"
			code = ["cmp " + p[1].place + " " + p[3].place] + ["jl "+truelabel] +["= " + nodename + " 0 " + nodename,"goto "+falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node(p[2], [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename )
		elif p[2] == ">":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Relational Expression"
			code = ["cmp " + p[1].place + " " + p[3].place] + ["jg "+truelabel] + ["= " + nodename + " 0 " + nodename, "goto "+falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node(">", [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
		elif p[2] == "<=":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Relational Expression"
			code = ["cmp " + p[1].place + " " + p[3].place] + ["jle "+truelabel] + ["= " + nodename + " 0 " + nodename, "goto "+falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node("<=", [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
		elif p[2] == ">=":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, 'BOOL')
			print nodename,"I am in Relational Expression"
			code = ["cmp " + p[1].place + " " + p[3].place] + ["jge "+truelabel] + ["= " + nodename + " 0 " + nodename, "goto "+falselabel, "label: "+truelabel, "= " + nodename + " 1 " + nodename, "label: "+falselabel]
			p[0] = Node(">=", [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
		elif p[2] == "instanceof":
			p[0] = Node("instanceof", [p[1], p[3]], [],typelist=['BOOL'],order='cc',isLeaf=True)
	else:
		p[0] = p[1]

def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression
					| ShiftExpression BITLSHIFT AdditiveExpression
					| ShiftExpression BITRSHIFT AdditiveExpression
					| ShiftExpression BITRSFILL AdditiveExpression'''
	if len(p) ==  4:
		type_here = higher(p[1].typelist[0] , p[3].typelist[0])
		if(not type_here):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		if p[2] == "<<":
			nodename = newtemp()
			print nodename,"I am in Shift Expression"
			currentScope.InsertVar(nodename,0, type_here)
			code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
			p[0] = Node("<<", [p[1], p[3]], [],typelist=[type_here],order='cc',isLeaf=True,code=p[1].code + p[3].code + code, place=nodename)
		elif p[2] == ">>":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, type_here)
			print nodename,"I am in Shift Expression"
			code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
			p[0] = Node("<<", [p[1], p[3]], [],typelist=[type_here],order='cc',isLeaf=True)
		elif p[2] == ">>>":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, type_here)
			print nodename,"I am in Shift Expression"
			code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
			p[0] = Node(">>>", [p[1], p[3]], [],typelist=[type_here],order='cc',isLeaf=True, code=p[1].code + p[3].code + code, place=nodename)
	else:
		p[0] = p[1]

# <additive expression> ::= <multiplicative expression> | <additive expression> + <multiplicative expression> | <additive expression> - <multiplicative expression>
def p_AdditiveExpression(p):
	'''AdditiveExpression : MultiplicativeExpression
							| AdditiveExpression PLUS MultiplicativeExpression
							| AdditiveExpression MINUS MultiplicativeExpression'''
	if len(p) ==  4:
		type_here = higher(p[1].typelist[0] , p[3].typelist[0])
		if(not type_here):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		if p[2] == "+":
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, type_here)
			print nodename,"I am in Additive Expression"
			code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
			p[0] = Node("+", [p[1],p[3]], [ ],typelist=[type_here],order='cc',isLeaf=True,code= p[1].code + p[3].code + code,place=nodename)
		else:
			nodename = newtemp()
			currentScope.InsertVar(nodename,0, type_here)
			print nodename,"I am in Additive Expression"
			code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
			p[0] = Node("-", [p[1],p[3]], [ ],typelist=[type_here],order='cc',isLeaf=True,code= p[1].code + p[3].code + code,place=nodename)
	#	print p[0].code
	#	print p[0].place
	else:
		p[0] = p[1]

# <multiplicative expression> ::= <unary expression> | <multiplicative expression> * <unary expression> | <multiplicative expression> / <unary expression> | <multiplicative expression> % <unary expression>
def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : UnaryExpression
								| MultiplicativeExpression MULTIPLICATION UnaryExpression
								| MultiplicativeExpression DIVISION UnaryExpression
								| MultiplicativeExpression MODULUS UnaryExpression'''
	if len(p) ==  4:
		nodename = newtemp()
		print nodename,"I am in Multiplicative Expression"
		code = [p[2] + " " + p[1].place + " " + p[3].place + " " + nodename]
		type_here = higher(p[1].typelist[0] , p[3].typelist[0])
		print p[1].typelist, "multiplicativeerror" , p[3].typelist, type_here
		if(not type_here):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
			#sys.exit("Error: ", p[1].typelist[0], " ", p[3].typelist[0]," type mismatch")
		currentScope.InsertVar(nodename,0, type_here)
		if p[2] == "*":
			p[0] = Node("*", [p[1], p[3]], [], typelist = [type_here], order='cc',isLeaf=True,code=p[1].code + p[3].code + code,place=nodename)
		elif p[2] == "%":
			p[0] = Node("%", [p[1], p[3]], [],order='cc',typelist = [type_here], isLeaf=True,code=p[1].code + p[3].code + code,place=nodename)
		elif p[2] == "/":
			p[0] = Node("/", [p[1], p[3]], [],order='cc', typelist = [type_here],isLeaf=True,code=p[1].code + p[3].code + code,place=nodename)
	else:
		p[0] = p[1]

def p_UnaryExpression(p):
	'''UnaryExpression :  UnaryExpressionNotPlusMinus'''
						# | PreincrementExpression
						# | PredecrementExpression'''
	if len(p) ==  3:
		if p[1] == "+":
			p[0] = Node("+", [p[2]], [],order='c',isLeaf=True)
		elif p[1] == "-":
			p[0] = Node("-", [p[2]], [],order='c',isLeaf=True)
	else:
		p[0] = p[1]
		#print p[1].typelist,"Unaryexpression"

def p_UnaryExpressionNotPlusMinus(p):
	'''UnaryExpressionNotPlusMinus : PostfixExpression
									| NOT UnaryExpression'''
									#| CastExpression'''
									#| BITNEG UnaryExpression
	if len(p) ==  3:
		nodename = newtemp()
		print nodename,"I am in Unary Expression Not Plus Minus Expression"
		code = [p[1] + " " + p[2].place + " " + nodename]
		# code = [nodename  + "="  + p[1] + " " + p[2].place]
		if(not p[2].typelist == ['BOOL']):
			print "Type mismatch error at line " + str(p.lexer.lineno)
			global Error
			Error = Error + 1
		type_here = ['BOOL']
		currentScope.InsertVar(nodename,0, type_here[0])
		p[0] = Node("!", [p[2]], [],typelist=type_here,order='c',isLeaf=True,code=p[2].code + code ,place= node)
	else:
		p[0] = p[1]

def p_PostfixExpression(p):
	'''PostfixExpression : Primary
							| AmbiguousName'''
							# | PostincrementExpression
							# | PostdecrementExpression'''
	p[0] = p[1]
#	print p[1].type, p[1].typelist, "in postfixexpression"
# <method invocation> ::= <method name> ( <argument list>? ) | <primary> . <identifier> ( <argument list>? ) | super . <identifier> ( <argument list>? )
#'''method_invocation : ambiguous_name LPAREN argument_list_extras RPAREN '''
def p_MethodInvocation(p):
	'''MethodInvocation : AmbiguousName LPARAN ArgumentLists RPARAN'''
					#		| AmbiguousName LPARAN RPARAN'''
						# | Primary DOT Identifier LPARAN ArgumentList RPARAN
						# | Super DOT Identifier LPARAN ArgumentList RPARAN'''
						# # | Super DOT Identifier LPARAN RPARAN
						# | AmbiguousName LPARAN RPARAN
						# | Primary DOT Identifier LPARAN RPARAN
	global currentScope
	global Error
	global esp
	global ebp
	code =[]
	# print p[1],"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	func_name = 'func_1' + "_" + p[1].type
	temp = None
#	print p[1].name,"name",currentScope.name
#	print p[3].type," ",p[3].typelist,"Method Invocation",currentScope.LookUpFunc(p[1].type, p[3].typelist)
	if(p[1].type == "println"):
		p[3].place = p[3].place.split(',,,')
		for i in range(0, len(p[3].typelist)):
			print p[3].typelist, "hey typelist"
			if(p[3].typelist[i] == 'STRING'):
				func_name = "printstr"
				code.append("printstr " + p[3].place[i])
			elif(p[3].typelist[i] == 'INT'):
				func_name = "print"
				code.append("print " + p[3].place[i])

		p[0] = Node("MethodInvocation", [p[1], p[3]], [] , order='cc',code=p[1].code + p[3].code + code)
		return
	if(p[1].type == "read"):
		if( len(p[3].type) > 1):
			print("read() takes only one argument")
			Error = Error + 1
		func_name = "read"
		code.append("read " + p[3].place)
		p[0] = Node("MethodInvocation", [p[1], p[3]], [] ,code =p[1].code + p[3].code + code, order='cc')
		return
	if p[3] == None :
		if (currentScope.LookUpFunc(p[1].type,[])==False):
			print "Method invocation error at line " + str(p.lexer.lineno)
			Error = Error + 1
	else:
		# print p[1].type, " " , p[3].typelist[0:], "in method invocation with typelist"
		if (currentScope.LookUpFunc(p[1].type, p[3].typelist[0:])==False):
			print "Method invocation error at line " + str(p.lexer.lineno)
			Error = Error + 1
		#sys.exit("Error: ",p[1].type, p[3].typelist[0:], " Method Invocation error")
	# else:
	# 	currentScope = currentScope.GetScope(p[1].name, p[3].typelist[0:])
	if p[3] == None:
		value = currentScope.GetFuncScope(p[1].type,[])
		code.append("call " + func_name)
		if(value == False):
			print "Method " + p[1].type+ " at line " + str(p.lexer.lineno)
	
			Error = Error + 1
			#sys.exit("Method" + p[1].type + " does not found")
		else:
			if(len(value.returnType) > 0):
				temp = newtemp()
				print temp, "I am in method invocation"
				code.append('get ' + temp)
			currentScope.InsertVar(temp,0, value.returnType[0])
			#print value.returnType,"checking"
			p[0] = Node("MethodInvocation", [p[1], p[3]], [ ],typelist = value.returnType , order='cc',code = code, place= temp)
	else:
		for k in p[3].meta:
			code.append("pusharg " + k)
		code.append("call " + func_name)
		value = currentScope.GetFuncScope(p[1].type,p[3].typelist)
		#print value.returnType,"checking"
		if(value == False):
			print "Method " + p[1].type+ " at line " + str(p.lexer.lineno)
			Error = Error + 1
			#sys.exit("Method" + p[1].type + " does not found")
		else:
			for idname in p[3].typelist:
				if "ARRAY" in idname:
					activr.push("newptr")
					esp = esp + currentScope.Size("POINTER")
				else:
					activr.push("value")
					# print idname, " ", "supposed to be argument type"
					esp = esp + currentScope.Size(idname)
				currentScope.itemcount = currentScope.itemcount + 1
			activr.push(ebp)
			ebp = esp
			activr.printstack()
				# you need to push var equal to size
			p[0] = Node("MethodInvocation", [p[1], p[3]], [ ],typelist = value.returnType , order='cc')
			for idname in p[3].typelist:
				if "ARRAY" in idname:
					activr.pop()
					esp = esp - currentScope.Size("POINTER")
				else:
					activr.pop()
					# print idname, " ", "supposed to be argument type"
					esp = esp - currentScope.Size(idname)
				currentScope.itemcount = currentScope.itemcount - 1
			if(len(value.returnType) > 0):
				temp = newtemp()
				print temp, "I am in method invocation"
				code.append('get ' + temp)
				currentScope.InsertVar(temp,0, value.returnType[0])
			p[0] = Node("MethodInvocation", [p[1], p[3]], [ ],typelist = value.returnType , order='cc',code= code,place=temp)
		
	# elif len(p) ==  4:
	# 	p[0] = Node("MethodInvocation", [p[1]], [p[2], p[3]])

def p_ArgumentLists(p):
	'''ArgumentLists : ArgumentList
						| empty'''
	#print "i ma here"
	if(p[1] == None):
	#	print "i ma here"
		pass
	else:
		p[0] = p[1]
		t = p[1].place.split(',,,')
		l = []
		for t1 in t:
			l.append(t1)
		p[0].meta = l
	#	print p[1].typelist, " argumentlists"

def p_Primary(p):
	'''Primary : PrimaryNoNewArray'''
				# | ArrayCreationExpression'''
	p[0] = p[1]

# <primary no new array> ::= <literal> | this | ( <expression> ) | <class instance creation expression>
# | <field access> | <method invocation> | <array access>

def p_PrimaryNoNewArray(p):
	'''PrimaryNoNewArray : Literal
						| LPARAN Expression RPARAN
						| MethodInvocation
						| ArrayAccess'''
						# | ClassInstanceCreationExpression
						# | FieldAccess
	if len(p) == 4:
		p[0] = p[2]
	else:
		# print p[1].type,"we are in p_PrimaryNoNewArray", p[1].typelist
		p[0] = p[1]
# <class instance creation expression> ::= new <class type> ( <argument list>? )

def p_ClassInstanceCreationExpression(p):
	'''ClassInstanceCreationExpression : R_NEW AmbiguousName LPARAN ArgumentLists RPARAN'''
								#		| R_NEW ClassType LPARAN RPARAN'''
	global Error
#	print "here ??"
	global currentScope
	if(p[4] != None):
		print p[2].type,"inclassinstance",p[4].typelist
		if(not currentScope.LookUpClass(p[2].type, p[4].typelist)):
			print "Class " + str(p[2])+" Not Found in currentScope error at line " + str(p.lexer.lineno)
			Error = Error + 1
			#return sys.exit(str(p[2])+"Class Not Found in currentScope")
		else:
			# print p[2].type, " " , p[4].typelist, " creating object"
			if(currentScope.InsertObject("temp", p[2].type, [])): #valList is to be sent here 
				pass
			else:
				print("Error: ", p[2].type, " alreay declared in currentScope" )
	else:
		#print p[2].type, "class name"
		if(not currentScope.LookUpClass(p[2].type, [])):
			print "Class " + str(p[2])+" Not Found in currentScope error at line " + str(p.lexer.lineno)
			Error = Error + 1
			#return sys.exit(str(p[2])+"Class Not Found in currentScope")
		else:
			# print p[2].type, " creating object"
			# print "here please"
			if(currentScope.InsertObject("temp", p[2].type, [])): #valList is to be sent here 
				pass
			else:
				print("Error: ", p[2].type, " alreay declared in currentScope" )


		# print p[2].type,"inclassinstanceasdasdadsasda",p[4].typelist
	p[0] = Node('ClassInstanceCreationExpression',[p[2], p[4]],[p[1]],typelist = ['object', p[2].type], order='lcc')
	# else:
	# 	p[0] = Node('ClassInstanceCreationExpression',[p[2]],[p[1],p[3],p[4]])

# <argument list> ::= <expression> | <argument list> , <expression>
def p_ArgumentList(p):
	'''ArgumentList : Expression
					| ArgumentList COMMA Expression'''
	if len(p) == 2:
		#print p[1].typelist, " p[1].typelist in ArgumentList"
		p[0] = p[1]
		# p[0] = Node('ArgumentList',[p[1]],[],typelist = p[1].typelist,order='c')
	else :
		p[0] = Node('ArgumentList',[p[1],p[3]],[p[2]],typelist = p[1].typelist + p[3].typelist,order='clc',code = p[1].code + p[3].code,place=p[1].place + ",,," + p[3].place)

# <array access> ::= <expression name> [ <expression> ] | <primary no new array> [ <expression>]
def p_ArrayAccess(p):
	'''ArrayAccess : AmbiguousName LSQRB Expression RSQRB
					| AmbiguousName LSQRB Expression COMMA Expression RSQRB'''
					# | PrimaryNoNewArray LSQRB Expression RSQRB'''
	if len(p) == 5:
		temp = newtemp()
		print temp, "I am in ArrayAcess"
		print p[3].type
		print p[1].typelist, "checking ArrayAccess iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
		size = currentScope.Size(p[1].typelist[0][5:])
		try:
			int(p[3].place)
			l1 = [ "<- " + p[1].place + " " +str(int(p[3].place)*size) + " " + temp]
		except:
			lab = newtemp()
			l1 = ["* " + p[3].place  + " " + str(size) + " " + lab ] + [ "<- " + p[1].place + " " + lab + " " + temp]
		# l1 = [ temp + " = " + p[1].place + " -> " + p[3].place]
		currentScope.InsertVar(temp,0, p[1].typelist[0][5:])
		print "\n\n", temp, "\n\n"
		print currentScope.name, " ", currentScope.variables
		p[0] = Node('ArrayAccess',[p[1],p[3]],[p[2],p[4]],typelist =[p[1].typelist[0][5:]] , order="clcl",code=p[3].code + l1,place = temp,meta=l1)
	else:
		temp = newtemp()
		temp2 = newtemp()
		print temp,temp2, " I am in arrayaccess "
		l=currentScope.LookUpVar(p[1].type)
		column = l[2]
		code = ['= ' + temp2 + " " + str(column) + " " + temp2 ]+ ["* " + temp2 + " " +p[3].place + " " + temp2] + [ "+ " + temp2 + " " +p[5].place + " " + temp2]
		l1 = [ "<- " + p[1].place + " " + temp2 + " " + temp]
		currentScope.InsertVar(temp2,0,'INT')
		currentScope.InsertVar(temp,0, p[1].typelist[0][10:])
		# l1 = [ temp + " = " + p[1].place + " -> " + temp2]
		p[0] = Node('ArrayAccess',[p[1],p[3],p[5]],[p[2],p[4],p[6]],typelist=[p[1].typelist[0][10:]], order="clclcl",code= p[5].code+p[3].code + code+l1,place=temp)

def p_AmbiguousName(p):
	'''AmbiguousName : ID
					| AmbiguousName DOT ID'''
	global currentScope
	global rootScope
	#print p[1],"hello i am here",currentScope.LookUpSymbol(p[1])
	
	if len(p)==2:
		if p[1] == 'println':
			p[0] = Node(p[1], [], [], typelist = [], isLeaf=True)
		elif p[1] == 'read':
			p[0] = Node(p[1], [], [], typelist = [], isLeaf=True)
		else:
			returnType = currentScope.LookUpSymbolType(p[1])
		# print returnType, "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
		# if(t=="variable"):
		# 	returnType = currentScope.LookUpVar(p[1])[1]
		# elif(t=="function"):
		# 	returnType = currentScope.LookUpFunc(p[1]).returnType
		# elif(t=="class"):
		# 	returnType = ['class',currentScope.LookUpClass(p[1]).name]
		# elif(t=="object"):
		# 	returnType = ['object', currentScope.LookUpObject(p[1]).name]
		# else:
		# 	returnType = False

			if(returnType):
				p[0] = Node(p[1], [], [], typelist = returnType, isLeaf=True,place=p[1])
			else:
				print "No Symbol found for " + str(p[1]) + " error at line " + str(p.lexer.lineno)
				global Error 
				Error = Error + 1
			#sys.exit("No symbol found for "+str(p[1]))
		# p[0] = Node('AmbiguousName',[],[p[1]],typelist = currentScope.LookUpSymbol(p[1]),order='l')
	else:
		thing = currentScope.LookDotThing(rootScope, p[1].type+"."+p[3])
		# print "here **************************",thing
		if(thing):
			p[0] = Node(p[1].type+"."+p[3],[p[1]],[p[2],p[3]],typelist = thing, order='cll',place=p[1].type+"."+p[3])

# <literal> ::= <integer literal> | <floating-point literal> | <boolean literal> | <character literal> | <string literal> | <null literal>
def p_Literal(p):
	'''Literal : IntegerLiteral
				| FloatingPointLiteral
				| BooleanLiteral
				| CharacterLiteral
				| StringLiteral
				| NullLiteral'''
	
	p[0] = p[1]
	# p[0] = Node("Literal", [p[1]],[],typelist = p[1].typelist,order='c')
# <integer literal> ::= <decimal integer literal> | <hex integer literal> | <octal integer literal>

def p_BooleanLiteral(p):
	'BooleanLiteral : BOOL'
	p[0] = Node(p[1], [], [], typelist = ['BOOL'], isLeaf=True,place=str(p[1]))
	# p[0] = Node('BooleanLiteral',[],[p[1]],typelist = ['BOOL'],order='l')

def p_IntegerLiteral(p):
	 'IntegerLiteral : INT'
	 p[0] = Node(p[1], [], [], typelist = ['INT'], isLeaf=True,place = str(p[1]))
	#  p[0] = Node('IntegerLiteral',[],[p[1]],typelist = ['INT'],order='l')

def p_FloatingPointLiteral(p):
	'FloatingPointLiteral : FLOAT'
	p[0] = Node(p[1], [], [], typelist = ['FLOAT'], isLeaf=True,place=str(p[1]))
	# p[0] = Node('FloatingPointLiteral',[],[p[1]],typelist =['FLOAT'],order='l')

def p_CharacterLiteral(p):
	'CharacterLiteral : CHAR'
	p[0] = Node(p[1], [], [], typelist = ['CHAR'], isLeaf=True,place=str(p[1]))
	# p[0] = Node('CharacterLiteral',[],[p[1]],typelist =['CHAR'],order='l')

def p_StringLiteral(p):
	'StringLiteral : STRING'
	length = len(p[1])
	p[0] = Node(p[1], [], [], typelist = ['STRING', length], isLeaf=True,place=str(p[1]))
	# p[0] = Node('StringLiteral',[],[p[1]],typelist = ['STRING'],order='l')


# # # <null literal> ::= null
def p_NullLiteral(p):
	'NullLiteral : R_NULL'
	p[0] = Node(p[1], [], [], typelist = ['NULL'], isLeaf=True,place=str(p[1]))
	# p[0] = Node("NullLiteral", [],[p[1]],typelist = ['NULL'],order='l')

#<empty statement> ::= ;
def p_EmptyStatement(p):
	'EmptyStatement : EndStatement'
	p[0] = p[1]
	# p[0] = Node("EmptyStatement", [p[1]],[],order='c')


def p_empty(p):
	'empty :'
	pass

def p_error(p):
	if (p == None):
		print "Object Declaration Error"
	else:
		print "Syntax Error at line " + str(p.lexer.lineno)
	#sys.exit("Syntax Error")
parser = yacc.yacc()

def allowed(type1, type2):
	if(type1=="DOUBLE" and (type2=="FLOAT" or type2 == "INT")):
		return True
	elif (type1=="FLOAT" and type2=="INT"):
		return True
	elif(type1==type2):
		return True
	elif(value(type1) and value(type2) and value(type1)>value(type2)):
		return True
	else:
		return False

def higher(type1, type2):
	if (type1 == "DOUBLE" and type2 == "DOUBLE"):
		return "DOUBLE"
	elif (type1 == "FLOAT" and type2 == "FLOAT"):
		return "FLOAT"
	elif((type1=="DOUBLE" and (type2=="FLOAT" or type2 == "INT")) or (type2=="DOUBLE" and (type1=="FLOAT" or type1 == "INT"))):
		return "DOUBLE"
	elif((type1=="FLOAT" and type2=="INT") or (type2=="FLOAT" and type1=="INT")):
		return "FLOAT"
	elif(value(type1) and value(type2) and value(type1)>=value(type2)):
		return type1
	elif(value(type1) and value(type2) and value(type2)>=value(type1)):
		return type2
	else:
		return False

def value(type):
	if(type == "BYTE"):
		return 1
	elif(type == "SHORT") :
		return 2
	elif(type=="INT") :
		return 3
	elif(type=="LONG") :
		return 3
	else :
		return 0


if __name__ == "__main__" :
	filename = sys.argv[1]
	# filename = "../tests/Good-8.scala"
	programfile = open(filename)
	data = programfile.read()
	parser.parse(data)
	import pickle
	pickle.dump(rootScope , open( "rootScope.p", "wb" ) )
	# global Error
	if(Error):
		print sys.exit("Your Program contain total " + str(Error) + " Errors"  )
	else:
		f = open('ThreeAddressCode.txt', 'w')  
		for stat in a3AC:
			f.write(stat + '\n')
		f.close()  
	graph.write_png('parsetree.png')
	filedot = open(filename + "dot",'w')
	filedot.write(graph.to_string())
	# print a3AC