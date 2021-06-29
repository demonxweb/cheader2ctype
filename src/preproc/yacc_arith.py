from preproc.lex_arith import tokens


def p_expr_plus(p):
    '''expression : factor PLUS factor'''
    p[0] = p[1]+p[3]

def p_int(p):
    'factor : INT'
    p[0] = int(p[1])

def p_float(p):
    'factor : FLOAT'
    p[0] = float(p[1])


def p_error(p):
    print('Error:',p)