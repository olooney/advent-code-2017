from pypeg2 import *
from pypeg2.xmlast import thing2xml

class Type(Keyword): 
    grammar = Enum( K("bool"), K("void"), K("int"), K("double"), K("float") )

class Parameter: 
    grammar = attr("type", Type), name()

class Parameters(Namespace): 
    #grammar = Parameter, maybe_some(",", Parameter)
    grammar = csl(Parameter)

class Instruction(str):
    grammar = [
        (word, ";"),
        (word, "=", word, ";"),
        (K("return"), "word", ";"),
    ]

block = "{", maybe_some(Instruction), "}"

class Function(List): 
    grammar = attr("type", Type), name(), "(", attr("params", Parameters), ")", block

class Program(List):
    grammar = some(Function)

program = '''

bool live_day(int age, bool female) {
    wake_up;
    eat;
    work;
    netflix;
    brush_teeth;
    sleep;
}

int live(bool female) {
    spawn;
    loop;
    live_day;
    endloop;
    die;
}

'''

tree = parse(program, Program)
print(repr(tree))
print(thing2xml(tree, pretty=True).decode())
