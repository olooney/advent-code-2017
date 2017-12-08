import pyparsing
from pyparsing import Optional, Word, Literal, Forward, alphas, nums, \
    Group, ZeroOrMore, oneOf, delimitedList, restOfLine
from pprint import pprint

comment_one_line = Literal("//") + restOfLine
identifier = Word(alphas+"_", alphas+nums+"_$")
integer_literal = Word(nums)
semicolon = Literal(';').suppress()
left_bracket = Literal('{').suppress()
right_bracket = Literal('}').suppress()

type_spec = Optional("const") + oneOf("void int float char") + Optional("*")
member = Group( type_spec + identifier + semicolon )
struct = Group(oneOf("struct class") + identifier + left_bracket + ZeroOrMore(member) + right_bracket + semicolon)

grammar = struct

grammar.ignore(comment_one_line)
grammar.ignore(pyparsing.cStyleComment)

if __name__ == '__main__':
    import sys
    src = sys.stdin.read()
    pprint(grammar.parseString(src).asList())





