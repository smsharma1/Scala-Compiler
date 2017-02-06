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
		for l in leaf:
			term = Node(l, [], [],True).name
			graph.add_edge(pydot.Edge(self.name, term))
		for ch in self.children:
			graph.add_edge(pydot.Edge(self.name, ch))
		self.leaf = leaf
		print leaf, " leaf"

def p_CompilationUnit(p):
	'''CompilationUnit : TopStatSeq 
	|	R_PACKAGE QualId semi CompilationUnit ''' 

def p_PackageObject(p):
	'PackageObject : R_PACKAGE R_OBJECT ObjectDef'

def p_Packaging(p):
	'''Packaging : R_PACKAGE QualId 
	| R_PACKAGE QualId n1 
	| Packaging TopStatSeq '''

def p_TopStat(p):
	'''TopStat : Import 
				| Packaging
				| PackageObject
			    | TopStat1 Modifier0more TmplDef
				| empty '''

def p_TopStat1(p):
	'''TopStat1 : empty
				| Anotation 
				| Annotation nl
				| TopStat1 Annotation 
				| TopStat1 Annotation nl'''

def p_Modifier0more(p):
	'''Modifier0more : empty 
				| Modifier0more Modifier'''

#look for semi
def p_TopStatSeq(p):
	'''TopStatSeq : semi TopStat 
				  | TopStat TopStatSeq'''

def p_SelfInvocation(p):
	'''SelfInvocation : R_THIS ArgumentExprs
					  | SelfInvocation ArgumentExprs'''

def p_ConstrBlock(p):
	'ConstrBlock : BLOCKOPEN SelfInvocation ConstrBlock1 BLOCKCLOSE '

def p_ConstrBlock1(p):
	'''ConstrBlock1 : empty 
					| semi BlockStat'''

def p_ConstrExpr(p):
	'''ConstrExpr : SelfInvocation 
				  | ConstrBlock'''

def p_EarlyDef(p):
	'EarlyDef : TopStat1 TopStat2 PatVarDef'

def p_EarlyDefs(p):
	'EarlyDefs : BLOCKOPEN EarlyDefs1 BLOCKCLOSE R_WITH'

def p_EarlyDefs1(p):
	'''EarlyDefs1 : empty 
				  | EarlyDef EarlyDefs2'''
		
def p_EarlyDefs2(p):
	'''EarlyDefs2 : empty 
				  | semi EarlyDef EarlyDefs2''' 

def p_Constr(p):
	'''Constr : AnnotType 
			  | AnnotType ArgumentExprs0more'''
	
def p_ArgumentExprs0more(p):
	'''ArgumentExprs0more : empty 
					   | ArgumentExprs0more ArgumentExprs'''
	
def p_TraitParents(p):
	'''TraitParents : AnnotType 
					| WithAnnotType0more'''

def p_WithAnnotType0more(p):
	'''WithAnnotType0more : empty
							| WithAnnotType0more R_WITH AnnotType'''

def p_ClassParents(p):
	'ClassParents : Constr WithAnnotType0more'

def p_TraitTemplate(p):
	'TraitTemplate : EarlyDefs01 TraitParents TemplateBody01'

def p_EarlyDefs01(p):
	'''EarlyDefs01 : empty 
					| EarlyDefs'''

def p_TemplateBody01(p):
	'''TemplateBody01 : empty 
						| TemplateBody'''

def p_ClassTemplate(p):
	'ClassTemplate : EarlyDefs01 ClassParents TemplateBody01'

def p_TraitTemplateOpt(p):
	'''TraitTemplateOpt : R_EXTENDS TraitTemplate
					 | Extends01TemplateBody01'''

def  p_Extends01TemplateBody01(p):
	'''Extends01TemplateBody01 : empty 
								| Extends01 TemplateBody'''

def p_Extends01(p):
	'''Extends01 : empty 
			  | Extends01 R_EXTENDS'''

def p_ClassTemplateOpt(p):
	''' ClassTemplateOpt : R_EXTENDS ClassTemplate
							| Extends01TemplateBody01'''

def p_ObjectDef(p):
	'ObjectDef : ID ClassTemplateOpt'

def p_TraitDef(p):
	'TraitDef : ID TypeParamClause01 TraitTemplateOpt'

def p_TypeParamClause01(p):
	'''TypeParamClause01 : empty
					| TypeParamClause'''

def p_ClassDef(p):
	'ClassDef : ID TypeParamClause01 ConstrAnnotation01 AccessModifier01 ClassParamClauses ClassTemplateOpt'

