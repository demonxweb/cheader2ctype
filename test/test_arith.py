from ply import lex
from ply import yacc
from preproc import yacc_arith
from preproc import lex_arith
import time

if __name__=='__main__':
    nt = time.time()
    lexer = lex.lex(lex_arith,debug=0)

    s = '''1 + 1.6'''

    parser = yacc.yacc(module=yacc_arith,debug=0)

    r = parser.parse(s,lexer=lexer,debug=0)
    print(r)
    print(time.time()-nt)

    nt = time.time()
    print(1+2.4)
    print(time.time() - nt)