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
	'break' : 'R_BREAK',
# 	'R_DEFAULT' used, but not defined as a token or a rule
# ERROR: parser3.py:443: Symbol 'IDVARNAME' used, but not defined as a token or a rule
# ERROR: parser3.py:447: Symbol 'R_UNTIL' used, but not defined as a token or a rule
# ERROR: parser3.py:448: Symbol 'R_TO' used, but not defined as a token or a rule
# ERROR: parser3.py:581: Symbol 'R_INSTANCEOF' used, but not defined as a token or a rule
	'default' : 'R_DEFAULT',
	'until' : 'R_UNTIL',
	'to' : 'R_TO',
	'array' : 'R_ARRAY',
	'instanceof' : 'R_INSTANCEOF',
	'continue' : 'R_CONTINUE',
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

tokens =list(reserved.values()) +  [
	'INT',
	'FLOAT',
	'STRING',
	'CHAR',
	'BOOL',
	'LPARAN',
	'RPARAN',
	'LSQRB',
	'RSQRB',
	'BLOCKOPEN',
	'BLOCKCLOSE',
	'GT',           #Greater than
	'GE',           #Grearer than equal
	'LT',           #Less than
	'LE',           #Less than equal
	'DIGIT',        #Digit
	'NONZERODIGIT',
    'ID',
	'BITAND',
	'BITOR',
	'BITXOR',
	'BITNEG',
	'BITLSHIFT',
	'BITRSHIFT',
	'BITRSFILL',    #bit right shift fill operator
	'EQUALASS',
	'ADDASS',
	'SUBASS',
	'MULASS',
	'MODASS',
	'DIVASS',
	'BITLEFTASS',
	'BITRIGHTASS',
	'BITANDASS',
	'BITORASS',
	'BITXORASS',
	'PLUS',
	'MINUS',
	'MULTIPLICATION',
	'DIVISION',
	'MODULUS',
	'EQUAL',
	'NOTEQUAL',
	'AND',
	'OR',
	'NOT',
	'STARTQUOTE',
	'ENDQUOTE',
	'DOT',
	'SEMICOLON',
	'COMMA',
	'BACKSPACE',
	'HORITAB',
	'LINEFEED',
	'FORMFEED',
	'CARRIAGERETN',
	'DOUBLEQUOTE',
	'SINGLEQUOTE',
	'BACKSLASH',
	'COLON',
	'COMMENT',
	'COLOR',
	'UNDERSCORE',
	'QUESTION',
	'BITRSFILLASS',
	'HEXDIGIT',
	'ZERO',
	'INTERGERTYPESUFFIX',
]
# <hex digit> :: = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | A | B | C | D | E | F
# <integer type suffix> ::= l | L

def t_COMMENT(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
	pass

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

@TOKEN(identifier)
def t_ID(t):
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t
t_QUESTION = r'\?'
t_HEXDIGIT = r'[0-9a-fA-F]'
t_INTERGERTYPESUFFIX = r'[lL]'
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_INT = r'[+-]?([0-9])+'
t_FLOAT = r'([+-])?[0-9]+\.([0-9]+([Ee]?[+-][0-9]+)?)?'
t_BOOL = r'(True | False)'
def t_CHAR(t):
	r'\'.\''
	t.value = t.value[1:-1]
	return t

def t_STRING(t):
	r'\"(\\.|[^\\"])*\"'
	t.value = t.value[1:-1]
	return t

t_DIGIT = r'[0-9]'
t_NONZERODIGIT = r'[1-9]'
t_ZERO = r'0'
t_LPARAN = r'\('
t_RPARAN = r'\)'
t_LSQRB = r'\['
t_RSQRB = r'\]'
t_BLOCKOPEN = r'\{'
t_BLOCKCLOSE = r'\}'
t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNEG = r'~'
t_BITLSHIFT = r'<<'
t_BITRSHIFT = r'>>'
t_BITRSFILL = r'>>>'
t_BITRSFILLASS = r'>>>='
t_EQUALASS = r'='
t_ADDASS = r'\+='
t_SUBASS = r'-='
t_MULASS = r'\*='
t_MODASS = r'%='
t_DIVASS = r'/='
t_BITLEFTASS = r'<<='
t_BITRIGHTASS = r'>>='
t_BITANDASS = r'&='
t_BITORASS = r'\|='
t_BITXORASS = r'\^='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_MODULUS = r'%'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_ignore  = ' \t'
t_BACKSPACE = r'\\b'
t_HORITAB = r'\t'
t_LINEFEED = r'\n'
t_FORMFEED = r'\f'
t_CARRIAGERETN = r'\r'
t_DOUBLEQUOTE = r'\"'
t_SINGLEQUOTE = r'\''
t_BACKSLASH = r'\\'
t_COLON = r':'
t_SEMICOLON = r';'
t_COLOR = r'\#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'
t_DOT = r'\.'
t_COMMA = r'\,'
t_UNDERSCORE = r'_'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

# Test it out

data = '''object addressbook {

  case class Person(name: String, age: Int)

  /** An AddressBook takes a variable number of arguments
   *  which are accessed as a Sequence
   */
  class AddressBook(a: Person*) {
    private val people: List[Person] = a.toList

    /** Serialize to XHTML. Scala supports XML literals
     *  which may contain Scala expressions between braces,
     *  which are replaced by their evaluation
     */
    def toXHTML =
      <table cellpadding="2" cellspacing="0">
        <tr>
          <th>Name</th>
          <th>Age</th>
        </tr>
        { for (val p <- people) yield
            <tr>
              <td> { p.name } </td>
              <td> { p.age.toString() } </td>
            </tr> 
        }
      </table>;
  }

  /** We introduce CSS using raw strings (between triple
   *  quotes). Raw strings may contain newlines and special
   *  characters (like \) are not interpreted.
   */
  val header =
    <head>
      <title>
        { "My Address Book" }
      </title>
      <style type="text/css"> {
     """table { border-right: 1px solid #cccccc; }
        th { background-color: #cccccc; }
        td { border-left: 1px solid #acacac; }
        td { border-bottom: 1px solid #acacac;"""}
      </style>
    </head>;

  val people = new AddressBook(
    Person("Tom", 20),
    Person("Bob", 22),
    Person("James", 19));

  val page =
    <html>
      { header }
      <body>
       { people.toXHTML }
      </body>
    </html>;

  def main(args: Array[String]) {
    println(page)
  }
}'''
data = "10.5E-5"
data = "\"Rahul is intelligent\""
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