def p_AccessModifier01(p):
	'''AccessModifier01 : empty 
						|  AccessModifier'''

def p_ConstrAnnotation01(p):
	'''ConstrAnnotation01 : empty
							| ConstrAnnotation'''

def p_TmplDef(p):
	'''TmplDef : Case01 R_CLASS ClassDef
			| Case01 R_OBJECT ObjectDef
			| R_TRAIT TraitDef'''

def p_Case01(p):
	'''Case01 : empty 
				| R_CASE'''

def p_TypeDef(p):
	'TypeDef : ID TypeParamClause01 EQUALASS Type'

def p_FunDef(p):
	'''FunDef : FunSig ColonType01 EQUALASS Expr
			| FunSig nl01 BLOCKOPEN Block BLOCKCLOSE
			| R_THIS ParamClause ParamClauses EQUALASS ConstrExpr
			| R_THIS ParamClause ParamClauses nl01 ConstrBlock'''
def p_ColonType01(p):
	'''ColonType01 : empty 
				| COLON Type'''

#check for nl
def p_nl01(p):
	'''nl01 : empty 
			| nl'''

#check for ids 
def p_VarDef(p):
	'''VarDef : PatDef
			| ids COLON Type EQUALASS UNDERSCORE'''

def p_PatDef(p):
	'PatDef : Pattern2 CommaPattern20more ColonType01 EQUALASS Expr'

def  p_CommaPattern20more(p):
	'''CommaPattern20more : empty
						  | CommaPattern20more COMMA Pattern2'''
def p_Def(p):
	'''Def : ParVarDef
		| R_DEF FunDef
		| R_TYPE nl0more TypeDef
		| TmplDef'''

def p_nl0more(p):
	'''nl0more : empty
				| nl0more nl '''

def p_PatVarDef(p):
	'''PatVarDef : R_VAL PatDef
				| R_VAR VarDef'''
#check for id
def p_TypeDcl(p):
	'TypeDcl : id TypeParamClause01 Obscure2Type01 ObscureType01'

def p_Obscure2Type01(p):
	'''Obscure2Type01 : empty 
					| R_OBSCURE2 Type'''

def p_ObscureType01(p):
	'''ObscureType01 : empty 
					| R_OBSCURE Type'''

def p_FunSig(p):
	'FunSig : id FunTypeParamClause01 ParamClauses'

def p_FunTypeParamClause01(p):
	''' FunTypeParamClause01 : empty 
							| FunTypeParamClause'''
def p_FunDcl(p):
	'FunDcl : FunSig ColonType01'

def p_VarDcl(p):
	'VarDcl : ids COLON Type'

def p_ValDcl(p):
	'ValDcl : ids COLON Type'

def p_Dcl(p):
	'''Dcl : R_VAL ValDcl
		| R_VAR VarDcl
		| R_DEF FunDcl
		| R_TYPE nl0more TypeDcl'''

def p_ImportSelector(p):
	'ImportSelector : id ImpliesidorUnderscore01'

def p_ImpliesidorUnderscore01(p):
	'''ImpliesidorUnderscore01 : empty 
							 | 	R_IMPLIES1 id
							| R_IMPLIES1 UNDERSCORE'''

def p_ImportSelectors(p):
	'''ImportSelectors : BLOCKOPEN ImportselectorComma0more ImportSelector BLOCKCLOSE
					| BLOCKOPEN ImportselectorComma0more UNDERSCORE BLOCKCLOSE '''

def p_ImportselectorComma0more(p):
	'''ImportselectorComma0more : empty
							| ImportselectorComma0more ImportSelector COMMA'''
def p_ImportExpr(p):
	'''ImportExpr : StableId DOT id
				| StableId DOT UNDERSCORE
				| StableId DOT ImportSelectors'''

def p_Import(p):
	'Import : R_IMPORT ImportExpr CommaImportExpr0more'

def p_CommaImportExpr0more(p):
	'''CommaImportExpr0more : empty
						| CommaImportExpr0more COMMA ImportExpr'''

def p_SelfType(p):
	'''SelfType : id ColonType01 R_IMPLIES1
			| R_THIS COLON Type R_IMPLIES1'''

def p_TemplateStat(p):
	'''TemplateStat : TopStat1 Modifier0more Def
				| TopStat1 Modifier0more Dcl
				| Expr
				| empty'''

