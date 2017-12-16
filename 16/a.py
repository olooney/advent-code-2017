import sys
import re
import string


def spin(data, n):
    return data[-n:] + data[:-n]

def exchange(data, i, j):
    data = data[:]
    data[i], data[j] = data[j], data[i]
    return data

def parse(line):
    line = line.strip()
    if line[0] == 's':
        op = lambda data: spin(data, int(line[1:]))
    if line[0] == 'x':
        i, j = [ int(l) for l in line[1:].split('/') ]
        op = lambda data: exchange(data, i, j)
    if line[0] == 'p':
        ni, nj = [ n for n in line[1:].split('/') ]
        op = lambda data: exchange(data, data.index(ni), data.index(nj))
    op.line = line
    return op
            

if __name__ == '__main__':
    lines = open(sys.argv[1])
    ops = [ parse(line) for line in lines ]
    data = list(string.ascii_lowercase[:16])
    original = string.ascii_lowercase[:16]
    print(''.join(data))
    for n in range(40):
        for op in ops:
            data = op(data)
            #print("{} => {}".format(op.line, ''.join(data)))
        #if ''.join(data) == original:
        print(n+1, ''.join(data))
    print(''.join(data))
