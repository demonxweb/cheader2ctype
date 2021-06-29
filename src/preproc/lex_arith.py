tokens = [
    'ID',
    'INT','FLOAT','HEX','STRING','CHAR',
    'COMA',
    'PLUS','MINUS','TIMES','DIVIDE','MODULO',
    'OR','AND','NOT','XOR','LSHIFT','RSHIFT',
    'LOR','LAND','LNOT',
    'LT','GT','LE','GE','EQ','NE',
    'ARROW',
    'TOSTR','CONCAT',
    'LPAREN','RPAREN',
    'NEXTLINE','WS',
    'COMMENT','COMMENT2'
]

t_ID = r'[A-Za-z_][A-Za-z0-9_]*'
t_INT = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_HEX = r'0x[0-9A-Fa-f]+'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_CHAR = r'(L)?\'([^\\\n]|(\\.))*?\''

t_COMA             = r','

t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MODULO           = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='
t_TOSTR            = r'\#'
t_CONCAT           = r'\#\#'

t_ARROW            = r'->'

t_LPAREN           = r'\('
t_RPAREN           = r'\)'


t_NEXTLINE = r'\\\s*\n'

def t_WS(t):
    r'\s+'

def to_NEXTLINE(t):
    r'\\ *\n'
    return t

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'

def t_COMMENT2(t):
    r'//.*\n'


def t_error(t):
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

def p_factor(p):
    '''factor : INT
             | FLOAT'''
    print(p[1])
    p[0] = int(p[1])

def p_expr_plus(p):
    '''expression : factor PLUS factor'''
    p[0] = p[1]+p[3]
def p_error(p):
    print("Syntax error in input!")