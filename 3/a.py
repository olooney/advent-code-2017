from math import *
from itertools import islice
import sys
import numpy as np

def location(address):
    ''' returns pair (x,y) for the spiral address'''
    p = (0,0)
    min_square = int(floor(sqrt(address)))
    odd_square = min_square if min_square % 2 else min_square -1
    odd_square_x = (odd_square -1)//2
    odd_square_y = -odd_square_y
    p = (odd_square_x+1, odd_square_y)

    base_address = odd_square**2 + 1
    offset = address - base_address
    edge_length = odd_square + 2

    # first side is 1 short, last side is one long...
    if offset < side_length -1:
        return (p[0], p[1] + offset)
    else:
        p = (p[0], p[1] + side_length-2)


def spiral_instructions():
    while True:
        yield 'r', stride
        yield 'u', stride
        stride += 1
        yield 'l', stride
        yield 'd', stride
        stride += 1

def follow(instructions, initial_position=None, until_address=sys.maxsize):
    address = 1
    p = initial_position or (0, 0)
    for dir, stride in instructions:
        if address + stride >= until_address:
            stride = until_address - stride

        if dir == 'r': p[0] += stride
        elif dir == 'l': p[0] -= stride
        elif dir == 'u': p[1] -= stride
        elif dir == 'd': p[1] += stride
        else:
            raise ValueError("unknown direction")

        address += stride
        if address == until_address:
            break
    return p




