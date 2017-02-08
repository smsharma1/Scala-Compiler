# Yacc example

import ply.yacc as yacc
import pydot
# Get the token map from the lexer.  This is required.
from lexer import tokens
graph = pydot.Dot(graph_type='digraph')

class Node:
	uid=0
	def __init__(self,type,children,leaf,isChild=False):
		self.type = type
		Node.uid = Node.uid + 1
		self.uid = Node.uid
		self.name = type+" "+str(self.uid)
		if isChild:
			self.node = pydot.Node(self.name, style="filled", fillcolor="green")
		else:
			self.node = pydot.Node(self.name, style="filled", fillcolor="red")
		graph.add_node(self.node)
		print children, " children"
		self.children = children
		print leaf, " leaf"
		self.leaf = leaf
		for l in leaf:
			term = Node(l, [], [],True).name
			graph.add_edge(pydot.Edge(self.name, term))
		for ch in self.children:
			graph.add_edge(pydot.Edge(self.name, ch))

def p_CompilationUnit(p):
	'''CompilationUnit : ImportDeclarations ClassesObjects
						| ClassesObjects'''
	if len(p)==2:
		p[0] = Node("CompilationUnit", [p[1], p[2]],[]).name
	else:
		p[0] = Node("CompilationUnit", [p[1]],[]).name

#<import declarations> ::= <import declaration> | <import declarations> <import declaration>

def p_ImportDeclarations(p):
	'''	ImportDeclarations : ImportDeclaration 
							| ImportDeclarations ImportDeclaration'''
	if len(p)==2:
		p[0] = Node("ImportDeclarations", [p[1], p[2]],[]).name
	else:
		p[0] = Node("ImportDeclarations", [p[1]],[]).name

#<import declaration> ::= import <type name> ;

def p_ImportDeclaration(p):
	'ImportDeclaration : R_IMPORT TypeName SEMICOLON'
	p[0] = Node("ImportDeclaration", [p[2]],[p[1],p[3]]).name
	
#<classes_objects> ::= <class_object> | <class_object> <classes_objects>

def p_ClassesObjects(p):
	'''ClassesObjects : ClassObject 
						| ClassObject ClassesObjects'''
	if len(p)==2:
		p[0] = Node("ClassesObjects", [p[1], p[2]],[]).name
	else:
		p[0] = Node("ClassesObjects", [p[1]],[]).name
#<class_object> ::= <class_declaration> | <object_declaration> | ;
def p_ClassObject(p):
	'''ClassObject : ClassDeclaration 
				| ObjectDeclaration
				| SEMICOLON'''
	if "ClassDeclaration" in p[1]:
		p[0] = Node("ClassObject", [p[1]],[]).name
	elif "ObjectDeclaration" in p[1]:
		p[0] = Node("ClassObject", [p[1]],[]).name
	else:
		p[0] = Node("ClassObject", [],[p[1]]).name

#<object_declaration> ::= object <identifier> <super>? { method_body }
def p_ObjectDeclaration(p):
	'''ObjectDeclaration : R_OBJECT Identifier BLOCKOPEN MethodBody BLOCKCLOSE
						| R_OBJECT Identifier Super BLOCKOPEN MethodBody BLOCKCLOSE'''
	if len(p)==6:
		p[0] = Node("ObjectDeclaration", [p[2], p[3], p[5]],[p[1], p[4], p[6]]).name
	else:
		p[0] = Node("ObjectDeclaration", [p[2], p[4]],[p[1], p[3], p[5]]).name

#<class_declaration> ::= class <identifier> <class_header> <super>? { <class body declarations>? }

def p_ClassDeclaration(p):
	'''ClassDeclaration : R_CLASS Identifier ClassHeader BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
					 | R_CLASS Identifier ClassHeader Super BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
					 | R_CLASS Identifier ClassHeader BLOCKOPEN  BLOCKCLOSE
					 | R_CLASS Identifier ClassHeader Super BLOCKOPEN  BLOCKCLOSE'''
	if len(p)==8:
		p[0] = Node("ClassDeclaration", [p[2], p[3], p[4], p[6]],[p[1], p[5], p[7]]).name
	elif "Super" in p[4]:
		p[0] = Node("ClassDeclaration", [p[2], p[3], p[4]],[p[1], p[5], p[6]]).name
	elif len(p)==7:
		p[0] = Node("ClassDeclaration", [p[2], p[3], p[5]],[p[1], p[4], p[6]]).name
	else:
		p[0] = Node("ClassDeclaration", [p[2], p[3]],[p[1], p[4], p[5]]).name
#<super> ::= extends <class type>

def p_Super(p):
	'Super : R_EXTENDS ClassType'
	p[0] = Node("Super", [p[2]],[p[1]]).name
#<class_header> ::= ( <formal parameter list>? )
def p_ClassHeader(p):
	'''ClassHeader : LPARAN RPARAN
				| LPARAN FormalParameterList RPARAN'''
	if len(p)==3:
		p[0] = Node("ClassHeader", [],[p[1], p[2]]).name
	else:
		p[0] = Node("ClassHeader", [p[2]],[p[1], p[3]]).name

#<class body declarations> ::= <class body declaration> | <class body declarations> <class body declaration>
def p_ClassBodyDeclarations(p):
	'''ClassBodyDeclarations : ClassBodyDeclaration
							 | ClassBodyDeclarations ClassBodyDeclaration'''
	if len(p)==3:
		p[0] = Node("ClassBodyDeclarations", [p[1], p[2]],[]).name
	else:
		p[0] = Node("ClassBodyDeclarations", [p[1]],[]).name
