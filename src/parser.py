# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

class Node:
	def __init__(self,type,children=None,leaf=None):
		 self.type = type
		 if children:
			  self.children = children
		 else:
			  self.children = [ ]
		 self.leaf = leaf

def p_literals(p):
	'''literals : INT | FLOAT | STRING | CHAR'''
	p[0] = p[1]

def p_QualId(p):
	'''QualId : ID | ID DOT QualId'''
	if(len(p) == 2):
		p[0] = Node("QualId", None, [p[1]] )
	else:
		p[0] = Node("QualId", [p[3]], [p[1],p[2]])

def p_Ids(p):
	'''Ids : ID | ID COMMA Ids'''
	if(len(p) == 2):
		p[0] = Node("Ids", None, [p[1]] )
	else:
		p[0] = Node("Ids", [p[3]], [p[1],p[2]])

def p_Path(p):
	'''Path : StableId | ID DOT THIS | THIS'''
	if(len(p) == 2):
		if(p[1] == "this"):
			p[0] = Node("Path", None, [p[1]] )
		else:
			p[0] = Node("Path", [p[1]],None )
	else:
		p[0] = Node("Path",None,  [p[1],p[2],p[3]])

def p_StableId(p):
	'''StableId :  ID | Path DOT ID | SUPER DOT ID | ID DOT SUPER DOT ID | ID DOT SUPER ClassQualifier DOT ID | SUPER ClassQualifier DOT ID'''
	if(len(p) == 2):
		p[0] = Node("StableId", None, p[1] )
	elif(len(p)==4):
		if(p[2] == "super"):
			p[0] = Node("StableId",None, [p[1], p[2], p[3]])
		else:
			p[0] = Node("StableId", [p[1]], [p[2],p[3]])
	elif(len(p)==5):
		p[0] = Node("StableId", [p[2]], [p[1],p[3], p[4]])
	elif(len(p)==6):
		p[0] = Node("StableId", None, [p[1], p[2], p[3], p[4], p[5]])
	else:
		p[0] = Node("StableId", [p[4]], [p[1], p[2], p[3], p[5], p[6]])


# def p_QualId(p):
# 	'''expression : ID | DOT expression'''
# 	if(len(p) == 2):
# 		p[0] = Node("QualId", None, p[1] )
# 	else:
# 		p[0] = Node("QualId", [p[1],[3]], p[2])

def p_expression_term(p):
	'expression : term'
	p[0] = p[1]

def p_term_times(p):
	'term : term TIMES factor'
	p[0] = p[1] * p[3]

def p_term_div(p):
	'term : term DIVIDE factor'
	p[0] = p[1] / p[3]

def p_term_factor(p):
	'term : factor'
	p[0] = p[1]

def p_factor_num(p):
	'factor : NUMBER'
	p[0] = p[1]

def p_factor_expr(p):
	'factor : LPAREN expression RPAREN'
	p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

data = '''+10-9><>=<=-5.8+-/%==!=&&||! /*while af sfsfaf asdfasf
fuckname af dfs fdadf af adf sf dasf
//sd fasf a asf jlasdlf lasdfalsfj ejf aljfljsdljsufnclajfje
if*/'''


while True:
   try:
	   s = raw_input('calc > ')
   except EOFError:
	   break
   if not s: continue
   result = parser.parse(s)
   print(result)