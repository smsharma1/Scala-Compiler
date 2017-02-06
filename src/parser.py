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

def p_QualId(p):
	'''QualId : ID 
		| ID DOT QualId'''
	print "p[0] : ",p[0]
	if(len(p) == 2):
		p[0] = Node("QualId" , [], [p[1]] ).name
		print "in if"
	else:
		print p[3]
		p[0] = Node("QualId", [p[3]], [p[2], p[1]]).name
		print "in else"

def p_CompilationUnit(p):
	'''CompilationUnit : TopStatSeq 
	|	R_PACKAGE QualId semi CompilationUnit ''' 
	if len(p)==2:
		p[0] = Node("CompilationUnit", [p[1]],[]).name
	else:
		p[0] = Node("CompilationUnit", [p[2],p[3],p[4]],[p[1]]).name

def p_PackageObject(p):
	'PackageObject : R_PACKAGE R_OBJECT ObjectDef'
	p[0] = Node("PackageObject", [p[3]],[p[2],p[1]]).name

def p_Packaging(p):
	'''Packaging : R_PACKAGE QualId 
	| R_PACKAGE QualId n1 
	| Packaging TopStatSeq '''
	if len(p)==4:
		p[0] = Node("Packaging", [p[2],p[3]],[p[1]]).name
	elif p[1] == "package":
		p[0] = Node("Packaging", [p[2]], [p[1]]).name
	else:
		p[0] = Node("Packaging", [p[1],p[2]],[]).name

def p_TopStat(p):
	'''TopStat : Import 
				| Packaging
				| PackageObject
			    | TopStat1 TopStat2 TmplDef
				| empty '''
	if len(p)==4:
		p[0] = Node("TopStat", [p[2],p[3],p[4]],[]).name
	elif "Import" in p[1]:
		p[0] = Node("TopStat", [p[1]], []).name
	elif "Packaging" in p[1]:
		p[0] = Node("TopStat", [p[1]], []).name
	elif "PackageObject" in p[1]:
		p[0] = Node("TopStat", [p[1]],[]).name
	else:
		p[0] = Node("TopStat", [p[1]],[]).name
	
def p_TopStat1(p):
	'''TopStat1 : empty
				| Annotation 
				| Annotation nl
				| TopStat1 Annotation 
				| TopStat1 Annotation nl'''
	if len(p)==4:
		p[0] = Node("TopStat1", [p[1],p[2],p[3]],[]).name
	elif "TopStat1" in p[1]:
		p[0] = Node("TopStat1", [p[1], p[2]], []).name
	elif "nl" in p[2]:
		p[0] = Node("TopStat1", [p[1], p[2]], []).name
	elif "Annotation" in p[1]:
		p[0] = Node("TopStat1", [p[1]],[]).name
	else :
		p[0] = Node("TopStat1", [p[1]],[]).name

def p_Modifier0more(p):
	'''Modifier0more : empty 
				| Modifier0more Modifier'''
	if len(p)==3:
		p[0] = Node("Modifier0more", [p[2],p[3]],[]).name
	elif "Import" in p[1]:
		p[0] = Node("Modifier0more", [p[1]], []).name
	else:
		p[0] = Node("Modifier0more", [p[1]],[]).name

#look for semi
def p_TopStatSeq(p):
	'''TopStatSeq : semi TopStat 
				  | TopStat TopStatSeq'''
	if "TopStat" in p[1]:
		p[0] = Node("TopStatSeq", [p[1],p[2]],[]).name
	else:
		p[0] = Node("TopStatSeq", [p[1],p[2]],[]).name

def p_SelfInvocation(p):
	'''SelfInvocation : R_THIS ArgumentExprs
					  | SelfInvocation ArgumentExprs'''
	if "this" in p[1]:
		p[0] = Node("SelfInvocation", [p[2]],[p[1]]).name
	else:
		p[0] = Node("SelfInvocation", [p[1],p[2]],[]).name

def p_ConstrBlock(p):
	'ConstrBlock : BLOCKOPEN SelfInvocation ConstrBlock1 BLOCKCLOSE '
	p[0] = Node("ConstrBlock", [p[2],p[3]],[p[1],p[4]]).name

def p_ConstrBlock1(p):
	'''ConstrBlock1 : empty 
					| semi BlockStat'''
	if "semi" in p[1]:
		p[0] = Node("ConstrBlock1", [p[1],p[2]], []).name
	else:
		p[0] = Node("ConstrBlock1", [p[1],p[2]],[]).name

