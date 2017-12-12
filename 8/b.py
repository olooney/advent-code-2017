import pyparsing
from pyparsing import Optional, Word, Literal, Forward, alphas, nums, \
    Group, OneOrMore, ZeroOrMore, oneOf, delimitedList, restOfLine, \
    QuotedString, Regex
from pprint import pprint

L = Literal
Ls = lambda expr: Literal(expr).suppress()

table = Forward()
array = Forward()

identifier = Word(alphas, alphas + nums + '_')
boolean = oneOf("true false")
integer = Word(nums)
double = Regex(r'[+-]?\d+\.\d*([eE][+-]?\d+)?').setParseAction(lambda t: float(t[0])) # TODO 
number = integer | double
string = QuotedString(quoteChar='"', escChar='\\')
value = number | boolean | string | table | array
key = integer | identifier
pair = Group(key + Ls(':') + value)

table << Group(Ls('{') + Optional(pair  + ZeroOrMore(Ls(',') + pair ) + Optional(Ls(','))) + Ls('}'))
array << Group(Ls('[') + Optional(value + ZeroOrMore(Ls(',') + value) + Optional(Ls(','))) + Ls(']'))

# statement = oneOf("return print read break continue")
# bin_op = oneOf("+ - * / % > < >= <= == != and or")
#line = register + instruction + integer + "if" + register + bin_op + integer

program = OneOrMore(value)
grammar = program

# comments
comment_one_line = Literal('//') + restOfLine
grammar.ignore(comment_one_line)
grammar.ignore(pyparsing.cStyleComment)


if __name__ == '__main__':
    import sys
    src = sys.stdin.read()
    pprint(grammar.parseString(src))

