import sys, traceback
import pyparsing
from pyparsing import Optional, Word, Literal, Forward, alphas, nums, \
    Group, OneOrMore, ZeroOrMore, oneOf, delimitedList, restOfLine, Regex
from asm_ast import Context, Statement, Condition

# short-hand utility functions
L = Literal
Ls = lambda expr: L(expr).suppress()

def make(cls):
    def maker(token):
        try:
            return cls(*token[0].asList())
        except:
            import sys
            traceback.print_exc(file=sys.stderr)
    return maker

# atomic
register = Word(alphas)
integer = Regex(r'[+-]?(0|[1-9][0-9]*)').setParseAction(lambda token:int(token[0]))
instruction = oneOf("inc dec")
bin_op = oneOf("> < >= <= == !=")

# complex
condition = Group(Ls("if") + register + bin_op + integer).setParseAction(make(Condition))
statement = Group(register + instruction + integer + condition).setParseAction(make(Statement))
program = OneOrMore(statement)
grammar = program

# comments
comment_one_line = L("//") + restOfLine
grammar.ignore(comment_one_line)
grammar.ignore(pyparsing.cStyleComment)

def parse(src):
    '''returns a list of Statement objects parsed from the input string.'''
    return grammar.parseString(src).asList()

__all__ = ['parse']