def p_TemplateBody(p):
	'TemplateBody : nl01 BLOCKOPEN SelfType01 TemplateStat semiTemplateStat0more BLOCKCLOSE'
 
def p_semiTemplateStat0more(p):
	'''semiTemplateStat0more : empty
							| semiTemplateStat0more semi TemplateStat'''
def p_SelfType01(p):
	'''SelfType01 : empty
					| SelfType'''

def p_NameValuePair(p):
	'NameValuePair : R_VAL id EQUALASS PrefixExpr'

def p_ConstrAnnotation(p):
	'ConstrAnnotation : R_ATTHERATE SimpleType ArgumentExprs'

def p_Annotation(p):
	'Annotation : R_ATTHERATE SimpleType ArgumentExprs0more'

def p_AccessQualifier(p):
	'''AccessQualifier : LSQRB id RSQRB
					| LSQRB R_THIS RSQRB'''

def p_AccessModifier(p):
	'''AccessModifier : R_PRIVATE AccessQualifier01
					| R_PROTECTED AccessQualifier01'''

def p_AccessQualifier01(p):
	'''AccessQualifier01 : empty
						| AccessQualifier'''

def p_LocalModifier(p):
	'''LocalModifier : R_ABSTRACT
					| R_FINAL
					| R_SEALED
					| R_IMPLICIT
					| R_LAZY'''

def p_Modifier(p):
	'''Modifier : LocalModifier
			| AccessModifier
			| R_OVERRIDE'''

def p_Binding(p):
	'''Binding : id ColonType01
			| UNDERSCORE ColonType01''' 

def p_Bindings(p):
	'Bindings : LPARAN Binding CommaBinding0more RPARAN' 

def p_CommaBinding0more(p):
	'''CommaBinding0more : empty
						| CommaBinding0more COMMA Binding''' 

def p_ClassParam(p):
	'ClassParam : Annotation0more Modifier0more valvar01 id  COLON ParamType EqualExpr01'

def p_Annotation0more(p):
	'''Annotation0more : empty
					| Annotation0more Annotation'''

def p_valvar01(p):
	'''valvar01 : empty
			| R_VAL
			| R_VAR'''

def p_EqualExpr01(p):
	'''EqualExpr01 : empty
				| EQUALASS Expr'''

def p_ClassParams(p):
	'ClassParams : ClassParam CommaClassParam0more'

def p_CommaClassParam0more(p):
	'''CommaClassParam0more : empty
						| CommaClassParam0more COMMA ClassParam'''

def p_ClassParamClause(p):
	'ClassParamClause : nl01 LPARAN ClassParams01 RPARAN'

def p_ClassParams01(p):
	'''ClassParams01 : empty
					| ClassParams '''

def p_ClassParamClauses(p):
	'ClassParamClauses : ClassParamClause0more Temp01'

def p_ClassParamClause0more(p):
	'''ClassParamClause0more : ClassParamClause0more ClassParamClause
								| empty'''

def p_Temp01(p):
	'''Temp01 : nl01 LPARAN R_IMPLICIT ClassParams RPARAN
			| empty'''

def p_ParamType(p):
	'''ParamType : Type
				| R_IMPLIES1 Type
				| Type MULASS'''

def p_Param(p):
	'Param : Annotation0more id ColonParamType01 EqualExpr01'

def p_ColonParamType01(p):
	'''ColonParamType01 : empty
					| COLON ParamType'''

def p_Params(p):
	'Params : Param CommaParam0more'

def p_CommaParam0more(p):
	'''CommaParam0more : empty
					| CommaParam0more COMMA Param'''

def p_ParamClause(p):
	'ParamClause : nl01 LPARAN Params01 RPARAN'

def p_Params01(p):
	'''Params01 : empty
			| Params'''

def p_ParamClauses(p):
	'ParamClauses : ParamClause0more Temp02'

def p_ParamClause0more(p):
	'''ParamClause0more : empty
					| ParamClause0more ParamClause'''

def p_Temp02(p):
	'''Temp02 : nl01 LPARAN R_IMPLICIT Params RPARAN
			| empty'''

def p_TypeParam(p): 
	'''TypeParam : id  TypeParamClause01  Obscure2Type01 ObscureType01 ObscureType0more ColonType0more	
				| UNDERSCORE TypeParamClause01  Obscure2Type01 ObscureType01 ObscureType0more ColonType0more'''

def p_ObscureType0more(p):
	'''ObscureType0more : empty
						| ObscureType0more R_OBSCURE Type'''

