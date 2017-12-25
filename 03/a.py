from math import *
from itertools import islice
import sys
import numpy as np

def no_op(*args, **kwargs):
    pass

memory = {
        (0,0): 1
}

def neighbors(p):
    yield (p[0], p[1]+1)
    yield (p[0], p[1]-1)
    yield (p[0]+1, p[1])
    yield (p[0]-1, p[1])

    yield (p[0]-1, p[1]-1)
    yield (p[0]-1, p[1]+1)
    yield (p[0]+1, p[1]-1)
    yield (p[0]+1, p[1]+1)

def spiral_instructions():
    stride = 1
    while True:
        yield 'r', stride
        yield 'u', stride
        stride += 1
        yield 'l', stride
        yield 'd', stride
        stride += 1

def follow(instructions, initial_position=None, until_address=sys.maxsize):
    address = 1
    p = list(initial_position) if initial_position else [0, 0]
    for dir, stride in instructions:
        if address + stride >= until_address:
            stride = until_address - address

        if dir == 'r': p[0] += stride
        elif dir == 'l': p[0] -= stride
        elif dir == 'u': p[1] += stride
        elif dir == 'd': p[1] -= stride
        else:
            raise ValueError("unknown direction")

        address += stride
        if address == until_address:
            break
    return p, address



def visit(instructions, initial_position=None, until_address=sys.maxsize, visitor=no_op):
    address = 1
    p = list(initial_position) if initial_position else [0, 0]
    for dir, stride in instructions:

        while stride:
            if dir == 'r': p[0] += 1
            elif dir == 'l': p[0] -= 1
            elif dir == 'u': p[1] += 1
            elif dir == 'd': p[1] -= 1
            else:
                raise ValueError("unknown direction")

            stride -= 1
            address += 1
            ret = visitor(p, address)
            if ret:
                return ret
            if address >= until_address:
                return p, address

    return p, address

def stress_memory(puzzle_input):

    def stressful_visitor(p, addr):
        p = tuple(p)
        if p not in memory:
            value = sum(memory.get(np, 0) for np in neighbors(p))
            memory[p] = value
            if value > puzzle_input:
                return value, p, addr

    value, p, addr = visit(spiral_instructions(), visitor=stressful_visitor)
    #print(value, p, addr)
    return value

if __name__ == '__main__':
    print stress_memory(325489)

