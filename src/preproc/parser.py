from preproc.arith_lex import ArithLexer
from ply import yacc
class PrePorc:
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )
    def __init__(self,defined={}):
        self.lexer = ArithLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self,
                                start='expression',
                                )
        self.defined = defined

    def print_lex(self,s):
        self.lexer.lexer.input(s)
        while True:
            tok = self.lexer.lexer.token()
            if not tok:
                break
            print(tok)


    def define(self,k,isstr=False):
        if isstr:
            if k in self.defined.keys():
                return self.defined.get(k)
            else:
                return k

        else:
            return self.defined.get(k)


    def parse(self,data):
        return self.parser.parse(input=data,lexer=self.lexer.lexer)

    def p_int(self,p):
        'number : INT'
        p[0] = eval(p[1])
    def p_n_int(self,p):
        'number : MINUS INT'
        p[0] = - eval(p[2])

    def p_float(self,p):
        'number : FLOAT'
        p[0] = float(p[1])
    def p_n_float(self,p):
        'number : MINUS FLOAT'
        p[0] = -float(p[2])

    def p_id(self,p):
        'id : ID'
        p[0] = self.define(p[1])

    def p_n_id(self,p):
        'id : MINUS ID'
        p[0] = -self.define(p[2])

    def p_factor(self,p):
        '''factor : number
                  | id'''
        p[0] = p[1]



    def p_expr(self, p):
        '''expression : LPAREN expression RPAREN
                      | factor'''
        if len(p) ==2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]

    def p_expr_math(self,p):
        '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression MODULO expression
                    '''
        if p[2]=='+':
            p[0] = p[1]+p[3]
        elif p[2]=='-':
            p[0] = p[1]-p[3]
        elif p[2]=='*':
            p[0] = p[1]*p[3]
        elif p[2]=='/':
            p[0] = p[1]/p[3]
        elif p[2]=='%':
            p[0] = p[1]%p[3]
    def p_bin(self,p):
        '''expression : expression LSHIFT expression
                      | expression RSHIFT expression
                      | expression OR expression
                      | expression AND expression
                      | expression XOR expression
                      '''
        if p[2] == '>>':
            p[0] = p[1] >> p[3]
        elif p[2] == '<<':
            p[0] = p[1] << p[3]
        elif p[2] == '|':
            p[0] = p[1] | p[3]
        elif p[2] == '&':
            p[0] = p[1] & p[3]
        elif p[2] == '^':
            p[0] = p[1] & p[3]
    def p_n_b(self,p):
        '''expression : NOT expression'''
        p[0] = ~p[2]

    def p_n_logic(self,p):
        '''expression : LNOT expression'''
        p[0] = not p[2]
    def p_logic(self,p):
        '''expression : expression LOR expression
                      | expression LAND expression
                      | expression LT expression
                      | expression GT expression
                      | expression LE expression
                      | expression GE expression
                      | expression EQ expression
                      | expression NE expression
                      '''

        if p[2] == '&&':
            p[0] = p[1] and p[3]
        elif p[2] == '||':
            p[0] = p[1] or p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '!=':
            p[0] = p[1] != p[3]

    def p_error(self,p):
        print('Error:',p)
        # if p.type=='NEXTLINE':
        #     tok = yacc.token()
        #     return tok