def p_ColonType0more(p):
	'''ColonType0more : empty
					| ColonType0more COLON Type'''

def p_VariantTypeParam(p):
	'''VariantTypeParam : Annotation0more TypeParam
					| Annotation0more PLUS TypeParam
					| Annotation0more MINUS TypeParam'''

def p_FunTypeParamClause(p):
	'FunTypeParamClause : LSQRB TypeParam CommaTypeParam0more RSQRB'

def p_CommaTypeParam0more(p):
	'''CommaParam0more : empty
					| CommaTypeParam0more COMMA TypeParam'''

def p_TypeParamClause(p):
	'TypeParamClause : LSQRB VariantTypeParam CommaVariantTypeParam0more RSQRB'

def p_CommaVariantTypeParam0more(p):
	'''CommaVariantTypeParam0more : empty
							| CommaVariantTypeParam0more COMMA VariantTypeParam''' 

#look reference there is ambiguity 
def p_Patterns(p):
	'Patterns : Pattern CommaPatterns01'

def p_CommaPatterns01(p):
	'''CommaPatterns01 : empty
					| COMMA Patterns'''

#look reference

def p_SimplePattern(p):
	'''SimplePattern : UNDERSCORE
					| varid
					| Literal
					| StableID
					| StableId LPARAN Patterns01 RPARAN
					| StableId LPARAN PatternsComma01 varidUnderscore01 UNDERSCORE MULTIPLICATION RPARAN
					| LPARAN Patterns01 RPARAN
					| XmlPattern'''
def p_Patterns01(p):
	'''Patterns01 : empty
				| Patterns'''

def p_PatternsComma01(p):
	'''PatternsComma01 : empty
				| Patterns COMMA'''

def p_varidUnderscore01(p):
	'''varidUnderscore01 : empty
				| varid  UNDERSCORE'''

def p_Pattern3(p):
	'''Pattern3 : SimplePattern
			| SimplePattern idnl01SimplePattern0more'''

def p_idnl01SimplePattern0more(p):
	'''idnl01SimplePattern0more : empty
				| idnl01SimplePattern0more id nl01 SimplePattern'''

def p_Pattern2(p):
	'''Pattern2 : varid AttheratePattern301
		| Pattern3'''

def p_AttheratePattern301(p):
	'''AttheratePattern301 : empty
				| ATTHERATE Pattern3''' 

def p_Pattern1(p):
	'''Pattern1 : varid COLON TypePat
				| UNDERSCORE COLON TypePat
				| Pattern2'''

def p_Pattern(p):
	'Pattern : Pattern1  BitorPattern10more'

def p_BitorPattern10more(p):
	'''BitorPattern10more : BitorPattern10more BITOR Pattern1
						| empty'''

def p_Guard(p):
	'Guard : R_IF PostfixExpr'

def p_CaseClause(p):
	'CaseClause : R_CASE Pattern Guard01 R_IMPLIES1 Block'

def p_Guard01(p):
	'''Guard01 : Guard
			| empty'''

def p_CaseClauses(p):
	'CaseClauses : CaseClause CaseClause0more'

def p_CaseClause0more(p):
	'''CaseClause0more : empty
					| CaseClause0more CaseClause'''

def p_Generator(p):
	'Generator : Pattern1 R_LEFTARROW1 Expr Guard01'

def p_Enumerator(p):
	'''Enumerator : Generator
				| Guard
				| Pattern1 EQUALASS Expr''' 

def p_Enumerators(p):
	'Enumerators ::= Generator semiEnumerator0more'

def p_semiEnumerator0more(p):
	'''semiEnumerator0more : empty
						| semiEnumerator0more semi Enumerator'''
def p_ResultExpr(p):
	'''ResultExpr : Expr1
				| Bindings R_IMPLIES1 Block
				| UNDERSCORE COLON CompoundType R_IMPLIES1 Block
				|  R_IMPLICIT id  COLON CompoundType R_IMPLIES1 Block
				| id  COLON CompoundType R_IMPLIES1 Block'''

#check Import	
def p_BlockStat(p):
	'''BlockStat : Import
				| Annotation0more  Def
				| Annotation0more R_IMPLICIT Def
				| Annotation0more  R_LAZY Def
				| Annotation0more LocalModifier0more TmplDef
				| Expr1
				| empty'''

def p_LocalModifier0more(p):
	'''LocalModifier0more : empty
						| LocalModifier0more LocalModifier'''

def p_Block(p):
	'Block : BlockStatsemi0more ResultExpr01'

