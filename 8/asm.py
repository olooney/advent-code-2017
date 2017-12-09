import sys
from pprint import pprint

from asm_ast import Context
from asm_grammar import parse

if __name__ == '__main__':
    src = sys.stdin.read()
    statements = parse(src)
    context = Context()
    greatest = 0
    for statement in statements:
        #print(statement)
        statement.eval(context)
        greatest = max(greatest, max(context.values()))
        #pprint(context)
    print('largest register at end: {}'.format(max(context.values())))
    print('largest register ever encountered: {}'.format(greatest))