#<class body declaration> ::= <field declaration> | <method declaration>
def p_ClassBodyDeclaration(p):
	'''ClassBodyDeclaration : FieldDeclaration
							| MethodDeclaration'''
	if "FieldDeclaration" in p[1]:
		p[0] = Node("ClassBodyDeclaration", [p[1]],[]).name
	else:
		p[0] = Node("ClassBodyDeclaration", [p[1]],[]).name

#<formal parameter list> ::= <formal parameter> | <formal parameter list> , <formal parameter>
def p_FormalParameterList(p):
	'''FormalParameterList : FormalParameter 
							| FormalParameterList COMMA FormalParameter'''
	if len(p)==2:
		p[0] = Node("FormalParameterList", [p[1]],[]).name
	else:
		p[0] = Node("FormalParameterList", [p[1], p[3]],[p[2]]).name
#<formal parameter> ::= <variable declarator id> : <type> 
def p_FormalParameter(p):
	'FormalParameter : Identifier COLON Type'
	p[0] = Node("FormalParamter", [p[1], p[3]],[p[2]]).name
#<class type> ::= <identifier> | with <identifier><class type>
#confusion check later
def p_ClassType(p):
	'''ClassType : Identifier 
				| R_WITH Identifier ClassType'''
	if len(p)==4:
		p[0] = Node("ClassType", [p[2], p[3]],[p[1]]).name
	else:
		p[0] = Node("ClassType", [p[1]],[]).name

#<field declaration> ::=  val <variable declarator> ;
def p_FieldDeclaration(p):
	'FieldDeclaration : R_VAL VariableDeclarator SEMICOLON'
	p[0] = Node("FieldDeclaration", [p[2]],[p[1], p[3]]).name
#<variable declarator> ::= <identifier> | <identifier>: <type>   | <identifier> <variable_declarator_extra>  
def p_VariableDeclarator(p):
	'''VariableDeclarator : Identifier 
						| Identifier COLON Type 
						| Identifier VariableDeclaratorExtra'''
	if len(p)==4:
		p[0] = Node("VariableDeclarator", [p[1], p[3]],[p[2]]).name
	elif len(p)==3:
		p[0] = Node("VariableDeclarator", [p[1], p[2]],[]).name
	else:
		p[0] = Node("VariableDeclarator", [p[1]],[]).name

#<variable_declarator_extra> ::= = <variable initializer> | :<type> = <variable initializer>
def p_VariableDeclaratorExtra(p):
	'''VariableDeclaratorExtra : EQUALASS VariableInitializer
							| COLON Type EQUALASS VariableInitializer''' 
	if len(p)==5:
		p[0] = Node("VariableDeclaratorExtra", [p[2], p[4]],[p[1], p[3]]).name
	else:
		p[0] = Node("VariableDeclaratorExtra", [p[2]],[p[1]]).name
#<variable initializer> ::= <expression> | <array initializer>
def p_VariableInitializer(p):
	'''VariableInitializer : Expression
						| ArrayInitializer'''
	if "Expression" in p[1]:
		p[0] = Node("VariableInitializer", [p[1]],[]).name
	else:
		p[0] = Node("VariableInitializer", [p[1]],[]).name

def p_ArrayInitializer(p):
    ''' ArrayInitializer : R_NEW R_ARRAY LSQRB Type RSQRB LPARAN INT RPARAN
							| R_NEW R_ARRAY LSQRB Type RSQRB LPARAN INT COMMA INT RPARAN'''
    if len(p) == 9:
		p[0] = Node('ArrayInitializer',[p[1],p[2],p[3],p[5],p[6],p[7],p[8]],[p[4]])
    else:
		p[0] = Node('ArrayInitializer',[p[1],p[2],p[3],p[5],p[6],p[7],p[8],p[9],p[10]],[p[4]])
#<method declaration> ::= <method header> <method body>
def p_MethodDeclaration(p):
	'MethodDeclaration : MethodHeader MethodBody'
	p[0] = Node("MethodDeclaration", [p[1], p[2]],[]).name
#<method header> ::= def <method declarator> : <type> = | def <method declarator> = 
def p_MethodHeader(p):
	'''MethodHeader : R_DEF MethodDeclarator COLON Type EQUALASS 
				| R_DEF MethodDeclarator EQUALASS'''
	if len(p)==6:
		p[0] = Node("MethodHeader", [p[2], p[4]],[p[1], p[3], p[5]]).name
	else:
		p[0] = Node("MethodHeader", [p[2]],[p[1],p[3]]).name
#<method declarator> ::= <identifier> ( <formal parameter list>? )
def p_MethodDeclarator(p):
	'''MethodDeclarator : Identifier LPARAN RPARAN
					| Identifier LPARAN FormalParameterList RPARAN'''
	if len(p)==4:
		p[0] = Node("MethodDeclarator", [p[1]],[p[2], p[3]]).name
	else:
		p[0] = Node("MethodDeclarator", [p[1], p[3]],[p[2], p[4]]).name

#<method body> ::= <block> | ;
def p_MethodBody(p):
	'''MethodBody : Block 
				| SEMICOLON'''
	if "Block" in p[1]:
		p[0] = Node("VariableInitializer", [p[1]],[]).name
	else:
		p[0] = Node("VariableInitializer", [],[p[1]]).name
