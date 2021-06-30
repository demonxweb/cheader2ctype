from ply import lex
class ArithLexer:
    def __init__(self):
        self.lexer = lex.lex(object=self)

    tokens = [
        'ID',
        'INT','FLOAT','STRING','CHAR',
        'COMA',
        'PLUS','MINUS','TIMES','DIVIDE','MODULO',
        'OR','AND','NOT','XOR','LSHIFT','RSHIFT',
        'LOR','LAND','LNOT',
        'LT','GT','LE','GE','EQ','NE',
        'ARROW',
        'LPAREN','RPAREN',
        'NEXTLINE','WS',
        'COMMENT','COMMENT2'
    ]

    t_ID = r'[A-Za-z_][A-Za-z0-9_]*'
    pat_hex = r'0x[0-9A-Fa-f]+'
    t_INT = r'('+pat_hex+'|\d+([uU]|[lL]|[uU][lL]|[lL][uU])?)'
    t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

    t_STRING = r'\"([^\\\n]|(\\.))*?\"'
    t_CHAR = r'(L)?\'([^\\\n]|(\\.))*?\''

    t_COMA             = r','

    t_PLUS             = r'\+'
    t_MINUS            = r'-'
    t_TIMES            = r'\*'
    t_DIVIDE           = r'/'
    t_MODULO           = r'%'
    t_LSHIFT           = r'<<'
    t_RSHIFT           = r'>>'

    t_OR               = r'\|'
    t_AND              = r'&'
    t_NOT              = r'~'
    t_XOR              = r'\^'

    t_LOR              = r'\|\|'
    t_LAND             = r'&&'
    t_LNOT             = r'!'
    t_LT               = r'<'
    t_GT               = r'>'
    t_LE               = r'<='
    t_GE               = r'>='
    t_EQ               = r'=='
    t_NE               = r'!='


    t_ARROW            = r'->'

    t_LPAREN           = r'\('
    t_RPAREN           = r'\)'



    def t_WS(self,t):
        r'\s+'

    def t_NEXTLINE(self,t):
        r'\\\s*\n'

    def t_COMMENT(self,t):
        r'/\*(.|\n)*?\*/'

    def t_COMMENT2(self,t):
        r'//.*\n'


    def t_error(self,t):
        t.type = t.value[0]
        t.value = t.value[0]
        t.lexer.skip(1)
        return t

