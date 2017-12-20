import string
import sys
from collections import defaultdict, deque

class Player:
    def __init__(self, instructions, program_id):
        self.registers = defaultdict(int)
        self.registers['p'] = program_id
        self.pc = 0
        self.instructions = instructions
        self.message_queue = deque()
        self.blocked = False
        self.messages_sent = 0
        self.messages_received = 0

    def bind(self, partner):
        self.partner = partner

    def pass_message(self, value):
        self.messages_received += 1
        self.message_queue.appendleft(value)

    def run(self):
        while 0 <= self.pc < len(self.instructions):
            self.step()

    def step(self):
        instruction = self.instructions[self.pc]
        #print('p{}: q: {!r} reg: {!r} line {}: {}'.format(self.registers['p'], list(self.message_queue), dict(self.registers), self.pc, instruction))
        offset = self.do(instruction)
        if offset is not None:
            self.pc += offset
        else:
            self.pc += 1

        return 0 <= self.pc < len(self.instructions)

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
        self.messages_sent += 1
        self.partner.pass_message(self.rvalue(x))

    def set(self, x, y):
        self.registers[x] = self.rvalue(y)

    def add(self, x, y):
        self.registers[x] = self.rvalue(x) + self.rvalue(y)

    def mul(self, x, y):
        self.registers[x] = self.rvalue(x) * self.rvalue(y)

    def mod(self, x, y):
        self.registers[x] = self.rvalue(x) % self.rvalue(y)

    def rcv(self, x):
        if self.message_queue:
            self.blocked = False
            self.registers[x] = self.message_queue.pop()
        else:
            self.blocked = True
            return 0  # blocks

    def jgz(self, x, y):
        if self.rvalue(x) > 0:
            return self.rvalue(y)
        

if __name__ == '__main__':
    with open(sys.argv[1]) as fin:
        code = fin.read().splitlines()
        player0 = Player(code, 0)
        player1 = Player(code, 1)
        player0.bind(player1)
        player1.bind(player0)

    cycles = 0
    max_cycles = int(1e6)
    while cycles < max_cycles and player0.step() and player1.step():
        if player0.blocked and player1.blocked:
            print('deadlocked!')
            break
        cycles += 1
    print('total cycles: {}'.format(cycles))
    print('player0 sent {} messages and recieved {}.'.format(player0.messages_sent, player0.messages_received))
    print('player1 sent {} messages and recieved {}.'.format(player1.messages_sent, player1.messages_received))


