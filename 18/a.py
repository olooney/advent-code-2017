import string
import sys

TRAVERSABLE = string.ascii_letters + '+|-'

def read_network(filename):
    with open(filename) as fin:
        return [ list(line) for line in fin ]

def find_start(net):
    top = net[0]
    x = top.index('|')
    return ((x, 0), (0,1))

def propogate(net, p, v):
    steps = 1

    def wall(x, y):
        if not (0 <= y < len(net)): return ' '
        if not (0 <= x < len(net[y])): return ' '
        return net[y][x]
        

    def traversable(c, v):
        #return (c in TRAVERSABLE and not (v[0] and c == '|') and not (v[1] and c == '-'))
        return (c in TRAVERSABLE)

    x, y = p
    while True:
        c = wall(x, y)
        #print((x,y), repr(c), v)

        if c in string.ascii_letters:
            yield c

        nc = wall(x+v[0], y+v[1])
        if traversable(nc, v):
            pass
        elif c == '+' or c in string.ascii_letters:
            # turn left or right
            vl = (v[1], v[0])
            cl = wall(x+vl[0], y+vl[1])
            vr = (-v[1], -v[0])
            cr = wall(x+vr[0], y+vr[1])
            if traversable(cl, vl):
                v = vl
            elif traversable(cr, vr):
                v = vr
            else:
                break
        else:
            break

        steps += 1
        x += v[0]
        y += v[1]
    yield '. steps={}'.format(steps)

    
    
    

if __name__ == '__main__':
    net = read_network(sys.argv[1])
    p, v = find_start(net)
    for c in propogate(net, p, v):
        print(c, end='')
    print('.')

