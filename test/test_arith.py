from preproc.parser import PrePorc
import time

if __name__=='__main__':
    nt = time.time()


    s = ''' a + \\
    6 '''
    parser = PrePorc({'a':10})

    r = parser.parse(s)
    print(r)
    parser.print_lex(s)

    print(time.time()-nt)