def p_ConstrExpr(p):
	'''ConstrExpr : SelfInvocation 
				  | ConstrBlock'''
	if "ConstrBlock" in p[1]:
		p[0] = Node("ConstrExpr", [p[1]], []).name
	else:
		p[0] = Node("ConstrExpr", [p[1]],[]).name

def p_EarlyDef(p):
	'EarlyDef : TopStat1 TopStat2 PatVarDef'
	p[0] = Node("EarlyDef", [p[1], p[2], p[3]],[]).name

def p_EarlyDefs(p):
	'EarlyDefs : BLOCKOPEN EarlyDefs1 BLOCKCLOSE R_WITH'
	p[0] = Node("EarlyDefs", [p[2]], [p[1], p[3], p[4]]).name

def p_EarlyDefs1(p):
	'''EarlyDefs1 : empty 
				  | EarlyDef EarlyDefs2'''
	if "EarlyDef" in p[1]:
		p[0] = Node("EarlyDefs1", [p[1], p[2]], []).name
	else:
		p[0] = Node("EarlyDefs1", [p[1]],[]).name
		
def p_EarlyDefs2(p):
	'''EarlyDefs2 : empty 
				  | semi EarlyDef EarlyDefs2'''
	if "semi" in p[1]:
		p[0] = Node("EarlyDefs2", [p[1], p[2], p[3]], []).name
	else:
		p[0] = Node("EarlyDefs2", [p[1]],[]).name

def p_Constr(p):
	'''Constr : AnnotType 
			  | AnnotType ArgumentExprs0more'''
	if len(p)==3:
		p[0] = Node("Constr", [p[1], p[2]], []).name
	else:
		p[0] = Node("Constr", [p[1]],[]).name
	
def p_ArgumentExprs0more(p):
	'''ArgumentExprs0more : empty 
					   | ArgumentExprs0more ArgumentExprs'''
	if len(p)==3:
		p[0] = Node("ArgumentExprs0more", [p[1], p[2]], []).name
	else:
		p[0] = Node("ArgumentExprs0more", [p[1]],[]).name
	
def p_TraitParents(p):
	'''TraitParents : AnnotType 
					| WithAnnotType0more'''
	if "WithAnnotType0more" in p[1]:
		p[0] = Node("TraitParents", [p[1]], []).name
	else:
		p[0] = Node("TraitParents", [p[1]],[]).name

