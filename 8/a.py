import pyparsing
from pyparsing import Optional, Word, Literal, Forward, alphas, nums, \
    Group, ZeroOrMore, oneOf, delimitedList, restOfLine
from pprint import pprint

comment_one_line = Literal("//") + restOfLine
register = Word(alphas)
integer = Word(nums)
instruction = oneOf("inc dec")
bin_op = oneOf("> < >= <= == !=")
line = register + instruction + integer + "if" + register + bin_op + integer
program = ZeroOrMore(line)
grammar = program

grammar.ignore(comment_one_line)
grammar.ignore(pyparsing.cStyleComment)

if __name__ == '__main__':
    import sys
    src = sys.stdin.read()
    pprint(grammar.parseString(src).asList())