#<type> ::= <primitive type> | <reference type>
def p_Type(p):
	'''Type : PrimitiveType 
		| ReferenceType'''
	if "PrimitiveType" in p[1]:
		p[0] = Node("Type", [p[1]],[]).name
	else:
		p[0] = Node("Type", [p[1]],[]).name
#<primitive type> ::= <numeric type> | boolean
def p_PrimitiveType(p):
	'''PrimitiveType : NumericType 
					| R_BOOLEAN'''
	if "NumericType" in p[1]:
		p[0] = Node("PrimitiveType", [p[1]],[]).name
	else:
		p[0] = Node("PrimitiveType", [p[1]],[]).name
#<numeric type> ::= <integral type> | <floating-point type>
def p_NumericType(p):
	'''NumericType : IntegralType
				| FloatingPointType'''
	if "IntegralType" in p[1]:
		p[0] = Node("Numeric Type", [p[1]],[]).name
	else:
		p[0] = Node("Numeric Type", [p[1]],[]).name

#<integral type> ::= byte | short | int | long | char

def p_IntegralType(p):
	'''IntegralType : R_BYTE
				 | R_SHORT
				 | R_INT
				 | R_LONG 
				 | R_CHAR'''
	p[0] = Node("IntegralType", [],[p[1]]).name

#<floating-point type> ::= float | double
def p_FloatingPointType(p):
	'''FloatingPointType : R_FLOAT 
						| R_DOUBLE'''
	p[0] = Node("FloatingPointType", [],[p[1]]).name
#<reference type> ::= <class type> | <array type>
def p_ReferenceType(p):
	'''ReferenceType : ClassType 
					| ArrayType'''
	p[0] = Node("ReferenceType", [p[1]],[]).name
#<class type> ::= <type name>
def p_ClassType(p):
	'ClassType : TypeName'
	p[0] = Node("ClassType", [p[1]],[]).name
#<array type> ::= <type> [ ]
def p_ArrayType(p):
	'ArrayType : Type LSQRB RSQRB'
	p[0] = Node("ArrayType", [p[1]],[p[2], p[3]]).name

#<block> ::= { <block statements>? }
def p_Block(p):
	'''Block : BLOCKOPEN BLOCKCLOSE
			| BLOCKOPEN BlockStatements BLOCKCLOSE'''
	if len(p)==3:
		p[0] = Node("Block", [],[p[1], p[2]]).name
	else:
		p[0] = Node("Block", [p[2]],[p[1], p[3]]).name
#<block statements> ::= <block statement> | <block statements> <block statement>
def p_BlockStatements(p):
	'''BlockStatements : BlockStatement 
					| BlockStatements BlockStatement'''
	if len(p)==2:
		p[0] = Node("BlockStatements", [p[1]],[]).name
	else:
		p[0] = Node("BlockStatements", [p[1],p[2]],[]).name				
#<block statement> ::= <local variable declaration statement> | <statement>
def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement 
					| Statement'''
	if "Statement" in p[1]:
		p[0] = Node("BlockStatement", [p[1]],[]).name
	else:
		p[0] = Node("BlockStatement", [p[1]],[]).name
#<local variable declaration statement> ::= <local variable declaration> ;
def p_LocalVariableDeclarationStatement(p):
	'LocalVariableDeclarationStatement : LocalVariableDeclaration'
	p[0] = Node("LocalVariableDeclarationStatement", [p[1]],[]).name	
#<local variable declaration> ::= <type> <variable declarators>
def p_LocalVariableDeclaration(p):
	'LocalVariableDeclaration : Type VariableDeclarator'
	p[0] = Node("LocalVariableDeclaration", [p[1],p[2]],[]).name	
#<statement> ::= <statement without trailing substatement> | <if then statement> | <if then else statement> 
# | <while statement> | <for statement>
def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
				| IfThenStatement
				| IfThenElseStatement
				| WhileStatement
				| ForStatement'''
	p[0] = Node("Statement", [p[1]],[]).name

#<statement without trailing substatement> ::= <block> | <empty statement> | <expression statement> 
# | <switch statement> | <break statement> | <continue statement> | <return statement>
def p_StatementWithoutTrailingSubstatement(p):
	'''StatementWithoutTrailingSubstatement : Block
										| EmptyStatement
										| ExpressionStatement
										| SwitchStatement
										| BreakStatement
										| ContinueStatement
										| ReturnStatement'''
	p[0] = Node("StatementWithoutTrailingSubstatement", [p[1]],[]).name

