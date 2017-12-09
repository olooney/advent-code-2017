'''AST classes for the little assembly language.
'''
class Context(dict):
    def eval(self, var):
        if type(var) == str:
            if var not in self:
                self[var] = 0
            return self[var]
        elif type(var) == int:
            return var

class Statement:
    def __init__(self, reg, instruction, arg, condition):
        self.reg = str(reg)
        self.instruction = str(instruction)
        self.arg = arg
        self.condition = condition

    def __repr__(self):
        return '{}({}, {}) {}'.format(instruction, reg, arg, condition)
    __str__ = __repr__

    def eval(self, context):
        if self.conditional.eval(context):
            arg = context.eval(self.arg)
            if self.instruction == 'inc':
                context[self.reg] += arg
            elif self.instruction == 'dec':
                context[self.reg] -= arg


class Condition:
    OPS = {
        ">": lambda x,y: x>y,
        "<": lambda x,y: x<y,
        ">=": lambda x,y: x>=y,
        "<=": lambda x,y: x<=y,
        "==": lambda x,y: x==y,
        "!=": lambda x,y: x!=y,
    }
    def __init__(self, lhs, bin_op, rhs):
        self.lhs = lhs
        self.bin_op = bin_op
        self.rhs = rhs

    def __repr__(self):
        return 'if({} {} {})'.format(lhs, bin_op, rhs)
    __str__ = __repr__

    def eval(self, context):
        lhs = context.eval(self.lhs)
        rhs = context.eval(self.lhs)
        return OPS(lhs, rhs)
        

__all__ = ['Context', 'Statement', 'Condition']
