import ply.lex as lex
from ply.lex import TOKEN

reserved = {
	'abstract' : 'R_ABSTRACT',
	'do'  : 'R_DO',
	'finally' : 'R_FINALLY',
	'import' : 'R_IMPORT',
	'object' : 'R_OBJECT',
	'override' : 'R_OVERRIDE',
	'package' : 'R_PACKAGE',
	'private' : 'R_PRIVATE',
	'protected' : 'R_PROTECTED',
	'return' : 'R_RETURN',
	'sealed' : 'R_SEALED',
 	'super' : 'R_SUPER',
	'this' : 'R_THIS',
	'throw' : 'R_THROW',
	'trait' : 'R_TRAIT',
	'try' : 'R_TRY',
	'true' : 'R_TRUE',
	'type' : 'R_TYPE', 
	'val' : 'R_VAL', 
	'var' : 'R_VAR', 
	'while' : 'R_WHILE',  
	'with' : 'R_WITH',
	'yield' : 'R_YIELD',
	'case' :'R_CASE',
	'catch' : 'R_CATCH',
	'class' : 'R_CLASS',
	'def' : 'R_DEF',
 	'else' : 'R_ELSE',
 	'extends' : 'R_EXTENDS',
 	'false' : 'R_FALSE', 
	'final' : 'R_FINAL',
 	'for' : 'R_FOR',
	'forSome' : 'R_FORSOME',
	'if' : 'R_IF',
	'implicit' : 'R_IMPLICIT',
 	'lazy' : 'R_LAZY',
	'match' : 'R_MATCH',
	'new' : 'R_NEW', 
	'null' : 'R_NULL',
	'\u21D2' : 'R_IMPLIES',
	'\u2190' : 'R_LEFTARROW',
	'=>' : 'R_IMPLIES1',
	'<-' : 'R_LEFTARROW1',
	'<:' : 'R_OBSCURE',
	'#' : 'R_HASH',
	'@' : 'R_ATTHERATE',
	'<%' : 'R_OBSCURE1',
	'>:' : 'R_OBSCURE2',
	'Byte' : 'R_BYTE',
	'Short' : 'R_SHORT',
	'Int' : 'R_INT',
	'Long' : 'R_LONG',
	'Float' : 'R_FLOAT',
	'Double' : 'R_DOUBLE',
	'Char' : 'R_CHAR',
	'String' : 'R_STRING',
	'Boolean' : 'R_BOOLEAN',
	'Unit' : 'R_UNIT',
	'Null' : 'R_NULL1',
	'Nothing' : 'R_NOTHING',
	'Any' : 'R_ANY',
	'AnyRef' : 'R_ANYREF'
}



whiteSpace       ::=  ‘\u0020’ | ‘\u0009’ | ‘\u000D’ | ‘\u000A’
upper            ::=  ‘A’ | … | ‘Z’ | ‘$’ | ‘_’  // and Unicode category Lu
upper = r'[A-Z$_]'
lower            ::=  ‘a’ | … | ‘z’ // and Unicode category Ll
lower = r'[a-z]'
letter           ::=  upper | lower // and Unicode categories Lo, Lt, Nl
letter = r'(' + upper + r'|' lower + r')'
digit            ::=  ‘0’ | … | ‘9’
digit = r'[0-9]'
paren            ::=  ‘(’ | ‘)’ | ‘[’ | ‘]’ | ‘{’ | ‘}’
paren = r'[\(\)\[\]\{\}]'
delim            ::=  ‘`’ | ‘'’ | ‘"’ | ‘.’ | ‘;’ | ‘,’
delim = r'[`'"\.;,]'
opchar           ::= // printableChar not matched by (whiteSpace | upper | lower |
                     // letter | digit | paren | delim | opchar | Unicode_Sm | Unicode_So)
printableChar    ::= // all characters in [\u0020, \u007F] inclusive
charEscapeSeq    ::= ‘\‘ (‘b‘ | ‘t‘ | ‘n‘ | ‘f‘ | ‘r‘ | ‘"‘ | ‘'‘ | ‘\‘)
charEscapeSeq = r'\\[btnfr"\'\]'
op               ::=  opchar {opchar}
varid            ::=  lower idrest
varid = r'(' + lower + idrest r')'
plainid          ::=  upper idrest
                 |  varid
                 |  op
id               ::=  plainid
                 |  ‘`’ stringLiteral ‘`’
idrest           ::=  {letter | digit} [‘_’ op]

integerLiteral   ::=  (decimalNumeral | hexNumeral) [‘L’ | ‘l’]
decimalNumeral   ::=  ‘0’ | nonZeroDigit {digit}
hexNumeral       ::=  ‘0’ (‘x’ | ‘X’) hexDigit {hexDigit}
digit            ::=  ‘0’ | nonZeroDigit
nonZeroDigit     ::=  ‘1’ | … | ‘9’

floatingPointLiteral
                 ::=  digit {digit} ‘.’ digit {digit} [exponentPart] [floatType]
                 |  ‘.’ digit {digit} [exponentPart] [floatType]
                 |  digit {digit} exponentPart [floatType]
                 |  digit {digit} [exponentPart] floatType
exponentPart     ::=  (‘E’ | ‘e’) [‘+’ | ‘-’] digit {digit}
floatType        ::=  ‘F’ | ‘f’ | ‘D’ | ‘d’

booleanLiteral   ::=  ‘true’ | ‘false’

characterLiteral ::=  ‘'’ (printableChar | charEscapeSeq) ‘'’

stringLiteral    ::=  ‘"’ {stringElement} ‘"’
                 |  ‘"""’ multiLineChars ‘"""’
stringElement    ::=  (printableChar except ‘"’)
                 |  charEscapeSeq
multiLineChars   ::=  {[‘"’] [‘"’] charNoDoubleQuote} {‘"’}

symbolLiteral    ::=  ‘'’ plainid

comment          ::=  ‘/*’ “any sequence of characters; nested comments are allowed” ‘*/’
                 |  ‘//’ “any sequence of characters up to end of line”

nl               ::=  “newlinecharacter”“newlinecharacter”
semi             ::=  ‘;’ |  nl {nl}