# <statement no short if> ::= <statement without trailing substatement> | <if then else statement no short if> 
# | <while statement no short if> | <for statement no short if>
def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
						| IfThenElseStatementNoShortIf'''
	p[0] = Node("StatementNoShortIf", [p[1]],[]).name

#<empty statement> ::= ;
def p_EmptyStatement(p):
	'EmptyStatement : SEMICOLON'
	p[0] = Node("EmptyStatement", [p[1]],[]).name

#<expression statement> ::= <statement expression> ;
def p_ExpressionStatement(p):
	'ExpressionStatement : StatementExpression SEMICOLON'
	p[0] = Node("ExpressionStatement", [p[1]],[]).name

#<statement expression> ::= <assignment> | <preincrement expression> 
# | <postincrement expression> | <predecrement expression> | <postdecrement expression> 
# | <method invocation> | <class instance creation expression>
def p_StatementExpression(p):
	'''StatementExpression : Assignment
						| PreincrementExpression
						| PostincrementExpression
						| PredecrementExpression
						| PostdecrementExpression
						| MethodInvocation
						| ClassInstanceCreationExpression'''
	p[0] = Node("StatementExpression", [p[1]],[]).name

def p_IfThenStatement(p):
	'IfThenStatement : R_IF LPARAN Expression RPARAN Statement'
	p[0] = Node("IfThenStatement", [p[3], p[5]],[p[1], p[2], p[4]]).name

def p_IfThenElseStatement(p):
	'IfThenElseStatement : R_IF LPARAN Expression RPARAN StatementNoShortIf R_ELSE Statement'
	p[0] = Node("IfThenElseStatement", [p[3], p[5], p[7]],[p[1], p[2], p[4], p[6]]).name

def p_IfThenElseStatementNoShortIf(p):
	'IfThenElseStatementNoShortIf : R_IF LPARAN Expression RPARAN StatementNoShortIf R_ELSE StatementNoShortIf'
	p[0] = Node("IfThenElseStatementNoShortIf", [p[3], p[5], p[7]],[p[1], p[2], p[4], p[6]]).name

def p_SwitchStatement(p):
	'SwitchStatement :  Expression  R_MATCH SwitchBlock'
	p[0] = Node("SwitchStatement", [p[1], p[3]],[p[2]]).name


def p_SwitchBlock(p):
	'''SwitchBlock : BLOCKOPEN SwitchBlockStatementGroups SwitchLabels BLOCKCLOSE
				| BLOCKOPEN  SwitchLabels BLOCKCLOSE
				| BLOCKOPEN SwitchBlockStatementGroups  BLOCKCLOSE
				| BLOCKOPEN   BLOCKCLOSE'''
	if len(p) ==  5:
		p[0] = Node("SwitchBlock", [p[2], p[3]],[p[1],p[4]]).name
	elif "SwitchLabels" in p[2]:
		p[0] = Node("SwitchBlock", [p[2]],[p[1],p[3]]).name
	elif "SwitchBlockStatementGroups" in p[2]:
		p[0] = Node("SwitchBlock", [p[2]],[p[1],p[3]]).name
	else:
		p[0] = Node("SwitchBlock", [], [p[1], p[2]])

def p_SwitchBlockStatementGroups(p):
	'''SwitchBlockStatementGroups : SwitchBlockStatementGroup
									 | SwitchBlockStatementGroups SwitchBlockStatementGroup'''
	if len(p) ==  3:
		p[0] = Node("SwitchBlockStatementGroups", [p[1], p[2]],[]).name
	else:
		p[0] = Node("SwitchBlockStatementGroups", [p[1]],[]).name

def p_SwitchBlockStatementGroup(p):
	'SwitchBlockStatementGroup : SwitchLabels BlockStatements'
	p[0] = Node("SwitchBlockStatementGroup", [p[1], p[2]],[]).name

def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabel 
					| SwitchLabels SwitchLabel'''
	if len(p) ==  3:
		p[0] = Node("SwitchLabels", [p[1], p[2]],[]).name
	else:
		p[0] = Node("SwitchLabels", [p[1]],[]).name

def p_SwitchLabel(p):
	'''SwitchLabel : R_CASE Expression COLON 
				| R_DEFAULT COLON'''
	if len(p) ==  3:
		p[0] = Node("SwitchLabel", [p[2]],[p[1], p[3]]).name
	else:
		p[0] = Node("SwitchLabel", [p[1], p[2]],[]).name

def p_WhileStatement(p):
	'WhileStatement :  R_WHILE  LPARAN Expression RPARAN Statement'
	p[0] = Node("WhileStatement", [p[3], p[5]],[p[1], p[2], p[4]]).name

def p_ForStatement(p): 
	'ForStatement : R_FOR BLOCKOPEN ForExprs ForIfCondition BLOCKCLOSE Statement'
	p[0] = Node("ForStatement", [p[3], p[4], p[6]],[p[1], p[2], p[5]]).name