def p_ResultExpr01(p):
	'''ResultExpr01 : empty	
					| ResultExpr'''

def p_BlockStatsemi0more(p):
	'''BlockStatsemi0more : BlockStatsemi0more BlockStat semi
							| empty'''

def p_BlockExpr(p):
	'''BlockExpr : BLOCKOPEN CaseClauses BLOCKCLOSE
				| BLOCKOPEN Block BLOCKCLOSE'''

def p_ArgumentExprs(p):
	'''ArgumentExprs : LPARAN Exprs RPARAN
					| LPARAN RPARAN
					| LPARAN ExprsComma01 PostfixExpr COLON UNDERSCORE MULTIPLICATION RPARAN
					| nl01 BlockExpr'''

def p_ExprsComma01(p):
	'''ExprsComma01 : empty
					| Exprs COMMA'''


def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_


def p_Ids(p):
        "Ids : ID "
        if(len(p) == 2):
                p[0] = Node("Ids", None, [p[1]] )
        else:
                p[0] = Node("Ids", [p[3]], [p[1],p[2]])


def p_QualId(p):
	'''QualId : ID 
		| ID DOT QualId'''
	print(p[0])
	if(len(p) == 2):
		p[0] = Node("QualId " , [], [p[1]] ).name
		print "in if"
	else:
		print p[3]
		p[0] = Node("QualId", [p[3]], [p[1],p[2]]).name
		print "in else"


def p_literals(p):
	'''literals : INT 
		| FLOAT 
		| STRING 
		| CHAR'''
	print("sharma")
	p[0] = Node("literals",None,[p[1]])
	return "literals"

# def p_CompilationUnit(p):
# 	'''CompilationUnit : TopStatSeq 
# 	|	R_PACKAGE QualId semi CompilationUnit ''' 
# 	if len(p) == 2:
# 		p[0] = Node(CompilationUnit,[p[1]],None)
# 	else:
# 		p[0] = Node(CompilationUnit,[p[2],p[3],p[4]],[p[1]])


# Build the parser

def p_Ids(p):
		"Ids : ID "
		if(len(p) == 2):
				p[0] = Node("Ids", [], [p[1]] )
		else:
				p[0] = Node("Ids", [p[3]], [p[1],p[2]])



# def p_Ids(p):
# 	'''Ids : ID 
# 	| ID COMMA Ids'''
# 	if(len(p) == 2):
# 		p[0] = Node("Ids", None, [p[1]] )
# 	else:
# 		p[0] = Node("Ids", [p[3]], [p[1],p[2]])

# def p_QualId(p):
# 	'''QualId : ID 
# 	| ID DOT QualId'''
# 	if(len(p) == 2):
# 		p[0] = Node("QualId", None, [p[1]] )
# 	else:
# 		p[0] = Node("QualId", [p[3]], [p[1],p[2]])	


# def p_Path(p):
# 	'''Path : StableId 
# 	| ID DOT R_THIS 
# 	| R_THIS'''
# 	if(len(p) == 2):
# 		if(p[1] == "this"):
# 			p[0] = Node("Path", None, [p[1]] )
# 		else:
# 			p[0] = Node("Path", [p[1]],None )
# 	else:
# 		p[0] = Node("Path",None,  [p[1],p[2],p[3]])

# def p_StableId(p):
# 	'''StableId :  ID 
# 	| Path DOT ID 
# 	| R_SUPER DOT ID 
# 	| ID DOT R_SUPER DOT ID '''
# 	# | ID DOT R_SUPER ClassQualifier DOT ID 
# 	# | R_SUPER ClassQualifier DOT ID'''
# 	if(len(p) == 2):
# 		p[0] = Node("StableId", None, p[1] )
# 	elif(len(p)==4):
# 		if(p[2] == "super"):
# 			p[0] = Node("StableId",None, [p[1], p[2], p[3]])
# 		else:
# 			p[0] = Node("StableId", [p[1]], [p[2],p[3]])
# 	elif(len(p)==5):
# 		p[0] = Node("StableId", [p[2]], [p[1],p[3], p[4]])
# 	elif(len(p)==6):
# 		p[0] = Node("StableId", None, [p[1], p[2], p[3], p[4], p[5]])
# 	else:
# 		p[0] = Node("StableId", [p[4]], [p[1], p[2], p[3], p[5], p[6]])




# Error rule for syntax errors
# def p_error(p):
# 	print("Syntax error in input!")


def p_empty(p):
    'empty :'
    pass
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
