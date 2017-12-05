import sys

def dump(mem, pc):
    for i, m in enumerate(mem):
        if i == pc:
            print('({:>4d})'.format(int(m)), end='')
        else:
            print(' {:>4d} '.format(int(m)), end='')
    print()

def jmp(mem):
    mem = [ int(m) for m in mem ]
    pc = 0
    steps = 0
    memsize = len(mem)
    while 0 <= pc < memsize:
        # dump(mem, pc)
        offset = mem[pc]
        mem[pc] += 1
        pc += offset
        steps += 1
    return steps
        
if __name__ == '__main__':
    mem = [ int(line) for line in sys.stdin.read().splitlines() ]
    print(jmp(mem))