def p_ForIfCondition(p): 
	'''ForIfCondition : IfVariables SEMICOLON ForIfCondition 
	 				| IfVariables'''
	if len(p) ==  3:
		p[0] = Node("ForIfCondition", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ForIfCondition", [p[1]],[]).name

def p_IfVariables(p):
	'IfVariables : R_IF Expression'
	p[0] = Node("ForIfCondition", [p[1]],[]).name

def p_ForExprs(p):
	'''ForExprs :  ForVariables SEMICOLON ForExprs 
			| ForVariables'''
	if len(p) ==  4:
		p[0] = Node("ForExprs", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ForExprs", [p[1]],[]).name

#''' for_variables : declaration_keyword_extras IDENTIFIER IN expression for_untilTo expression '''
def p_ForVariables(p): 
	'ForVariables : DeclarationKeywordExtras Identifier R_LEFTARROW1 Expression ForUntilTo Expression' 
	p[0] = Node("ForVariables", [p[3], p[4], p[5]], [p[1], p[2]]).name
 #'''declaration_keyword_extras : variable_header | empty'''	
#'''variable_header : K_VAL | K_VAR '''
def p_DeclarationKeywordExtras(p):
	'''DeclarationKeywordExtras : VariableHeader 
								| empty'''
	if 'VariableHeader' in p[1]:
		p[0] = Node('DeclarationKeywordExtras',[p[1]],[])

def p_VariableHeader(p):
	'''VariableHeader : R_VAL
					| R_VAR'''
	p[0] = Node('VariableHeader',[[p[1]]],[])
def p_ForUntilTo(p):
	'''ForUntilTo : R_UNTIL 
				| R_TO'''
	p[0] = Node("ForUntilTo", [],[p[1]]).name

def p_StatementExpressionList(p):
	'''StatementExpressionList : StatementExpression 
							| StatementExpressionList COMMA StatementExpression'''
	if len(p) ==  4:
		p[0] = Node("StatementExpressionList", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("StatementExpressionList", [p[1]],[]).name

def p_BreakStatement(p) :
	'''BreakStatement : R_BREAK Identifier SEMICOLON
					| R_BREAK SEMICOLON'''
	if len(p) ==  4:
		p[0] = Node("BreakStatement", [p[2]], [p[1]],[p[3]]).name
	else:
		p[0] = Node("BreakStatement", [],[p[1], p[2]]).name

def p_ContinueStatement(p):
	'''ContinueStatement : R_CONTINUE Identifier SEMICOLON
						| R_CONTINUE  SEMICOLON'''
	if len(p) ==  4:
		p[0] = Node("ContinueStatement", [p[2]], [p[1]],[p[3]]).name
	else:
		p[0] = Node("ContinueStatement", [],[p[1], p[2]]).name

def p_ReturnStatement(p):
	'''ReturnStatement : R_RETURN Expression SEMICOLON
					| R_RETURN SEMICOLON'''
	if len(p) ==  4:
		p[0] = Node("ReturnStatement", [p[2]], [p[1]],[p[3]]).name
	else:
		p[0] = Node("ReturnStatement", [],[p[1], p[2]]).name

def p_ConstantExpression(p):
	'ConstantExpression : Expression'
	p[0] = Node("ConstantExpression", [p[1]],[]).name

def p_Expression(p):
	'Expression : AssignmentExpression'
	p[0] = Node("Expression", [p[1]],[]).name

def p_AssignmentExpression(p):
	'''AssignmentExpression : ConditionalExpression 
						| Assignment'''
	p[0] = Node("AssignmentExpression", [p[1]],[]).name

def p_Assignment(p):
	'Assignment : LeftHandSide AssignmentOperator AssignmentExpression'
	p[0] = Node("Assignment", [p[1], p[2], p[3]],[]).name

def p_LeftHandSide(p):
	'''LeftHandSide : ExpressionName 
				| FieldAccess
				| ArrayAccess'''
	p[0] = Node("LeftHandSide", [p[1]],[]).name

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
	p[0] = Node("AssignmentOperator", [],[p[1]]).name

def p_ConditionalExpression(p):
	'''ConditionalExpression : ConditionalOrExpression 
							| ConditionalOrExpression QUESTION  Expression COLON ConditionalExpression'''
	if len(p) ==  6:
		p[0] = Node("ConditionalAndExpression", [p[1], p[3], p[5]], [p[2]],[p[4]]).name
	else:
		p[0] = Node("ConditionalAndExpression", [p[1]],[]).name

def p_ConditionalOrExpression(p):
	'''ConditionalOrExpression : ConditionalAndExpression 
							| ConditionalOrExpression OR ConditionalAndExpression'''
	if len(p) ==  4:
		p[0] = Node("ConditionalOrExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ConditionalOrExpression", [p[1]],[]).name

def p_ConditionalAndExpression(p) :
	'''ConditionalAndExpression : InclusiveOrExpression 
							| ConditionalAndExpression AND InclusiveOrExpression'''
	if len(p) ==  4:
		p[0] = Node("ConditionalAndExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ConditionalAndExpression", [p[1]],[]).name

def p_InclusiveOrExpression(p) :
	'''InclusiveOrExpression : ExclusiveOrExpression 
						| InclusiveOrExpression AND ExclusiveOrExpression'''
	p[0] = Node("InclusiveOrExpression", [p[1]],[]).name

def p_ExclusiveOrExpression(p):
	'''ExclusiveOrExpression : AndExpression 
							| ExclusiveOrExpression BITXOR AndExpression'''
	if len(p) ==  4:
		p[0] = Node("ExclusiveOrExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ExclusiveOrExpression", [p[1]],[]).name

def p_AndExpression(p):
	'''AndExpression : EqualityExpression 
					| AndExpression BITAND EqualityExpression'''
	if len(p) ==  4:
		p[0] = Node("AndExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("AndExpression", [p[1]],[]).name			

def p_EqualityExpression(p):
	'''EqualityExpression : RelationalExpression
						 | EqualityExpression AND RelationalExpression
						| EqualityExpression NOTEQUAL RelationalExpression'''
	if len(p) ==  4:
		p[0] = Node("EqualityExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("EqualityExpression", [p[1]],[]).name

def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression 
						| RelationalExpression LT ShiftExpression 
						| RelationalExpression GT ShiftExpression 
						| RelationalExpression LE ShiftExpression 
						| RelationalExpression GE ShiftExpression 
						| RelationalExpression R_INSTANCEOF ReferenceType'''
	if len(p) ==  4:
		p[0] = Node("RelationalExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("RelationalExpression", [p[1]],[]).name

def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression 
					| ShiftExpression BITLSHIFT AdditiveExpression 
					| ShiftExpression BITRSHIFT AdditiveExpression 
					| ShiftExpression BITRSFILL AdditiveExpression'''
	if len(p) ==  4:
		p[0] = Node("ShiftExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("ShiftExpression", [p[1]],[]).name

# <additive expression> ::= <multiplicative expression> | <additive expression> + <multiplicative expression> | <additive expression> - <multiplicative expression>
def p_AdditiveExpression(p):
	'''AdditiveExpression : MultiplicativeExpression
							| AdditiveExpression PLUS MultiplicativeExpression
							| AdditiveExpression MINUS MultiplicativeExpression'''
	if len(p) ==  4:
		p[0] = Node("AdditiveExpression", [p[1]],[p[3]], [p[2]]).name
	else:
		p[0] = Node("AdditiveExpression", [p[1]],[]).name

# <multiplicative expression> ::= <unary expression> | <multiplicative expression> * <unary expression> | <multiplicative expression> / <unary expression> | <multiplicative expression> % <unary expression>
def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : UnaryExpression
								| MultiplicativeExpression MULTIPLICATION UnaryExpression
								| MultiplicativeExpression DIVISION UnaryExpression
								| MultiplicativeExpression MODULUS UnaryExpression'''
	if len(p) ==  4:
		p[0] = Node("MultiplicativeExpression", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("MultiplicativeExpression", [p[1]],[]).name

# <cast expression> ::= ( <primitive type> ) <unary expression> | ( <reference type> ) <unary expression not plus minus>
def p_CastExpression(p):
	'''CastExpression : LPARAN PrimitiveType RPARAN UnaryExpression 
						| LPARAN ReferenceType RPARAN UnaryExpressionNotPlusMinus'''
	if len(p) ==  5:
		p[0] = Node("CastExpression", [p[2], p[4]], [p[1],p[3]]).name
	else:
		p[0] = Node("CastExpression", [p[2], p[3], p[5]],[p[1],p[4]]).name

# <unary expression> ::= <preincrement expression> | <predecrement expression> | + <unary expression> | - <unary expression> | <unary expression not plus minus>
def p_UnaryExpression(p):
	'''UnaryExpression : PreincrementExpression
						| PredecrementExpression
						| PLUS UnaryExpression
						| MINUS UnaryExpression
						| UnaryExpressionNotPlusMinus'''
	if len(p) ==  3:
		p[0] = Node("MultiplicativeExpression", [p[2]], [p[1]]).name
	else:
		p[0] = Node("MultiplicativeExpression", [p[1]],[]).name
# <predecrement expression> ::= -- <unary expression>
def p_PredecrementExpression(p):
	'PredecrementExpression : MINUS MINUS UnaryExpression'
	p[0] = Node("PredecrementExpression", [p[3]], [p[1], p[2]]).name
# <preincrement expression> ::= ++ <unary expression>
def p_PreincrementExpression(p):
	'PreincrementExpression : PLUS PLUS UnaryExpression'
	p[0] = Node("PreincrementExpression", [p[3]], [p[1], p[2]]).name
# <unary expression not plus minus> ::= <postfix expression> | ~ <unary expression> | ! <unary expression> | <cast expression>
def p_UnaryExpressionNotPlusMinus(p):
	'''UnaryExpressionNotPlusMinus : PostfixExpression
									| BITNEG UnaryExpression
									| NOT UnaryExpression
									| CastExpression'''
	if len(p) ==  3:
		p[0] = Node("UnaryExpressionNotPlusMinus", [p[2]], [p[1]]).name
	else:
		p[0] = Node("UnaryExpressionNotPlusMinus", [p[1]],[]).name

# <postdecrement expression> ::= <postfix expression> --
def p_PostdecrementExpression(p):
	'PostdecrementExpression : PostfixExpression'
	p[0] = Node("PostdecrementExpression", [p[1]],[]).name
# <postincrement expression> ::= <postfix expression> ++
def p_PostincrementExpression(p):
	'PostincrementExpression : PostfixExpression PLUS PLUS'
	p[0] = Node("PostincrementExpression", [p[1]],[p[2], p[3]]).name

# <postfix expression> ::= <primary> | <expression name> | <postincrement expression> | <postdecrement expression>
def p_PostfixExpression(p):
	'''PostfixExpression : Primary
							| ExpressionName
							| PostincrementExpression
							| PostdecrementExpression'''
	p[0] = Node("PostfixExpression", [p[1]],[]).name
# <method invocation> ::= <method name> ( <argument list>? ) | <primary> . <identifier> ( <argument list>? ) | super . <identifier> ( <argument list>? )
def p_MethodInvocation(p):
	'''MethodInvocation : MethodName LPARAN ArgumentList RPARAN
						| MethodName LPARAN RPARAN
						| Primary DOT Identifier LPARAN ArgumentList RPARAN
						| Primary DOT Identifier LPARAN RPARAN
						| Super DOT Identifier LPARAN ArgumentList RPARAN
						| Super DOT Identifier LPARAN RPARAN'''
	if len(p) ==  7:
		p[0] = Node("MethodInvocation", [p[1], p[3], p[5]], [p[2], p[4], p[6]]).name
	elif len(p) ==  6:
		p[0] = Node("MethodInvocation", [p[1], p[3]], [p[2], p[4], p[5]]).name
	if len(p) ==  5:
		p[0] = Node("MethodInvocation", [p[1], p[3]], [p[2], p[4]]).name
	else:
		p[0] = Node("MethodInvocation", [p[1]],[p[2], p[3]]).name
# <field access> ::= <primary> . <identifier> | super . <identifier>
def p_FieldAccess(p):
	'''FieldAccess : Primary DOT Identifier
					| Super DOT Identifier'''
	p[0] = Node('FieldAccess',[p[1],p[3]],[p[2]]).name

# <primary> ::= <primary no new array> | <array creation expression>
def p_Primary(p):
	'''Primary : PrimaryNoNewArray
				| ArrayCreationExpression'''
	p[0] = Node('Primary',[p[1]],[]).name

# <primary no new array> ::= <literal> | this | ( <expression> ) | <class instance creation expression> 
# | <field access> | <method invocation> | <array access>

def p_PrimaryNoNewArray(p):
	'''PrimaryNoNewArray : Literal
						| R_THIS
						| LPARAN Expression RPARAN
						| ClassInstanceCreationExpression
						| FieldAccess
						| MethodInvocation
						| ArrayAccess'''
	if len(p) == 3:
		p[0] = Node('PrimaryNoNewArray',[p[2]],[p[1],p[3]]).name
	elif 'this' in p[1] :
		p[0] = Node('PrimaryNoNewArray',[ ],[p[1]]).name
	else:
		p[0] = Node('PrimaryNoNewArray',[p[1]],[]).name
# <class instance creation expression> ::= new <class type> ( <argument list>? )

def p_ClassInstanceCreationExpression(p):
	'''ClassInstanceCreationExpression : R_NEW ClassType LPARAN ArgumentList RPARAN
										| R_NEW ClassType LPARAN RPARAN'''
	if len(p) ==6:
		p[0] = Node('ClassInstanceCreationExpression',[p[2],p[4]],[p[1],p[3],p[5]]).name
	else:
		p[0] = Node('ClassInstanceCreationExpression',[p[2]],[p[1],p[3],p[4]]).name

# <argument list> ::= <expression> | <argument list> , <expression>
def p_ArgumentList(p):
	'''ArgumentList : Expression
					| ArgumentList COMMA Expression'''
	if len(p) == 2:
		p[0] = Node('ArgumentList',[p[1]],[]).name
	else :
		p[0] = Node('ArgumentList',[p[1],p[3]],[p[2]]).name

# <array creation expression> ::= new <primitive type> <dim exprs> <dims>? | new <class or interface type> <dim exprs> <dims>?
def p_ArrayCreationExpression(p):
	'''ArrayCreationExpression : R_NEW PrimitiveType DimExprs
								| R_NEW PrimitiveType DimExprs Dims
								| R_NEW ClassType DimExprs
								| R_NEW ClassType DimExprs Dims'''
	if len(p) == 4:
		p[0] = Node('ArrayCreationExpression',[p[2],p[3]],p[0]).name
	else :
		p[0] = Node('ArrayCreationExpression',[p[2],p[3],p[4]],p[0]).name
# <dim exprs> ::= <dim expr> | <dim exprs> <dim expr>
def p_DimExprs(p):
	'''DimExprs : DimExpr
				| DimExprs DimExpr'''
	if len(p) ==2:
		p[0] = Node('DimExprs',[p[1]],[]).name
	else :
		p[0] = Node('DimExprs',[p[1],p[2]],[]).name

# <dim expr> ::= [ <expression> ]
def p_DimExpr(p):
	'''DimExpr : LSQRB Expression RSQRB'''
	p[0] = Node('DimExpr',[p[2]],[p[1],p[3]]).name

# <dims> ::= [ ] | <dims> [ ]
def p_Dims(p):
	'''Dims : LSQRB RSQRB
			| Dims LSQRB RSQRB'''
	if len(p) == 3 :
		p[0] = Node('Dims',[],[p[1],p[2]]).name
	else:
		p[0] = Node('Dims',[p[2]],[p[1],p[3]]).name

# <array access> ::= <expression name> [ <expression> ] | <primary no new array> [ <expression>]
def p_ArrayAccess(p):
	'''ArrayAccess : ExpressionName LSQRB Expression RSQRB
					| PrimaryNoNewArray LSQRB Expression RSQRB'''
	p[0] = Node('ArrayAccess',[p[1],p[3]],[p[2],p[4]]).name



# <package name> ::= <identifier> | <package name> . <identifier>
def p_PackageName(p):
	'''PackageName : Identifier
					| PackageName DOT Identifier'''
	if len(p)==2:
		p[0] = Node('PackageName',[p[1]],[]).name
	else:
		p[0] = Node('PackageName',[p[1],p[3]],[p[2]]).name


# <type name> ::= <identifier> | <package name> . <identifier>
def p_TypeName(p):
	'''TypeName : Identifier 
				| PackageName DOT Identifier'''
	if len(p)==2:
		p[0] = Node('TypeName',[p[1]],[]).name
	else:
		p[0] = Node('TypeName',[p[1],p[3]],[p[2]]).name


# <simple type name> ::= <identifier>
def p_SimpleTypeName(p):
	'SimpleTypeName : Identifier'
	p[0] = Node('SimpleTypeName',[p[1]],[]).name


# <expression name> ::= <identifier> | <ambiguous name> . <identifier>
def p_ExpressionName(p):
	'''ExpressionName : Identifier
						| AmbiguousName DOT Identifier'''
	if len(p)==2:
		p[0] = Node('ExpressionName',[p[1]],[]).name
	else:
		p[0] = Node('ExpressionName',[p[1],p[3]],[p[2]]).name


# <method name> ::= <identifier> | <ambiguous name>. <identifier>
def p_MethodName(p):
	'''MethodName : Identifier 
					| AmbiguousName DOT Identifier'''
	if len(p)==2:
		p[0] = Node('MethodName',[p[1]],[]).name
	else:
		p[0] = Node('MethodName',[p[1],p[3]],[p[2]]).name


# <ambiguous name>::= <identifier> | <ambiguous name>. <identifier>
def p_AmbiguousName(p):
	'''AmbiguousName : Identifier 
					| AmbiguousName DOT Identifier'''
	if len(p)==2:
		p[0] = Node('AmbiguousName',[p[1]],[]).name
	else:
		p[0] = Node('AmbiguousName',[p[1],p[3]],[p[2]]).name

# <literal> ::= <integer literal> | <floating-point literal> | <boolean literal> | <character literal> | <string literal> | <null literal>
def p_Literal(p):
	'''Literal : IntegerLiteral
				| FloatingPointLiteral
				| BooleanLiteral
				| CharacterLiteral
				| StringLiteral
				| NullLiteral'''

	p[0] = Node("Literal", [p[1]],[]).name
# <integer literal> ::= <decimal integer literal> | <hex integer literal> | <octal integer literal>

def p_BooleanLiteral(p):
	'BooleanLiteral : BOOL'
	p[0] = Node('BooleanLiteral',[],[p[1]]).name

def p_IntegerLiteral(p):
	 'IntegerLiteral : INT'
	 p[0] = Node('IntegerLiteral',[],[p[1]]).name

def p_FloatingPointLiteral(p):
	'FloatingPointLiteral : FLOAT'
	p[0] = Node('FloatingPointLiteral',[],[p[1]]).name

def p_CharacterLiteral(p):
	'CharacterLiteral : CHAR'
	p[0] = Node('CharacterLiteral',[],[p[1]]).name

def p_StringLiteral(p):
	'StringLiteral : STRING'
	p[0] = Node('StringLiteral',[],[p[1]]).name

# <decimal numeral> ::= 0 | <non zero digit> <digits>?
def p_DecimalNumeral(p):
	'''DecimalNumeral : ZERO 
					| NONZERODIGIT 
					| NONZERODIGIT DIGITS'''

def p_DIGITS(p):
	'''DIGITS : DIGIT 
			| DIGITS DIGIT'''


def p_HexNumeral(p):
	'''HexNumeral : ZERO X_SMALL HEXDIGIT 
					| ZERO X_BIG HEXDIGIT 
					| HexNumeral HEXDIGIT'''



# <octal numeral> ::= 0 <octal digit> | <octal numeral> <octal digit>




# <floating-point literal> ::= <digits> . <digits>? <exponent part>? <float type suffix>?
# def FloatingPointLiteral(p):
# 	'''FloatingPointLiteral : Digits Dot
# 							| Digits Dot FloatTypeSuffix
# 							| Digits Dot ExponentPart
# 							| Digits Dot ExponentPart FloatTypeSuffix
# 							| Digits Dot Digits
# 							| Digits Dot Digits FloatTypeSuffix
# 							| Digits Dot Digits ExponentPart
# 							| Digits Dot Digits ExponentPart FloatTypeSuffix'''

# <digits> <exponent part>? <float type suffix>?
#doubtful

# <exponent part> ::= <exponent indicator> <signed integer>
#  def ExponentPart(p):
#  	'''ExponentPart(p) : ExponentIndicator 
#  						| SignedInteger'''

# <exponent indicator> ::= e | E
#define in lexer
# <signed integer> ::= <sign>? <digits>
# def SignedInteger(p):
# 	'''SignedInteger : Sign digits
# 					| digits'''


# <sign> ::= + | -

# <float type suffix> ::= f | F | d | D
#define in lexer
# # <boolean literal> ::= true | false
# # def BooleanLiteral(p):
# # 	'''BooleanLiteral : true 
# # 						| false'''

# # <character literal> ::= ' <single character> ' | ' <escape sequence> '
# # def CharacterLiteral(p):
# # 	'''CharacterLiteral : SingleCharacter
# # 						| EscapeSequence'''


# # <single character> ::= <input character> except ' and \
# # #define InputChar in lexer
# # def SingleCharacter(p):
# # 	'SingleCharacter : InputChar'
# # <string literal> ::= " <string characters>?"
# # def StringLiteral(p):
# # 	'StringLiteral : StringCharacters'

# # # <string characters> ::= <string character> | <string characters> <string character>
# # def StringCharacters(p):
# # 	'''StringCharacters: StringCharacter
# # 						| StringCharacters StringCharacter'''

# # <string character> ::= <input character> except " and \ | <escape character>
# # #define string char in lexer
# # def StringCharacter(p):
# # 	'StringCharacter : StrChar'
def p_empty(p):
    'empty :'
    pass

# # # <null literal> ::= null
def p_NullLiteral(p):
	'NullLiteral : R_NULL'
	p[0] = Node("NullLiteral", [],[p[1]]).name

def p_Identifier(p):
	'Identifier : ID'
	p[0] = Node("Identifier", [],[p[1]]).name
parser = yacc.yacc()

while True:
	try:
		s = raw_input('calc > ')
	except EOFError:
		break
	if not s: continue
	parser.parse(s)
	graph.write_png('parsetree.png')
	graph.to_string()
	print(graph.to_string())
