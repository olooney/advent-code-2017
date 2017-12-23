import string
import sys
from collections import defaultdict, deque, Counter

class VirtualMachine:
    def __init__(self, instructions):
        self.registers = defaultdict(int)
        self.pc = 0
        self.instructions = instructions
        self.profile = Counter()
        
    def run(self):
        while 0 <= self.pc < len(self.instructions):
            self.step()

    def step(self):
        instruction = self.instructions[self.pc]
        #print('{!r}; line {}: {}'.format(dict(self.registers), self.pc, instruction))
        offset = self.do(instruction)
        if offset is not None:
            self.pc += offset
        else:
            self.pc += 1

        return 0 <= self.pc < len(self.instructions)

    def do(self, instruction):
        parts = instruction.split(' ')
        op, args = parts[0], parts[1:]
        self.profile.update([op])
        op_handler = getattr(self, op)
        return op_handler(*args)

    def rvalue(self, arg):
        if arg in string.ascii_lowercase:
            return self.registers[arg]
        else:
            return int(arg)

    def set(self, x, y):
        self.registers[x] = self.rvalue(y)

    def add(self, x, y):
        self.registers[x] = self.rvalue(x) + self.rvalue(y)

    def sub(self, x, y):
        self.registers[x] = self.rvalue(x) - self.rvalue(y)

    def mul(self, x, y):
        self.registers[x] = self.rvalue(x) * self.rvalue(y)

    def mod(self, x, y):
        self.registers[x] = self.rvalue(x) % self.rvalue(y)

    def jgz(self, x, y):
        if self.rvalue(x) > 0:
            return self.rvalue(y)

    def jnz(self, x, y):
        if self.rvalue(x) != 0:
            return self.rvalue(y)
        

if __name__ == '__main__':
    with open(sys.argv[1]) as fin:
        code = fin.read().splitlines()
        vm = VirtualMachine(code)
        vm.do('set a 1')
        vm.run()
        print('registers:', vm.registers)
        print('profile:', vm.profile)



