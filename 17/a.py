import string
import sys
from collections import defaultdict

class Player:
    def __init__(self, instructions):
        self.sound = 0
        self.registers = defaultdict(int)
        self.pc = 0
        self.instructions = instructions
        self.cycles = 0

    def run(self):
        while 0 <= self.pc < len(self.instructions):
            self.step()
            self.cycles += 1

    def step(self):
        instruction = self.instructions[self.pc]
        print('sound: {} reg: {!r} line {}: {}'.format(self.sound, dict(self.registers), self.pc, instruction))
        offset = self.do(instruction)
        if offset is not None:
            self.pc += offset
        else:
            self.pc += 1

    def do(self, instruction):
        parts = instruction.split(' ')
        op, args = parts[0], parts[1:]
        op_handler = getattr(self, op)
        return op_handler(*args)

    def rvalue(self, arg):
        if arg in string.ascii_lowercase:
            return self.registers[arg]
        else:
            return int(arg)

    def snd(self, x):
        self.sound = self.rvalue(x)

    def set(self, x, y):
        self.registers[x] = self.rvalue(y)

    def add(self, x, y):
        self.registers[x] = self.rvalue(x) + self.rvalue(y)

    def mul(self, x, y):
        self.registers[x] = self.rvalue(x) * self.rvalue(y)

    def mod(self, x, y):
        self.registers[x] = self.rvalue(x) % self.rvalue(y)

    def rcv(self, x):
        if self.rvalue(x) > 0:
            print('recovered:', self.sound)
            self.registers[x] = self.sound
            return -9999
        else:
            print('recover skipped')

    def jgz(self, x, y):
        if self.rvalue(x) > 0:
            return self.rvalue(y)
        

if __name__ == '__main__':
    with open(sys.argv[1]) as fin:
        player = Player(fin.read().splitlines())
        player.run()
        print(player.sound, player.registers)