def p_WithAnnotType0more(p):
	'''WithAnnotType0more : empty
							| WithAnnotType0more R_WITH AnnotType'''
	if "WithAnnotType0more" in p[1]:
		p[0] = Node("WithAnnotType0more", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("WithAnnotType0more", [p[1]],[]).name

def p_ClassParents(p):
	'ClassParents : Constr WithAnnotType0more'
	p[0] = Node("ClassParents", [p[1], p[2]], []).name

def p_TraitTemplate(p):
	'TraitTemplate : EarlyDefs01 TraitParents TemplateBody01'
	p[0] = Node("TraitTemplate", [p[1], p[2], p[3]], []).name

def p_EarlyDefs01(p):
	'''EarlyDefs01 : empty 
					| EarlyDefs'''
	p[0] = Node("EarlyDefs01", [p[1]], []).name

def p_TemplateBody01(p):
	'''TemplateBody01 : empty 
						| TemplateBody'''
	p[0] = Node("TemplateBody01", [p[1]], []).name

def p_ClassTemplate(p):
	'ClassTemplate : EarlyDefs01 ClassParents TemplateBody01'
	p[0] = Node("ClassTemplate", [p[1], p[2], p[3]], []).name

def p_TraitTemplateOpt(p):
	'''TraitTemplateOpt : R_EXTENDS TraitTemplate
					 | Extends01TemplateBody01'''
	if len(p)==2
		p[0] = Node("TraitTemplateOpt", [p[2]], [p[1]]).name
	else:
		p[0] = Node("TraitTemplateOpt", [p[1]],[]).name

def  p_Extends01TemplateBody01(p):
	'''Extends01TemplateBody01 : empty 
								| Extends01 TemplateBody'''
	if len(p)==2:
		p[0] = Node("Extends01TemplateBody01", [p[1], p[2]], []).name
	else:
		p[0] = Node("Extends01TemplateBody01", [p[1]],[]).name

def p_Extends01(p):
	'''Extends01 : empty 
			  | Extends01 R_EXTENDS'''
	if len(p)==2:
		p[0] = Node("Extends01", [p[1]], [p[2]]).name
	else:
		p[0] = Node("Extends01", [p[1]],[]).name

def p_ClassTemplateOpt(p):
	''' ClassTemplateOpt : R_EXTENDS ClassTemplate
							| Extends01TemplateBody01'''
	if len(p)==2:
		p[0] = Node("ClassTemplateOpt", [p[2]], [p[1]]).name
	else:
		p[0] = Node("ClassTemplateOpt", [p[1]],[]).name

def p_ObjectDef(p):
	'ObjectDef : ID ClassTemplateOpt'
	p[0] = Node("ObjectDef", [p[2]], [p[1]]).name

def p_TraitDef(p):
	'TraitDef : ID TypeParamClause01 TraitTemplateOpt'
	p[0] = Node("TraitDef", [p[2], p[3]], [p[1]]).name

def p_TypeParamClause01(p):
	'''TypeParamClause01 : empty
					| TypeParamClause'''
	p[0] = Node("TypeParamClause01", [p[1]], []).name

def p_ClassDef(p):
	'ClassDef : ID TypeParamClause01 ConstrAnnotation01 AccessModifier01 ClassParamClauses ClassTemplateOpt'
	p[0] = Node("ClassDef", [p[2], p[3], p[4], p[5], p[5]], [p[1]]).name

def p_AccessModifier01(p):
	'''AccessModifier01 : empty 
						|  AccessModifier'''
	p[0] = Node("AccessModifier01", [p[1]], []).name

def p_ConstrAnnotation01(p):
	'''ConstrAnnotation01 : empty
							| ConstrAnnotation'''
	p[0] = Node("ConstrAnnotation01", [p[1]], []).name

def p_TmplDef(p):
	'''TmplDef : Case01 R_CLASS ClassDef
			| Case01 R_OBJECT ObjectDef
			| R_TRAIT TraitDef'''
	if "ClassDef" in p[3]:
		p[0] = Node("TmplDef", [p[1], p[3]], [p[2]]).name
	if "ObjectDef" in p[3]:
		p[0] = Node("TmplDef", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("TmplDef", [p[2]],[p[1]]).name

def p_Case01(p):
	'''Case01 : empty 
				| R_CASE'''
	if p[1] == "case":
		p[0] = Node("Case01", [], [p[1]]).name
	else:
		p[0] = Node("Case01", [p[1]], []).name

def p_TypeDef(p):
	'TypeDef : ID TypeParamClause01 EQUALASS Type'
	p[0] = Node("TypeDef", [p[2], p[4]], [p[1], p[3]]).name


def p_FunDef(p):
	'''FunDef : FunSig ColonType01 EQUALASS Expr
			| FunSig nl01 BLOCKOPEN Block BLOCKCLOSE
			| R_THIS ParamClause ParamClauses EQUALASS ConstrExpr
			| R_THIS ParamClause ParamClauses nl01 ConstrBlock'''
	if "ColonType01" in p[2]:
		p[0] = Node("FunDef", [p[1], p[2], p[4]], [p[3]]).name
	if "nl01" in p[2]:
		p[0] = Node("FunDef", [p[1], p[2], p[4]], [p[3], p[5]]).name
	if "nl01" in p[4]:
		p[0] = Node("FunDef", [p[2], p[3], p[4], p[5]], [p[1]]).name
	else:
		p[0] = Node("FunDef", [p[2], p[3], p[5]], [p[1], p[4]]).name

def p_ColonType01(p):
	'''ColonType01 : empty 
				| COLON Type'''
	if len(p):
		p[0] = Node("Case01", [], [p[1]]).name
	else:
		p[0] = Node("Case01", [p[1]], []).name
	
#check for nl
def p_nl01(p):
	'''nl01 : empty 
			| nl'''
	if "nl" in p[1]:
		p[0] = Node("nl01", [p[1]], []).name
	else:
		p[0] = Node("nl01", [], [p[1]]).name

#check for ids 
def p_VarDef(p):
	'''VarDef : PatDef
			| ids COLON Type EQUALASS UNDERSCORE'''
	if "Patdef" in p[1]:
		p[0] = Node("Vardef", [p[1]], []).name
	else:
		p[0] = Node("Vardef", [p[1], p[3]], [p[2], p[4], p[5]]).name

def p_PatDef(p):
	'PatDef : Pattern2 CommaPattern20more ColonType01 EQUALASS Expr'
	p[0] = Node("Patdef", [p[1], p[2], p[3], p[5]], [p[4]]).name

def  p_CommaPattern20more(p):
	'''CommaPattern20more : empty
						  | CommaPattern20more COMMA Pattern2'''
	if "CommaPatter20more" in p[1]:
		p[0] = Node("CommaPatter20more", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("CommaPatter20more", [p[1]], []).name

def p_Def(p):
	'''Def : ParVarDef
		| R_DEF FunDef
		| R_TYPE nl0more TypeDef
		| TmplDef'''
	if len(p)==4:
		p[0] = Node("Def", [p[2],p[3]],[p[1]]).name
	elif len(p)==3:
		p[0] = Node("Def", [p[2]], [p[1]]).name
	elif "ParVarDef" in p[1]:
		p[0] = Node("Def", [p[1]], []).name
	else
		p[0] = Node("Def", [p[1]],[]).name

def p_nl0more(p):
	'''nl0more : empty
				| nl0more nl '''
	if "nl0more" in p[1]:
		p[0] = Node("nl0more", [p[1], p[2]], []).name
	else:
		p[0] = Node("nl0more", [p[1]], []).name

def p_PatVarDef(p):
	'''PatVarDef : R_VAL PatDef
				| R_VAR VarDef'''
	if "PatDef" in p[2]:
		p[0] = Node("PatVarDef", [p[2]], [p[1]]).name
	else:
		p[0] = Node("PatVarDef", [p[2]], [p[1]]).name
#check for id
def p_TypeDcl(p):
	'TypeDcl : id TypeParamClause01 Obscure2Type01 ObscureType01'
	p[0] = Node("TypeDcl", [p[1], p[2], p[3], p[4]], []).name


def p_Obscure2Type01(p):
	'''Obscure2Type01 : empty 
					| R_OBSCURE2 Type'''
	if "Type" in p[2]:
		p[0] = Node("Obscure2Type01", [p[2]], [p[1]]).name
	else:
		p[0] = Node("Obscure2Type01", [p[1]], []).name

def p_ObscureType01(p):
	'''ObscureType01 : empty 
					| R_OBSCURE Type'''
	if "Type" in p[2]:
		p[0] = Node("ObscureType01", [p[2]], [p[1]]).name
	else:
		p[0] = Node("ObscureType01", [p[1]], []).name

def p_FunSig(p):
	'FunSig : id FunTypeParamClause01 ParamClauses'
	p[0] = Node("FunSig", [p[1], p[2], p[3]], []).name

def p_FunTypeParamClause01(p):
	''' FunTypeParamClause01 : empty 
							| FunTypeParamClause'''
	if "FunTypeParamClause" in p[2]:
		p[0] = Node("FunTypeParamClause01", [p[1]], []).name
	else:
		p[0] = Node("FunTypeParamClause01", [p[1]], []).name

def p_FunDcl(p):
	'FunDcl : FunSig ColonType01'
	p[0] = Node("FunDcl", [p[1], p[2]], []).name

def p_VarDcl(p):
	'VarDcl : ids COLON Type'
	p[0] = Node("VarDcl", [p[1], p[3]], [p[2]]).name

def p_ValDcl(p):
	'ValDcl : ids COLON Type'
	p[0] = Node("ValDcl", [p[1], p[3]], [p[2]]).name

def p_Dcl(p):
	'''Dcl : R_VAL ValDcl
		| R_VAR VarDcl
		| R_DEF FunDcl
		| R_TYPE nl0more TypeDcl'''
	if len(p)==4:
		p[0] = Node("Dcl", [p[2],p[3]],[p[1]]).name
	elif "FunDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	elif "VarDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	else
		p[0] = Node("Dcl", [p[2]],[p[1]]).name

def p_ImportSelector(p):
	'ImportSelector : id ImpliesidorUnderscore01'
	p[0] = Node("ImportSelector", [p[1], p[2]], []).name

def p_ImpliesidorUnderscore01(p):
	'''ImpliesidorUnderscore01 : empty 
							 | 	R_IMPLIES1 id
							| R_IMPLIES1 UNDERSCORE'''
	if len(p)==4:
		p[0] = Node("Dcl", [p[2],p[3]],[p[1]]).name
	elif "FunDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	elif "VarDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name

def p_ImportSelectors(p):
	'''ImportSelectors : BLOCKOPEN ImportselectorComma0more ImportSelector BLOCKCLOSE
					| BLOCKOPEN ImportselectorComma0more UNDERSCORE BLOCKCLOSE '''
	if "ImportSelector" in p[3]:
		p[0] = Node("ImportSelectors", [p[2], p[3]], [p[1], p[4]]).name
	else:
		p[0] = Node("ImportSelectors", [p[2]], [p[1], p[3], p[4]]).name

def p_ImportselectorComma0more(p):
	'''ImportselectorComma0more : empty
							| ImportselectorComma0more ImportSelector COMMA'''
	if "ImportSelector" in p[2]:
		p[0] = Node("ImportselectorComma0more", [p[1], p[2]], [p[3]]).name
	else:
		p[0] = Node("ImportselectorComma0more", [p[1]], []).name
	
def p_ImportExpr(p):
	'''ImportExpr : StableId DOT id
				| StableId DOT UNDERSCORE
				| StableId DOT ImportSelectors'''
	if "ImportSelectors" in p[3]:
		p[0] = Node("ImportExpr", [p[3],p[1]],[p[2]]).name
	elif "id" in p[3]:
		p[0] = Node("ImportExpr", [p[3], p[1]], [p[2]).name
	else:
		p[0] = Node("ImportExpr", [p[1], p[3]], [p[2]]).name

def p_Import(p):
	'Import : R_IMPORT ImportExpr CommaImportExpr0more'
	p[0] = Node("Import", [p[2], p[3]], [p[1]]).name
	
def p_CommaImportExpr0more(p):
	'''CommaImportExpr0more : empty
						| CommaImportExpr0more COMMA ImportExpr'''
	if "ImportExpr" in p[3]:
		p[0] = Node("CommaImportExpr0more", [p[1], p[3]], [p[3]]).name
	else:
		p[0] = Node("CommaImportExpr0more", [p[1]], []).name

def p_SelfType(p):
	'''SelfType : id ColonType01 R_IMPLIES1
			| R_THIS COLON Type R_IMPLIES1'''
	if "id" in p[1]:
		p[0] = Node("SelfType", [p[1], p[2]], [p[3]]).name
	else:
		p[0] = Node("SelfType", [p[3]], [p[1], p[2], p[4]).name

def p_TemplateStat(p):
	'''TemplateStat : TopStat1 Modifier0more Def
				| TopStat1 Modifier0more Dcl
				| Expr
				| empty'''
	if "Def" in p[3]:
		p[0] = Node("TemplateStat", [p[1], p[2],p[3]],[]).name
	elif "Def" in p[3]:
		p[0] = Node("TemplateStat", [p[1], p[2],p[3]],[]).name
	elif "Expr" in p[1]:
		p[0] = Node("TemplateStat", [p[1]], []).name
	else:
		p[0] = Node("TemplateStat", [p[1]], []).name

def p_TemplateBody(p):
	'TemplateBody : nl01 BLOCKOPEN SelfType01 TemplateStat semiTemplateStat0more BLOCKCLOSE'
	p[0] = Node("TemplateBody", [p[1], p[3], p[4], p[5]], [p[2], p[6]]).name
 
def p_semiTemplateStat0more(p):
	'''semiTemplateStat0more : empty
							| semiTemplateStat0more semi TemplateStat'''
	if "semi" in p[2]:
		p[0] = Node("semiTemplateStat0more", [p[1], p[2],p[3]],[]).name
	else
		p[0] = Node("semiTemplateStat0more", [p[1]],[]).name

def p_SelfType01(p):
	'''SelfType01 : empty
					| SelfType'''
	if "semi" in p[1]:
		p[0] = Node("SelfType01", [p[1]],[]).name
	else
		p[0] = Node("SelfType01", [p[1]],[]).name

def p_NameValuePair(p):
	'NameValuePair : R_VAL id EQUALASS PrefixExpr'
	p[0] = Node("NameValuePair", [p[2],p[4]],[p[1],p[3]]).name

def p_ConstrAnnotation(p):
	'ConstrAnnotation : R_ATTHERATE SimpleType ArgumentExprs'
	p[0] = Node("ConstrAnnotation", [p[2],p[3]],[p[1]]).name

def p_Annotation(p):
	'Annotation : R_ATTHERATE SimpleType ArgumentExprs0more'
	p[0] = Node("Annotation", [p[2],p[3]],[p[1]]).name

def p_AccessQualifier(p):
	'''AccessQualifier : LSQRB id RSQRB
					| LSQRB R_THIS RSQRB'''
	if "id" in p[2]:
		p[0] = Node("AccessQualifier", [p[2]],[p[1], p[3]]).name
	else
		p[0] = Node("AccessQualifier", [],[p[1], p[2], p[3]]).name

def p_AccessModifier(p):
	'''AccessModifier : R_PRIVATE AccessQualifier01
					| R_PROTECTED AccessQualifier01'''
	if p[1] == "private":
		p[0] = Node("AccessModifier", [p[2]],[p[1]]).name
	else
		p[0] = Node("AccessModifier", [p[2]],[p[1]]).name

def p_AccessQualifier01(p):
	'''AccessQualifier01 : empty
						| AccessQualifier'''
	if "AccessQualifier" in p[1]:
		p[0] = Node("AccessQualifier01", [p[1]],[]).name
	else
		p[0] = Node("AccessQualifier01", [p[1]],[]).name

def p_LocalModifier(p):
	'''LocalModifier : R_ABSTRACT
					| R_FINAL
					| R_SEALED
					| R_IMPLICIT
					| R_LAZY'''
	if p[1] == "abstract":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "final":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "sealed":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "lazy":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	else
		p[0] = Node("LocalModifier", [p[1]],[]).name

def p_Modifier(p):
	'''Modifier : LocalModifier
			| AccessModifier
			| R_OVERRIDE'''
	if "LocalModifier" in p[1]:
		p[0] = Node("Modifier", [p[1]],[]).name
	if "AccessModifier" in p[1]:
		p[0] = Node("Modifier", [p[1]],[]).name
	else
		p[0] = Node("Modifier", [],[p[1]]).name

def p_Binding(p):
	'''Binding : id ColonType01
			| UNDERSCORE ColonType01''' 
	if "id" in p[1]:
		p[0] = Node("Binding", [p[1],p[2]],[]).name
	else
		p[0] = Node("Binding", [p[2]],[p[1]]).name

def p_Bindings(p):
	'Bindings : LPARAN Binding CommaBinding0more RPARAN' 
	p[0] = Node("Bindings", [p[2],p[3]],[p[1], p[4]]).name

def p_CommaBinding0more(p):
	'''CommaBinding0more : empty
						| CommaBinding0more COMMA Binding'''
	if "Binding" in p[3]:
		p[0] = Node("CommaBinding0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaBinding0more", [p[1]],[]).name

def p_ClassParam(p):
	'ClassParam : Annotation0more Modifier0more valvar01 id  COLON ParamType EqualExpr01'
	p[0] = Node("ClassParam", [p[1], p[2],p[3], p[4], p[6], p[7]],[p[5]]).name

def p_Annotation0more(p):
	'''Annotation0more : empty
					| Annotation0more Annotation'''
	if "Annotation" in p[2]:
		p[0] = Node("Annotation0more", [p[1],p[2]],[]).name
	else:
		p[0] = Node("Annotation0more", [p[1]],[]).name

def p_valvar01(p):
	'''valvar01 : empty
			| R_VAL
			| R_VAR'''
	if p[1] == "val":
		p[0] = Node("valvar01", [p[1]],[]).name
	if p[1] == "var":
		p[0] = Node("valvar01", [p[1]],[]).name
	else:
		p[0] = Node("valvar01", [p[1]],[]).name

def p_EqualExpr01(p):
	'''EqualExpr01 : empty
				| EQUALASS Expr'''
	if "Expr" in p[2]:
		p[0] = Node("EqualExpr01", [p[2]],[p[1]]).name
	else:
		p[0] = Node("EqualExpr01", [p[1]],[]).name

def p_ClassParams(p):
	'ClassParams : ClassParam CommaClassParam0more'
	p[0] = Node("ClassParams", [p[1],p[2]],[]).name

def p_CommaClassParam0more(p):
	'''CommaClassParam0more : empty
						| CommaClassParam0more COMMA ClassParam'''
	if "Expr" in p[2]:
		p[0] = Node("CommaClassParam0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaClassParam0more", [p[1]],[]).name

def p_ClassParamClause(p):
	'ClassParamClause : nl01 LPARAN ClassParams01 RPARAN'
	p[0] = Node("ClassParamClause", [p[1],p[3]],[p[2], p[4]]).name

def p_ClassParams01(p):
	'''ClassParams01 : empty
					| ClassParams '''
	if "ClassParams" in p[1]:
		p[0] = Node("ClassParams01", [p[1]],[]).name
	else:
		p[0] = Node("ClassParams01", [p[1]],[]).name

def p_ClassParamClauses(p):
	'ClassParamClauses : ClassParamClause0more Temp01'
	p[0] = Node("ClassParamClauses", [p[1],p[2]],[]).name

def p_ClassParamClause0more(p):
	'''ClassParamClause0more : ClassParamClause0more ClassParamClause
								| empty'''

def p_Temp01(p):
	'''Temp01 : nl01 LPARAN R_IMPLICIT ClassParams RPARAN
			| empty'''
	if "ClassParams" in p[4]:
		p[0] = Node("Temp01", [p[1], p[4]],[p[2], p[3], p[5]]).name
	else:
		p[0] = Node("Temp01", [p[1]],[]).name

def p_ParamType(p):
	'''ParamType : Type
				| R_IMPLIES1 Type
				| Type MULASS'''
	if len(p)==1:
		p[0] = Node("ParamType", [p[1]],[]).name
	elif "Type" in p[2]:
		p[0] = Node("ParamType", [p[2]],[p[1]]).name
	else:
		p[0] = Node("ParamType", [p[1]],[p[2]]).name

def p_Param(p):
	'Param : Annotation0more id ColonParamType01 EqualExpr01'
	p[0] = Node("Param", [p[1], p[2], p[3], p[4]],[]).name

def p_ColonParamType01(p):
	'''ColonParamType01 : empty
					| COLON ParamType'''
	if "ParamType" in p[2]:
		p[0] = Node("ParamType", [p[2]],[p[1]]).name
	else:
		p[0] = Node("ParamType", [p[1]],[]).name

def p_Params(p):
	'Params : Param CommaParam0more'
	p[0] = Node("Params", [p[1], p[2]],[]).name

def p_CommaParam0more(p):
	'''CommaParam0more : empty
					| CommaParam0more COMMA Param'''
	if "Param" in p[3]:
		p[0] = Node("CommaParam0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaParam0more", [p[1]],[]).name

def p_ParamClause(p):
	'ParamClause : nl01 LPARAN Params01 RPARAN'
	p[0] = Node("ParamClause", [p[1],p[3]],[p[2],p[4]]).name

def p_Params01(p):
	'''Params01 : empty
			| Params'''
	if "Params" in p[1]:
		p[0] = Node("Params01", [p[1]],[]).name
	else:
		p[0] = Node("Params01", [p[1]],[]).name

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

def p_Exprs(p):
	'Exprs : Expr  CommaExpr0more'

def p_CommaExpr0more(p):
	'''CommaExpr0more : CommaExpr0more COMMA Expr
					| empty'''

def p_SimpleExpr1(p):
	'''SimpleExpr1 : Literal
				| Path
				| UNDERSCORE
				| LPARAN Exprs RPARAN
				| LPARAN  RPARAN
				| SimpleExpr DOT id
				| SimpleExpr TypeArgs
				| SimpleExpr1 ArgumentExprs
				| XmlExpr'''

def p_SimpleExpr(p):
	'''SimpleExpr : R_NEW ClassTemplate
				| R_NEW TemplateBody
				| BlockExpr
				| SimpleExpr1 
				| SimpleExpr1 UNDERSCORE'''

def p_PrefixExpr(p):
	'''PrefixExpr : MINUS SimpleExpr
				| PLUS SimpleExpr
				| BITNEG SimpleExpr
				| SimpleExpr
				| NOT SimpleExpr'''

def p_InfixExpr(p):
	'''InfixExpr : PrefixExpr
				| InfixExpr id nl01 InfixExpr'''

def p_PostfixExpr(p):
	'''PostfixExpr : InfixExpr
				| InfixExpr id nl01'''

def p_semi01(p):
	'''semi01 : semi
			| empty'''

def p_Expr1(p):
	'''Expr1 : R_IF LPARAN Expr RPARAN nl0more Expr
		  | R_IF LPARAN Expr RPARAN nl0more Expr semi01 else Expr
		  | R_WHILE LPARAN Expr RPARAN nl0more Expr
		  | R_TRY BLOCKOPEN Block BLOCKCLOSE 
		  | R_TRY BLOCKOPEN Block BLOCKCLOSE R_CATCH BLOCKOPEN CaseClauses BLOCKCLOSE
		  | R_TRY BLOCKOPEN Block BLOCKCLOSE R_FINALLY Expr
		  | R_TRY BLOCKOPEN Block BLOCKCLOSE R_CATCH BLOCKOPEN CaseClauses BLOCKCLOSE R_FINALLY Expr
		  | R_DO Expr semi01 R_WHILE LPARAN Expr RPARAN
		  | R_FOR LPARAN Enumerators RPARAN nl0more R_YIELD Expr
		  | R_FOR BLOCKOPEN Enumerators BLOCKCLOSE nl0more R_YIELD Expr
		  | R_FOR LPARAN Enumerators RPARAN nl0more  Expr
		  | R_FOR BLOCKOPEN Enumerators BLOCKCLOSE nl0more  Expr
		  | R_THROW Expr
		  | R_RETURN 
		  | R_RETURN Expr
		  | SimpleExpr DOT id EQUALASS Expr
		  | id EQUALASS Expr
		  | SimpleExpr1 ArgumentExprs EQUALASS Expr
		  | PostfixExpr
          | PostfixExpr Ascription
          | PostfixExpr R_MATCH OPENBLOCK CaseClauses CLOSEBLOCK'''

def p_Expr(p):
	'''Expr : Bindings R_IMPLIES1 Expr
		 |   id  R_IMPLIES1 Expr
		 |  R_IMPLICIT id  R_IMPLIES Expr
		 |  UNDERSCORE R_IMPLIES Expr
		 | Expr1'''

def p_Ascription(p):
	'''Ascription : COLON InfixType
				| COLON Annotation Annotation0more
				| COLON UNDERSCORE MULTIPLICATION'''

def p_TypePat(p);
	'TypePat : Type'

def p_RefineStat(p):
	'''RefineStat : Dcl
				| R_TYPE TypeDef'''

def p_Refinement(p):
	'Refinement ::= nl01 BLOCKOPEN RefineStat semiRefineStat0more BLOCKCLOSE'

def p_semiRefineStat0more(p):
	'''semiRefineStat0more : semiRefineStat0more semi RefineStat
						| empty'''

def p_Types(p):
	'Types : Type CommaType0more'

def p_CommaType0more(p):
	'''CommaType0more : CommaType0more COMMA Type
					| empty'''

def p_TypeArgs(p):
	'TypeArgs : LSQRB Types RSQRB'

def p_SimpleType(p):
	'''SimpleType : SimpleType TypeArgs
		   		  | SimpleType R_HASH id
		   		  | StableId
		          | Path DOT R_TYPE
		          | LPARAN Types RPARAN'''

def p_AnnotType(p):
	'AnnotType : SimpleType Annotation0more'

def p_CompoundType(p):
	'''CompoundType : AnnotType withAnnotType0more 
				| AnnotType withAnnotType0more Refinement
				| Refinement'''

def p_InfixType(p):
	'InfixType : CompoundType idnl01CompoundType0more'

def p_idnl01CompoundType0more(p):
	'''idnl01CompoundType0more : idnl01CompoundType0more id nl01 CompoundType
							 | empty '''

def p_ExistentialDcl(p):
	'''ExistentialDcl : R_TYPE TypeDcl
					| R_VAL ValDcl'''

def p_ExistentialClause(p):
	'ExistentialClause : R_FORSOME OPENBLOCK ExistentialDcl semiExistentialDcl0more CLOSEBLOCK'

def p_semiExistentialDcl0more(p):
	'''semiExistentialDcl0more : semiExistentialDcl0more semi ExistentialDcl
							| empty'''

def p_FunctionArgTypes(p):
	'''FunctionArgTypes : InfixType
					| LPARAN ParamType CommaParamType0more  RPARAN
					| LPARAN  RPARAN'''
					
def p_CommaParamType0more(p):
	'''CommaParamType0more : CommaParamType0more COMMA ParamType
							| empty'''

def p_Type(p):
	'''Type : FunctionArgTypes R_IMPLIES1 Type
		| InfixType ExistentialClause
		| InfixType'''

def p_ClassQualifier(p):
	'ClassQualifier : LSQRB id RSQRB'

def p_StableId(p):
	'''StableId : id
			| Path DOT id
			| id DOT R_SUPER ClassQualifier01 DOT id
			| R_SUPER ClassQualifier01 DOT id'''

def p_ClassQualifier01(p):
	'''ClassQualifier01 : ClassQualifier
						| empty '''

def p_Path(p):
	'''Path : StableId
		| id DOT R_THIS
		|  R_THIS'''

def p_ids(p):
	'ids : id commaid0more'

def p_commaid0more(p):
	'''commaid0more : commaid0more COMMA ID
					| empty'''

def p_QualId(p):
	QualId : id Dotid0more

def p_Dotid0more(p):
	'''Dotid0more : Dotid0more DOT id
				| empty'''

def p_literals(p):
	'''literals : INT 
		| FLOAT 
		| STRING 
		| CHAR
		| R_NULL'''

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
