'''AST classes for the little assembly language.
'''

OPS = {
    ">": lambda x,y: x>y,
    "<": lambda x,y: x<y,
    ">=": lambda x,y: x>=y,
    "<=": lambda x,y: x<=y,
    "==": lambda x,y: x==y,
    "!=": lambda x,y: x!=y,
}

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
        return '{}({}, {}) {!r}'.format(self.instruction, self.reg, self.arg, self.condition)
    __str__ = __repr__

    def eval(self, context):
        if self.condition.eval(context):
            arg = context.eval(self.arg)
            val = context.eval(self.reg) 
            if self.instruction == 'inc':
                context[self.reg] = val + arg
            elif self.instruction == 'dec':
                context[self.reg] = val - arg


class Condition:
    def __init__(self, lhs, bin_op, rhs):
        self.lhs = lhs
        self.bin_op = bin_op
        self.rhs = rhs

    def __repr__(self):
        return 'if({} {} {})'.format(self.lhs, self.bin_op, self.rhs)
    __str__ = __repr__

    def eval(self, context):
        lhs = context.eval(self.lhs)
        rhs = context.eval(self.rhs)
        bin_op = OPS[self.bin_op]
        return bin_op(lhs, rhs)
        

__all__ = ['Context', 'Statement', 'Condition']
